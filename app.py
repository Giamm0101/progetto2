from flask import Flask, render_template, request, redirect, url_for
import csv
import mysql.connector


app = Flask(__name__)
app.config.from_object('config.Config')

def create_db_connection():
    db_config = {
        'host': app.config['MYSQL_HOST'],
        'user': app.config['MYSQL_USER'],
        'password': app.config['MYSQL_PASSWORD'],
        'database': app.config['MYSQL_DB']
    }
    return mysql.connector.connect(**db_config)

def execute_query(query, params=None):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def inserisci_dati(query, params=None):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()



@app.route('/')
def home():
    bottoni = {
        'b1': 'film',
        'b2': 'music',
        'b3': 'book',
    }
    return render_template('home.html', titolo='MediApp'.upper(), bottoni=bottoni)

@app.route('/book')
def book():
    books = execute_query('SELECT * FROM book')
    return render_template('book.html', books=books)

@app.route('/api/book')
def api_book():
    books = execute_query('SELECT * FROM book')
    return books

@app.route('/api/book/<publisher>') #Questo parametro messo tra le <> è un Query Params.
def api_book_search(publisher):
    books = execute_query('SELECT * FROM book WHERE publisher = %s', (publisher,))
    return books

@app.route('/api/book2') #Query String
def api_book_search2():
    publisher = request.args.get('publisher')
    genre = request.args.get('genre')
    id = request.args.get('id')

    sql = "SELECT * FROM book WHERE 1=1"
    params = []
    if publisher:
        sql += " AND publisher = %s"
        params.append(publisher)
    if genre:
        sql += ' AND genre = %s'
        params.append(genre)
    if id:
        sql += ' AND id = %s'
        params.append(id)
    books = execute_query(sql, params=tuple(params))
    return books

@app.route('/add_book', methods=['GET'])
def add_book():
    return render_template('add_book.html')

@app.route('/submit_book', methods=['POST'])
def submit_book():
    # Ottenere i dati dal form
    title = request.form['title']
    author = request.form['author']
    genre = request.form['genre']
    publisher = request.form['publisher']
    year = request.form['year']
    sql = "INSERT INTO book (title, author, genre, publisher, year) VALUES (%s, %s, %s, %s, %s)"
    inserisci_dati(sql, (title, author, genre, publisher, year))
    return redirect(url_for('book'))

@app.route('/delete_book', methods=['GET'])
def delete_book():
    return render_template('delete_book.html')

@app.route('/delete_data', methods=['POST'])
def delete_data():
    # Ottenere i dati dal form
    id = request.form['id_']
    sql = "DELETE FROM book WHERE id = %s"
    inserisci_dati(sql, (id,))
    return redirect(url_for('book'))

@app.route('/delete_data2/<id>')
def delete_data2(id):
    # Ottenere i dati dal form
    sql = "DELETE FROM book WHERE id = %s"
    inserisci_dati(sql, (id,))
    print('eliminato id: ', id)
    return redirect(url_for('book'))

@app.route('/user')
def user():
    users = execute_query('SELECT * FROM user')
    return render_template('user.html', users=users)

@app.route('/api/user')
def api_user():
    users = execute_query('SELECT * FROM user')
    return users

if __name__ == '__main__':
    app.run(debug=True)