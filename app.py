from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
import validators
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


@app.route("/view/<string:id>", methods=['GET'])
def view(id):
    con = sql.connect("notes.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from notes where id = ?", (id))

    data = cur.fetchone()

    print(data)
    return render_template("view_note.html", datas=data)


@app.route("/new", methods=['POST','GET'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        subject = request.form['subject']
        imgLink = request.form['imageLink']
        extLink = request.form['extLink']
        youtubeLink = request.form['youtubeLink']

        youtubeLink = youtubeLink.replace("watch?v=", "embed/")

        con = sql.connect("notes.db")
        cur = con.cursor()
        cur.execute("insert into notes(title, content, subject, imgLink, extLink, youtubeLink) values (?, ?, ?, ?, ?, ?)", (title, content, subject, imgLink, extLink, youtubeLink))
        con.commit()

        flash('Note Added','success')
        return redirect(url_for("index"))

    return render_template("add_note.html")


@app.route("/edit/<string:id>", methods=['POST','GET'])
def edit(id):
    nId = id

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        subject = request.form['subject']
        imgLink = request.form['imageLink']
        extLink = request.form['extLink']
        youtubeLink = request.form['youtubeLink']

        youtubeLink = youtubeLink.replace("watch?v=", "embed/")

        if validators.url(extLink) or extLink == "":
            con = sql.connect("notes.db")
            cur = con.cursor()
            cur.execute("update notes set title=?, content=?, subject=?, imgLink=?, extLink=?, youtubeLink=? where id=?", (title, content, subject, imgLink, extLink, youtubeLink, id))
            con.commit()

            flash('Note Updated','success')
            return redirect(url_for("index"))

        else:
            flash('External Link Invalid','warning')
            return redirect(url_for("edit", id=nId))

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