from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/clothes/')
def clothes():
    section_title = 'Одежда'
    clothes_list = [
        {
            "name": "Куртка",
            "price": 9000,
            "quantity": 10
        },
        {
            "name": "Джинсы",
            "price": 4500,
            "quantity": 20
        },
        {
            "name": "Футболка",
            "price": 1100,
            "quantity": 15
        }
    ]
    return render_template('clothes.html', section_title=section_title, clothes_list=clothes_list)


@app.route('/shoes/')
def shoes():
    section_title = 'Обувь'
    shoes_list = [
        {
            "name": "Кроссовки",
            "price": 5500,
            "quantity": 8
        },
        {
            "name": "Ботинки",
            "price": 7000,
            "quantity": 12
        },
        {
            "name": "Сандалии",
            "price": 2500,
            "quantity": 10
        }
    ]
    return render_template('shoes.html', section_title=section_title, shoes_list=shoes_list)


@app.route('/item/<name>/')
def item(name):
    section_title = name
    return render_template('item.html', section_title=section_title)


if __name__ == '__main__':
    app.run()
