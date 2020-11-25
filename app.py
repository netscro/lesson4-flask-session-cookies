from flask import Flask, render_template, request, make_response, session

app = Flask(__name__)
app.secret_key = b'askdjfhaskdjhf23423409809#$#$%^&sdkjfsdkjlfncvc123'


@app.route('/')
def index():
    """
    Home page. Prints the username and the number of page visit counter.
    :return: how many times the user has opened the page
    and which user has authorized on the site (added to the session)
    """
    # вывод имени пользователя на главной странице в зависимости от наличия Сессии
    if session.get('username'):
        username = session['username']
    else:
        username = 'Anonymous'
    # # счетчик посетителей
    counter = 0

    if request.cookies.get('visitor'):
        counter = int(request.cookies['visitor'])
    # переменная вывода строки первого посещения и общего кол-ва посещений страницы
    if counter == 0:
        counter_on_page = 'visited this site first time'
    else:
        counter_on_page = f"opened this page {counter} times"
    # конец переменной вывода
    # выводим страницу основного шаблона
    response = make_response(render_template('index.html', username=username, visit=counter_on_page))
    response.set_cookie('visitor', str(counter + 1))
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login page.
    :return: Username input field and authorized username
    """
    # проверяем на наличие Сессии пользователя
    if session.get('username'):
        username = session['username']
        return render_template('logged-user.html', username=username)

    # проверяем на GET запрос
    elif request.method == 'GET':
        return """
             <form action='http://localhost:5000/login', method='POST'>
                 <input name="username">
                 <input type="submit">
             </form>
            """
    # проверяем на POST запрос
    elif request.method == 'POST':
        username = request.form['username']
        # добавляем сессию пользователю
        session['username'] = username
        return make_response(render_template('logged-user.html', username=username))


@app.route('/logout')
def logout():
    """
    User logout page.
    :return: Deletes cookies and user session (page visit counter)
    """
    logout_user = make_response('<h1>Your session is clear</h1>')
    # удаляем Cookies пользователя
    logout_user.set_cookie('visitor', '', 0)
    # удаляем сессию (обнуляем счетчик поситителей)
    session.pop('username', None)
    return logout_user


if __name__ == '__main__':
    app.run(debug=True)
