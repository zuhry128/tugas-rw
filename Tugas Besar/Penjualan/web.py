from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import jwt
import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'praktikum'
app.secret_key= 'paladins'
mysql = MySQL(app)

@app.route('/auth')
def tokenify():
  if 'token' in session:
    return redirect(url_for('home'))

@app.route('/auth/home')
def home():
  if 'is_logged_in' and 'token' in session:   
    print(session['username']) 
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM barang")
    rv = cur.fetchall()
    return render_template("index.html", rv=rv)
  else:
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST' and 'newUserName' in request.form and 'newMail' in request.form and 'newPass' in request.form and 'newAddress' in request.form and 'newPhone' in request.form:
    username = request.form['newUserName']
    password = request.form['newPassword']
    email = request.form['newMail']
    phone = request.form['newPhone']

    cursor = mysql.connection.cursor()
    insert = "INSERT INTO user (username, password, email, telepon) VALUES (%s, %s, %s, %s)"
    values = (username, password, email, phone)
    cursor.execute(insert, values)
    mysql.connection.commit()
    print(f'data is successfully inserted')

    return redirect(url_for('login'))
  return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form['loginEmail']
    password = request.form['loginPassword']

    token = jwt.encode({'email':email, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user where email = %s and password = %s", (email, password))

    result = cursor.fetchone()

    if result:
      session['is_logged_in'] = True
      session['username'] = result[1]
      session['token'] = token
      return redirect(url_for('tokenify'))
    else:
      return render_template('login.html')

  return render_template('login.html')

@app.route('/logout')
def logout():
  session.pop('is_logged_in', None)
  session.pop('username', None)
  return redirect(url_for('login')) 

@app.route('/inputBarang', methods=['GET', 'POST'])
def inputBarang():
  if request.method == 'POST' and 'namaBarang' in request.form and 'jenisBarang' in request.form and 'jumlahBarang':
    nama_barang = request.form['namaBarang']
    jenis_barang = request.form['jenisBarang']
    jumlah_barang = request.form['jumlahBarang']

    cursor = mysql.connection.cursor()
    insert = "INSERT INTO barang (nama_barang, jenis_barang, jumlah_barang) VALUES (%s, %s, %s)"
    values = (nama_barang, jenis_barang, jumlah_barang)
    cursor.execute(insert, values)
    mysql.connection.commit()
    print(f'inventory data is successfully inserted')
  return render_template('inputBarang.html')

@app.route('/edit',  methods=['POST'])
def edit():
  id = request.form['id']
  nama = request.form['namaBarang']
  jenis = request.form['jenisBarang']
  jumlah = request.form['jumlahBarang'] 
  cur = mysql.connection.cursor()
  cur.execute("UPDATE barang SET nama_barang=%s, jenis_barang=%s, jumlah_barang=%s WHERE id=%s" , (nama, jenis, jumlah,id,))
  mysql.connection.commit()
  return redirect(url_for('home'))

@app.route('/delete/<id>',  methods=['GET'])
def delete(id):
  cur = mysql.connection.cursor()
  cur.execute("DELETE FROM barang WHERE id=%s", (id,))
  mysql.connection.commit()
  return redirect('/auth/home')
  

if __name__ == "__main__":
    app.run(debug=True)


























