import sqlite3


class db():
    def get_connection():
        conn = sqlite3.connect('database.db')
        return conn

    def put_user(username, password, contact):
        conn = get_connection()
        conn.execute(f"INSERT INTO accounts (username,password,contact) \
        VALUES ({username},{password},{contact})")
        conn.commit()
        conn.close()

    def get_user(username):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT password FROM accounts WHERE username=?", (username,))
        row = cur.fetchone()
        conn.close()
        return row

    def update_user(username, password):
        conn = get_connection()
        conn.execute(
            "UPDATE accounts set password = ? where username = ?", (password, username,))
        conn.commit()
        conn.close()

    def delete_user(username):
        conn = get_connection()
        conn.execute("DELETE from accounts where username = ?;", (username,))
        conn.commit()
        conn.close()
