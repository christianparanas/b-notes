from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
app=Flask(__name__)

@app.route("/")
def index():
    con = sql.connect("notes.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from notes ORDER BY id DESC")
    data = cur.fetchall()

    print(data)

    return render_template("index.html", datas=data)


@app.route("/new", methods=['POST','GET'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        subject = request.form['subject']

        con = sql.connect("notes.db")
        cur = con.cursor()
        cur.execute("insert into notes(title, content, subject) values (?, ?, ?)", (title, content, subject))
        con.commit()

        flash('Note Added','success')
        return redirect(url_for("index"))

    return render_template("add_note.html")


@app.route("/edit/<string:id>", methods=['POST','GET'])
def edit(id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        subject = request.form['subject']

        con = sql.connect("notes.db")
        cur = con.cursor()
        cur.execute("update notes set title=?, content=?, subject=? where id=?", (title, content, subject, id))
        con.commit()
        flash('Note Updated','success')
        return redirect(url_for("index"))

    con = sql.connect("notes.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from notes where id = ?", (id))

    data = cur.fetchone()
    return render_template("edit_note.html", datas=data)
    
@app.route("/delete/<string:id>", methods=['GET'])
def delete(id):
    con = sql.connect("notes.db")
    cur = con.cursor()
    cur.execute("delete from notes where id=?",(id))
    con.commit()

    flash('Note Deleted','warning')
    return redirect(url_for("index"))
    
if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)