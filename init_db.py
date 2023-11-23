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
    print("ForumPost table created.")

    content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis consectetur ultrices egestas. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nam accumsan nibh vitae est porta placerat. Pellentesque lobortis risus non massa posuere, sed consectetur lorem rutrum. Sed sagittis lacus sit amet dui pharetra, quis imperdiet est aliquet. Nam id enim pretium, feugiat mauris non, sollicitudin massa. Integer fermentum magna eget eros ultricies, at venenatis augue congue. Pellentesque consectetur augue nec consequat vehicula. Donec venenatis cursus lobortis. Praesent ut arcu euismod, laoreet elit ac, facilisis nunc. Sed maximus dolor ac nunc volutpat, non iaculis turpis vehicula. Vivamus volutpat non lectus ac eleifend. Maecenas fermentum accumsan semper. Morbi cursus nec ipsum quis gravida. In hac habitasse platea dictumst. Aenean tincidunt cursus metus ac varius"
    forumStarterPosts = [(1, 'SVossler', 'ExamplePost1', content, 'python', 100, 50),
                         (2, 'SVossler', 'ExamplePost2', content, 'c++', 50, 100),
                         (3, 'SVossler', 'ExamplePost3', content, 'java', 0, 0),
                         (4, 'TThompson', 'ExamplePost4', content, 'javascript', 0, 0)]
    
    cur.executemany('INSERT INTO ForumPost VALUES (?, ?, ?, ?, ?, ?, ?)', forumStarterPosts)
    conn.commit()
    conn.close()
main()
