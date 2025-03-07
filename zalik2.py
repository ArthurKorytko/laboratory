import logging
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime, timedelta

TOKEN = "-"
bot = Bot(token=TOKEN)
dp = Dispatcher()

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT,
    deadline TEXT
)
""")
conn.commit()


class TaskState(StatesGroup):
    waiting_for_text = State()
    waiting_for_deadline = State()


async def send_notifications():
    while True:
        now = datetime.now()
        cursor.execute("SELECT id, user_id, text FROM tasks WHERE deadline <= ?",
                       (now.strftime('%m-%d %H:%M'),))
        for task_id, user_id, text in cursor.fetchall():
            await bot.send_message(user_id, f"1Напоминание! {text}")
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
        await asyncio.sleep(60)


def get_tasks_markup(user_id):
    cursor.execute("SELECT id, text FROM tasks WHERE user_id = ?", (user_id,))
    buttons = [InlineKeyboardButton(
        text=f"{text[:20]}", callback_data=f"view_{task_id}") for task_id, text in cursor.fetchall()]
    return InlineKeyboardMarkup(inline_keyboard=[buttons[i:i+2] for i in range(0, len(buttons), 2)]) if buttons else None


def get_tasks_with_delete_markup(user_id):
    cursor.execute("SELECT id, text FROM tasks WHERE user_id = ?", (user_id,))
    buttons = [InlineKeyboardButton(
        text=f"❌ {text[:20]}", callback_data=f"delete_{task_id}") for task_id, text in cursor.fetchall()]
    return InlineKeyboardMarkup(inline_keyboard=[buttons[i:i+2] for i in range(0, len(buttons), 2)]) if buttons else None


@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="Добавить задачу"), KeyboardButton(
            text="Список задач"), KeyboardButton(text="Удалить задачу")]
    ])
    await message.answer("Привет! Я твой менеджер задач. Нажми 'Добавить задачу' для создания новой.", reply_markup=keyboard)


@dp.message(F.text == "Добавить задачу")
async def add_task_start(message: types.Message, state: FSMContext):
    await message.answer("Введите текст задачи:")
    await state.set_state(TaskState.waiting_for_text)


@dp.message(TaskState.waiting_for_text)
async def add_task_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Введите дату и время дедлайна в формате MM.DD HH:MM или напишите 'нет' для автоматического времени (через 1 час):")
    await state.set_state(TaskState.waiting_for_deadline)


@dp.message(TaskState.waiting_for_deadline)
async def add_task_deadline(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await state.get_data()
    task_text = user_data.get("text")
    deadline_str = message.text.strip()

    if deadline_str.lower() == "нет":
        deadline = datetime.now() + timedelta(hours=1)
    else:
        try:
            deadline = datetime.strptime(deadline_str, '%m.%d %H:%M')
        except ValueError:
            await message.answer("Неверный формат даты. Используйте MM.DD HH:MM")
            return

    cursor.execute("INSERT INTO tasks (user_id, text, deadline) VALUES (?, ?, ?)",
                   (user_id, task_text, deadline.strftime('%m-%d %H:%M')))
    conn.commit()

    await message.answer(f"Задача добавлена: {task_text}\nДедлайн: {deadline.strftime('%m-%d %H:%M')}")
    await state.clear()


@dp.message(F.text == "Список задач")
@dp.message(Command("tasks"))
async def list_tasks(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT id, text FROM tasks WHERE user_id = ?", (user_id,))
    tasks = cursor.fetchall()
    if not tasks:
        await message.answer("У вас нет задач.")
        return
    await message.answer("Ваши задачи:", reply_markup=get_tasks_markup(user_id))


@dp.message(F.text == "Удалить задачу")
async def delete_task_list(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT id, text FROM tasks WHERE user_id = ?", (user_id,))
    tasks = cursor.fetchall()
    if not tasks:
        await message.answer("У вас нет задач для удаления.")
        return
    await message.answer("Выберите задачу для удаления:", reply_markup=get_tasks_with_delete_markup(user_id))


@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    action, task_id = callback.data.split("_")

    if action == "view":
        cursor.execute(
            "SELECT text, deadline FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        task = cursor.fetchone()
        if task:
            await callback.message.answer(f"{task[0]}\n Дедлайн: {task[1]}")
        else:
            await callback.message.answer("Задача не найдена.")
    elif action == "delete":
        cursor.execute(
            "DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        conn.commit()
        await callback.message.answer("Задача удалена.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.create_task(send_notifications())
    loop.create_task(dp.start_polling(bot))
    loop.run_forever()
