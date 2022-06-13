from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movielist")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', movielist=data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        Title = request.form['Title']
        Release_Date = request.form['Release_Date']
        Genre = request.form['Genre']
        Price = request.form['Price']
        Rating = request.form['Rating']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO movielist (Title, Release_Date, Genre, Price, Rating) VALUES (%s, %s, %s, %s, %s)", (Title, Release_Date, Genre, Price, Rating))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM movielist WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        Title = request.form['Title']
        Release_Date = request.form['Release_Date']
        Genre = request.form['Genre']
        Price = request.form['Price']
        Rating = request.form['Rating']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE movielist SET Title=%s, Release_Date=%s, Genre=%s, Price=%s, Rating=%s
        WHERE id=%s
        """, (Title, Release_Date, Genre, Price, Rating, id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))




if __name__ == "__main__":
    app.run(debug=True)