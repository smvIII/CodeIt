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
        PostContent TEXT NOT NULL,
        Upvotes INTEGER NOT NULL,
        Downvotes INTEGER NOT NULL
    )''')
    conn.commit()
    print('ForumPost table created')

    conn.close()
main()
