"""
Задание
Создать страницу, на которой будет форма для ввода имени и электронной почты,
при отправке которой будет создан cookie-файл с данными пользователя, а также будет
произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка «Выйти», при нажатии на которую
будет удалён cookie-файл с данными пользователя и произведено
перенаправление на страницу ввода имени и электронной почты.
"""

from flask import Flask, request, make_response, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = '5a34f4d6677854f8689f470a5d35185b940b9fd6d4b986be32519e90bf020877'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        response = make_response(redirect(url_for('welcome')))
        response.set_cookie('user_name', name)
        response.set_cookie('user_email', email)
        return response
    return render_template('index.html')


@app.route('/welcome')
def welcome():
    name = request.cookies.get('user_name')
    if name:
        context = {'name': name}
        return render_template('welcome.html', **context)
    else:
        return redirect('/')


@app.route('/logout/')
def logout():
    response = make_response(redirect('/'))
    response.set_cookie('user_name', expires=0)
    response.set_cookie('user_email', expires=0)
    return response


if __name__ == '__main__':
    app.run(debug=True)
