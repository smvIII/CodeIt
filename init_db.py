import sqlite3
import string, base64
import sys

def main():

    conn = sqlite3.connect('ForumUsers.db')
    cur = conn.cursor()

    confirm = 0
    while(confirm == 0):
        foo = input('CAUTION! Running this script will delete database entries, do you wish to proceed? (y/n)\n')
        if foo == 'Y' or foo == 'y':
            confirm = 1
        else:
            sys.exit()

    #drop previous table if it already exists
    try:
        cur.execute('DROP TABLE IF EXISTS ForumUser')
        conn.commit()
        print("ForumUser table dropped.")
    except:
        print("The table did not exist.")

    cur.execute('''CREATE TABLE ForumUser(
        UserId INTEGER PRIMARY KEY NOT NULL,
        Username TEXT NOT NULL,
        Password TEXT NOT NULL,
        EmailAddress TEXT NOT NULL,
        IsAdmin TEXT NOT NULL
    )''')

    conn.commit()
    print("ForumUser table created.")

    forumAdmins = [(1, 'SVossler', 'password', 'none@none.com', 1),
                     (2, 'TThompson','password', 'none@none.com' , 1),
                     (3, 'DClemente', 'password', 'none@none.com', 1),
                     (4, 'JScarff', 'password', 'none@none.com', 1)]

    cur.executemany('INSERT INTO ForumUser VALUES (?, ?, ?, ?, ?)', forumAdmins)
    conn.commit()
    conn.close()

    #create post database
    conn = sqlite3.connect('ForumPosts.db')
    cur = conn.cursor()

    try:
        cur.execute('DROP TABLE IF EXISTS ForumPost')
        conn.commit()
        print("ForumPost table dropped.")
    except:
        print("The table did not exist.")

    cur.execute('''CREATE TABLE ForumPost(
        PostId INTEGER PRIMARY KEY NOT NULL,
        PostedBy TEXT NOT NULL,
        PostTitle TEXT NOT NULL,
        PostContent TEXT NOT NULL,
        PostSubForum TEXT NOT NULL,
        Upvotes INTEGER NOT NULL,
        Downvotes INTEGER NOT NULL
    )''')

    conn.commit()
    conn.close()
    print("ForumPost table created.")

    conn = sqlite3.connect("PostComments.db")
    cur = conn.cursor()

    try:
        cur.execute('DROP TABLE IF EXISTS PostComment')
        conn.commit()
        print("PostComment table dropped.")
    except:
        print("The table did not exist.")

    cur.execute('''CREATE TABLE PostComment(
                CommentId INTEGER PRIMARY KEY NOT NULL,
                PostId INTEGER NOT NULL,
                CommentContent TEXT NOT NULL,
                CommentedBy TEXT NOT NULL,
                FOREIGN KEY (PostId) REFERENCES ForumPost(PostId)
    )''')
    conn.commit()
    conn.close()
    print("PostComment tabled created.")

    conn = sqlite3.connect("ForumPosts.db")
    cur = conn.cursor()

    content1 = "Hi everyone,<br><br>I'm new to C++ and currently working on a project where I need to declare a class called Student. However, I'm encountering some issues and would really appreciate your help.<br><br>Here's what I've tried so far:<br><br>class Student {<br> public:<br> string name;<br> int age;<br> double gpa;<br>};<br>The compiler keeps throwing errors about string not being recognized. Also, I'm not sure if I'm correctly declaring the member variables and if my syntax is right. I'm using Visual Studio Code as my IDE, if that matters.<br><br>Can someone please explain what I'm doing wrong here and how to properly declare this class? Also, any tips for a beginner on class declaration in C++ would be greatly appreciated!"
    content2 = "Hello everyone,<br><br>I'm new to programming and recently started learning JavaScript. I've been going through some tutorials but I'm finding it a bit challenging to grasp some concepts. Could anyone recommend any resources that are beginner-friendly?<br><br>Specifically, I'm struggling with understanding functions and asynchronous programming. I've heard about promises and async/await but they're going over my head. Are there any interactive tutorials or websites where I can practice these concepts in a structured way?<br><br>Also, any general advice on how to approach learning JavaScript for someone with no prior programming experience would be greatly appreciated!<br><br>Thanks in advance!"
    content3 = "Hey everyone,<br><br>I've recently started learning Java Swing to create GUI applications, and I'm facing some issues with using JPanel and JFrame. Although I understand the basic concepts of Java, this is my first time dealing with Swing, and I'm finding it a bit tricky.<br><br>I'm trying to create a simple application, but I'm stuck at declaring a JPanel and embedding it into a JFrame. Every time I run my code, either the panel doesn't show up at all, or it doesn't behave as I expect.<br><br>Here's a snippet of what I've tried:<br><br>JFrame frame = new JFrame();<br>JPanel panel = new JPanel();<br>frame.add(panel);<br>frame.setVisible(true);"
    content4 = "I'm working on a text processing task in Python where I need to remove a specific prefix from a string. For instance, if I have a string like \"SampleText\" and I want to remove the \"Sample\" part, so it just leaves \"Text\""

    forumStarterPosts = [(1, 'SVossler', 'Issues with Declaring a Student class in C++', content1, 'c++', 100, 74),
                         (2, 'DClemente', 'Struggling with JavaScript - Need Resources and Tips', content2, 'javascript', 61, 100),
                         (3, 'JScarff', 'Java Swing Libary Issue', content3, 'java', 4, 0),
                         (4, 'TThompson', 'Remove String Prefix in Python', content4, 'python', 1, 0)]
    
    cur.executemany('INSERT INTO ForumPost VALUES (?, ?, ?, ?, ?, ?, ?)', forumStarterPosts)
    conn.commit()
    conn.close()
main()
