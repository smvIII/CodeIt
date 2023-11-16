from flask import Flask, render_template, session, flash, request
import sqlite3 as sql

app = Flask(__name__)
                
@app.route("/")
@app.route("/index")
def index():

    con = sql.connect("ForumPosts.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('select * from ForumPost')
    posts = cur.fetchall()

    if not session.get('logged_in'):
        return render_template('index.html', posts=posts)
    else:
        return render_template('index.html',
                name = session['name'], posts=posts)

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/register-submit", methods =['post'])
def register_submit():
    checks = int(0)
    msg = ""
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # add input validation and a flash message that gives a message if any given input is wrong
    # or says that user was successfully added.
    # check if username is already in the database, do not let duplicate usernames

    con = sql.connect("ForumUsers.db")
    cur = con.cursor()
    cur.execute("INSERT INTO ForumUser (Username, Password, EmailAddress, IsAdmin) VALUES(?,?,?,?)"
                ,(username, password, email, 0))
    con.commit()

    return render_template('index.html')

#app.route("/post-submit") when posts are created and submitted

@app.route("/login-clicked")
def login_clicked():
    return render_template('login.html')

@app.route("/login", methods = ['POST'])
def login():
    try:
        nm = request.form['username']
        pw = request.form['password']

        with sql.connect("ForumUsers.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            sql_select_query = """select * from ForumUser where\
                Username = ? and Password = ?"""
            cur.execute(sql_select_query, (nm,pw))

            row = cur.fetchone()

            if (row != None):
                session['logged_in'] = True
                session['name'] = row['Username']
            else:
                session['logged_in'] = False
                flash('invalid username or password')
                return render_template('login.html')

    except:
        con.rollback()
        flash("Error")
    finally:
        con.close()
    return index()

@app.route("/logout")
def logout():
    
    session['logged_in'] = False
    session['name'] = ""

    return index()

@app.route("/upvote-clicked")
def upvote_clicked():
    #if logged in, also need a toggle function to keep track of if it has already been upvoted
    post_id = request.args.get('post_id')

    conn = sql.connect("ForumPosts.db")
    cur = conn.cursor()

    cur.execute("SELECT Upvotes FROM ForumPost WHERE PostId = ?", (post_id,))
    upvotes = cur.fetchone()[0] + 1

    cur.execute("UPDATE ForumPost SET Upvotes = ? WHERE PostId = ?", (upvotes, post_id))
    postId = request.args.get('post_id')

    conn.commit()
    conn.close()
    return index()

@app.route("/downvote-clicked")
def downvote_clicked():
    post_id = request.args.get('post_id')

    conn = sql.connect("ForumPosts.db")
    cur = conn.cursor()

    cur.execute("SELECT Downvotes FROM ForumPost WHERE PostId = ?", (post_id,))
    downvotes = cur.fetchone()[0] + 1

    cur.execute("UPDATE ForumPost SET Downvotes = ? WHERE PostId = ?", (downvotes, post_id))
    postId = request.args.get('post_id')

    conn.commit()
    conn.close()
    return index()

if __name__ == "__main__":
    # TT: secret key needs to be set to avoid error at runtime
    # TODO probably should be randomized?
    app.secret_key = 'secretKey'
    app.run(debug=True)