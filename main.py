from flask import Flask,redirect, url_for, request, render_template
import sqlite3
from flask_wtf import FlaskForm
app = Flask(__name__)

conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users(name text, email text, password text)""")
conn.commit()



""" HTTP methods using GET and POST  """
@app.route('/login')
def auth():
    return render_template('login.html')

@app.route('/success/<email>/<password>')
def success(email, password):
    c.execute("SELECT * FROM users WHERE email = :email AND password = :password", {'email': email, 'password': password})
    for row in c.fetchall():
        return render_template('hello.html', name=row[0],email=row[1], password=row[2])



@app.route('/logininfo', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form['email']
        password = request.form['password']
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (mail, password))
        if mail == "admin@gmail.com" and password == "admin":
            return redirect(url_for('admin'))
        if len(c.fetchall()) > 0 and mail != "admin" and password != "admin":
            return redirect(url_for('success', email=mail, password=password))
        else:
            return "Invalid email or password post"
    else:
        mail = request.args.get('email')
        password = request.args.get('password')
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (mail, password))
        if mail == "admin@gmail.com" and password == "admin":
            return redirect(url_for('admin'))
        if len(c.fetchall()) > 0:
            return redirect(url_for('success', email=mail, password=password))
        else:
            return "Invalid email or password get"

@app.route('/admin')
def admin():
    c.execute("SELECT * FROM users")
    user = {"name" : [], "email" : [], "password" : []}
    for row in c.fetchall():
        user["name"].append(row[0])
        user["email"].append(row[1])
        user["password"].append(row[2])
    return render_template('admin.html', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/registerinfo', methods=['GET', 'POST'])
def registerinfo():
    if request.method == 'POST':
        print("get")
        name = request.form['name']
        mail = request.form['email']
        password = request.form['password']
        c.execute("SELECT * FROM users WHERE email = ?", (mail,))
        if len(c.fetchall()) > 0:
            return "Email already exists"
        else:
            print(len(c.fetchall()))
            c.execute("INSERT INTO users VALUES(?, ?, ?)", (name, mail, password))
            conn.commit()
            return redirect(url_for('auth'))
    else:
        print("post")
        name = request.args.get('name')
        mail = request.args.get('email')
        password = request.args.get('password')
        c.execute("SELECT * FROM users WHERE email = ?", (mail,))
        if len(c.fetchall()) > 0:
            return "Email already exists"
        else:
            print(len(c.fetchall()))
            c.execute("INSERT INTO users VALUES(?, ?, ?)", (name, mail, password))
            conn.commit()
            return redirect(url_for('auth'))


@app.route('/hello', methods=['POST'])
def hello():
    return "Hello Ioseb"
# page not found 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# internal server error 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, port=7777, host='0.0.0.0')