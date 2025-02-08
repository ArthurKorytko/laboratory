# Лабораторна робота 25, завдання 1 Коритко Артур

from flask import Flask, render_template_string
from flask import Flask, jsonify
import requests

print(requests.get("https://jsonplaceholder.typicode.com/posts/1").json())

# Лабораторна робота 25, завдання 2 Коритко Артур


app = Flask(__name__)


@app.route("/user")
def user():
    return jsonify(name="Олександр", age=28, city="Львів")


if __name__ == "__main__":
    app.run()

# Лабораторна робота 25, завдання 3 Коритко Артур


app = Flask(__name__)


@app.route("/")
def index():
    products = ["Ноутбук", "Смартфон", "Навушники"]
    return render_template_string("<ul>{% for p in products %}<li>{{ p }}</li>{% endfor %}</ul>", products=products)


if __name__ == "__main__":
    app.run()
