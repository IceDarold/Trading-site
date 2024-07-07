from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from flask import render_template
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)
CORS(app)


@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/services')
def services():
    return render_template("services.html")

@app.route('/contact')
def contact():
    return render_template("contact.html") 

@app.route('/')
def main():
    return redirect(url_for('home'))

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    print(f"Имя: {name}")
    print(f"Email: {email}")
    print(f"Сообщение: {message}")

    return jsonify({'message': 'ХАХАХАХАХ ТЕПЕРЬ ВАШИ ДАННЫЕ У НАС ЫЫЫЫ!'})

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)

@app.route('/plotly')
def index():
    # Пример данных
    df = px.data.iris()  # Загрузка набора данных iris

    # Создание графика
    fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species',
                     title='Iris Dataset')

    # Конвертация графика в JSON
    graphJSON = pio.to_json(fig)

    return render_template('draw_plot.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
