from flask import Flask, render_template, session, flash, request
import sqlite3 as sql

app = Flask(__name__)
                
@app.route("/")
def root():
    session["logged_in"] = False
    session['name'] = ""
    return index()

@app.route("/index")
def index():
    #session['logged_in'] = False
    #session['name'] = ""
    con = sql.connect("ForumPosts.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute("ATTACH DATABASE 'PostComments.db' AS PostCommentsDB")
    cur.execute('''
        SELECT ForumPost.*, COUNT(PostComment.CommentId) AS CommentCount
        FROM ForumPost
        LEFT JOIN PostComment ON ForumPost.PostId = PostComment.PostId
        GROUP BY ForumPost.PostId
    ''') 

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

    return index()


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

            sql_select_query = """select * from ForumUser WHERE\
                Username = ? and Password = ?"""
            cur.execute(sql_select_query, (nm,pw))

            row = cur.fetchone()

            if (row != None):
                session['logged_in'] = True
                session['name'] = row['Username']
            else:
                # i think this session declaration is redundant now- SV
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
    # add a flash message that says you must be logged in to upvote or something
    if session['logged_in'] == True:
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
    if session['logged_in'] == True:
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

@app.route("/profile")
def profile():
    foo = request.args.get('posted_by')
    if foo != session['name']:
        nm = foo
    else:
        nm = session['name']

    con = sql.connect("ForumPosts.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    sql_select_query = """select * from ForumPost WHERE\
        PostedBy = ?"""
    cur.execute(sql_select_query, (nm,))
    posts = cur.fetchall()
    con.close()

    return render_template('profile.html',
            postedBy = nm, name = session['name'], posts=posts)

@app.route("/create-post")
def create_post():
    if session['logged_in'] == True:
        return render_template("create_post.html")
    else:
        return index()

@app.route("/create-post-submit", methods =['POST'])
def create_post_submit():
    title = request.form['post-title'] 
    postedBy = session['name']
    content = request.form['post-content']
    subforum = request.form['subforum']

    con = sql.connect("ForumPosts.db")
    cur = con.cursor()
    cur.execute("INSERT INTO ForumPost (PostedBy, PostTitle, PostContent, PostSubForum, Upvotes, Downvotes) VALUES(?,?,?,?,?,?)"
                ,(postedBy, title, content, subforum, 0, 0))
    con.commit()
    return index()

@app.route("/on-select-change", methods=["POST"])
def on_select_change():
    subforum = request.form['subforum']
    con = sql.connect("ForumPosts.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("ATTACH DATABASE 'PostComments.db' AS PostCommentsDB")

    if subforum == "all":
        cur.execute('''
            SELECT ForumPost.*, COUNT(PostCommentsDB.PostComment.CommentId) AS CommentCount
            FROM ForumPost
            LEFT JOIN PostCommentsDB.PostComment ON ForumPost.PostId = PostCommentsDB.PostComment.PostId
            GROUP BY ForumPost.PostId
        ''')
    else:
        sql_select_query = '''
            SELECT ForumPost.*, COUNT(PostCommentsDB.PostComment.CommentId) AS CommentCount
            FROM ForumPost
            LEFT JOIN PostCommentsDB.PostComment ON ForumPost.PostId = PostCommentsDB.PostComment.PostId
            WHERE ForumPost.PostSubForum = ?
            GROUP BY ForumPost.PostId
        '''
        cur.execute(sql_select_query, (subforum,))

    posts = cur.fetchall()

    con.close()
    return render_template('index.html', posts=posts, selected_subforum=subforum)

@app.route("/post")
def post():
    id = request.args.get('post_id')

    con = sql.connect("ForumPosts.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    sql_select_query = """select * from ForumPost WHERE\
        PostId = ?"""
    cur.execute(sql_select_query, (id,))
    post = cur.fetchone()
    con.close()

    postDict = None
    if post:
        postDict = {
            "postId": post[0],
            "postedBy": post[1],
            "title": post[2],
            "content": post[3],
            "subforum": post[4]
        }

    con = sql.connect("PostComments.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    sql_select_query = """select * from PostComment where\
        PostId = ?"""
    cur.execute(sql_select_query, (id,))
    comments = cur.fetchall()
    print(comments)
    con.close()

    return render_template('post.html',
            postDict = postDict, comments=comments )

@app.route("/comment-submit", methods=['POST'])
def comment_submit():
    #if logged in and the comment isn't empty
    if session['logged_in'] and request.form["comment-content"]:
        con = sql.connect("PostComments.db")
        cur = con.cursor()
        id = request.args.get("post_id")
        content = request.form["comment-content"]
        commentedBy = session["name"]
        cur.execute("insert into PostComment (PostId, CommentContent,CommentedBy) VALUES (?, ?, ?)"
                    ,(id, content,commentedBy)) 
        con.commit()
        con.close()
        return post()
    else:
        #you must be logged in to submit comment flashA
        flash("You have to be logged in to comment!")
        return post() 

if __name__ == "__main__":
    # TT: secret key needs to be set to avoid error at runtime
    # TODO probably should be randomized?
    app.secret_key = 'secretKey'
    app.run(debug=True)
