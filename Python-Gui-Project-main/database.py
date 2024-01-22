import sqlite3


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None


def setupDatabase():
    conn = create_connection("library.db")
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(
                '''CREATE TABLE IF NOT EXISTS admin (
                        name text PRIMARY KEY,
                        email text,
                        phone_number text,
                        password text NOT NULL);''')

            c.execute(
                '''CREATE TABLE IF NOT EXISTS users (
                        student_id text PRIMARY KEY,
                        name text NOT NULL);''')

            c.execute(
                '''CREATE TABLE IF NOT EXISTS books (
                        isbn text PRIMARY KEY,
                        title text NOT NULL,
                        author text,
                        genre text,
                        quantity integer NOT NULL);''')

            c.execute(
                '''CREATE TABLE IF NOT EXISTS borrowed_books (
                        id integer PRIMARY KEY,
                        user_id text NOT NULL,
                        isbn text NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (student_id),
                        FOREIGN KEY (isbn) REFERENCES books (isbn));''')
            
            add_default_admin_if_empty()

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")


def add_default_admin_if_empty():
    conn = create_connection("library.db")
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM admin")
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO admin (name, email, phone_number, password) VALUES ('admin', '555-555-5555', 'admin@admin.admin', 'admin')")
                conn.commit() 
        finally:
            conn.close()


def add_book(isbn, title, author, genre, quantity):
    conn = create_connection("library.db")
    if conn is not None:
        try:
            cur = conn.cursor()

            try:
                quantity = int(quantity)
            except ValueError:
                return "Invalid quantity: must be an integer."

            sql_check = '''SELECT title, author, genre, quantity FROM books WHERE isbn = ?'''
            cur.execute(sql_check, (isbn,))
            existing_book = cur.fetchone()

            if existing_book:
                existing_title, existing_author, existing_genre, existing_quantity = existing_book
                if (title == existing_title and author == existing_author and genre == existing_genre):

                    new_quantity = existing_quantity + quantity
                    sql_update = '''UPDATE books SET quantity = ? WHERE isbn = ?'''
                    cur.execute(sql_update, (new_quantity, isbn))
                    conn.commit()
                    return "Book quantity updated successfully."
                else:

                    return "ISBN exists, details don't match up."
            else:

                sql_insert = '''INSERT INTO books(isbn, title, author, genre, quantity) VALUES(?,?,?,?,?)'''
                cur.execute(sql_insert, (isbn, title, author, genre, quantity))
                conn.commit()
                return "Book added successfully."

        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()
    else:
        return "Error! Cannot create the database connection."


def add_user(student_id, name):
    conn = create_connection("library.db")
    if conn is not None:
        try:
            cur = conn.cursor()

            sql_check = '''SELECT name FROM users WHERE student_id = ?'''
            cur.execute(sql_check, (student_id,))
            existing_user = cur.fetchone()

            if existing_user:
                return "User with this student ID already exists."

            else:
                sql_insert = '''INSERT INTO users(student_id, name) VALUES(?,?)'''
                cur.execute(sql_insert, (student_id, name))
                conn.commit()
                return "User added successfully."

        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()
    else:
        return "Error! Cannot create the database connection."



def add_admin(name, email, phone_number, password):
    conn = create_connection("library.db")
    if conn is not None:
        try:
            cur = conn.cursor()

            sql_check = '''SELECT name FROM admin WHERE name = ?'''
            cur.execute(sql_check, (name,))
            existing_admin = cur.fetchone()

            if existing_admin:
                return "Admin with this name already exists."

            sql_insert = '''INSERT INTO admin(name, email, phone_number, password) VALUES(?,?,?,?)'''
            cur.execute(sql_insert, (name, email, phone_number, password))
            conn.commit()
            return "Admin added successfully."

        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()
    else:
        return "Error! Cannot create the database connection."



def borrow_book(user_id, isbn):
    conn = create_connection("library.db")
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT COUNT(*) FROM borrowed_books WHERE user_id = ? AND isbn = ?", (user_id, isbn))
            count = cur.fetchone()[0]

            if count > 0:
                return "User has already borrowed a copy of this book."

            available_copies = check_book_availability(isbn)
            if available_copies > 0:
                sql = '''INSERT INTO borrowed_books(user_id, isbn)
                          VALUES(?,?)'''
                cur.execute(sql, (user_id, isbn))
                conn.commit()
                return "Book borrowed successfully."
            else:
                return "Book is not available."
        except Exception as e:
            return "An error occurred."
        finally:
            conn.close()
    else:
        return "Error! Cannot create the database connection."


def return_book(user_id, isbn):
    conn = create_connection("library.db")
    if conn is not None:
        try:
            sql = '''DELETE FROM borrowed_books WHERE user_id = ? AND isbn = ?'''
            cur = conn.cursor()
            cur.execute(sql, (user_id, isbn))
            affected_rows = cur.rowcount
            conn.commit()

            if affected_rows > 0:
                return "Book returned successfully."
            else:
                return "No such borrowed book record found."
        except Exception as e:
            return "An error occurred."
        finally:
            conn.close()
    else:
        return "Error! Cannot create the database connection."


def check_book_availability(isbn):
    conn = create_connection("library.db")
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute("SELECT quantity FROM books WHERE isbn = ?", (isbn,))
            total_copies = cur.fetchone()[0]

            cur.execute(
                "SELECT COUNT(*) FROM borrowed_books WHERE isbn = ?", (isbn,))
            borrowed_copies = cur.fetchone()[0]

            available_copies = total_copies - borrowed_copies
            return available_copies
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")
        return None


def list_borrowed_books_by_user(user_id):
    conn = create_connection("library.db")
    result = []
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(
                '''SELECT b.isbn, b.title, b.author, b.genre
                      FROM borrowed_books bb
                      JOIN books b ON bb.isbn = b.isbn
                      WHERE bb.user_id = ?''', (user_id,))

            rows = cur.fetchall()
            for row in rows:
                result.append((row[0], row[1], row[2], row[3])) # isbn, title, author, genre
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()
            return result
    else:
        print("Error! Cannot create the database connection.")


def list_users_who_borrowed_book(isbn):
    conn = create_connection("library.db")
    result = []
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(
                '''SELECT u.student_id, u.name
                      FROM borrowed_books bb
                      JOIN users u ON bb.user_id = u.student_id
                      WHERE bb.isbn = ?''', (isbn,))

            rows = cur.fetchall()
            for row in rows:
                result.append((row[0], row[1]))  # student_id, name
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()
            return result
    else:
        print("Error! Cannot create the database connection.")


def list_all_admins():
    conn = create_connection("library.db")
    result = []
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(''' SELECT name, email, phone_number FROM admin''')

            rows = cur.fetchall()
            for row in rows:
                result.append((row[0], row[1], row[2])) # name, email, phone_number
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()
            return result
    else:
        print("Error! Cannot create the database connection.")

    return result


def list_all_users():
    conn = create_connection("library.db")
    result = []
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(''' SELECT student_id, name FROM users''')

            rows = cur.fetchall()
            for row in rows:
                result.append((row[0], row[1]))  # student_id, name
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()
            return result
    else:
        print("Error! Cannot create the database connection.")


def list_all_books():
    conn = create_connection("library.db")
    result = []
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(
                '''SELECT b.isbn, b.title, b.author, b.genre, b.quantity,
                    (b.quantity - IFNULL(bb.borrowed_count, 0)) as available,
                    IFNULL(bb.borrowed_count, 0) as borrowed
                FROM books b
                LEFT JOIN (SELECT isbn, COUNT(*) as borrowed_count 
                    FROM borrowed_books 
                    GROUP BY isbn) bb 
                ON b.isbn = bb.isbn''')

            rows = cur.fetchall()
            for row in rows:
                result.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6])) # isbn, title, author, genre, quantity, available, borrowed
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()
            return result


def list_borrowed_books():
    conn = create_connection("library.db")
    result = []
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(
                '''SELECT b.isbn, b.title, b.author, b.genre, COUNT(bb.isbn) as borrowed_count
                   FROM borrowed_books bb
                   JOIN books b ON bb.isbn = b.isbn
                   GROUP BY bb.isbn''')

            rows = cur.fetchall()
            for row in rows:
                result.append((row[0], row[1], row[2], row[3], row[4])) # isbn, title, author, genre, borrowed_count
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()
            return result
    else:
        print("Error! Cannot create the database connection.")


def list_users_with_borrowed_books():
    conn = create_connection("library.db")
    result = []
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(
                '''SELECT u.student_id, u.name, COUNT(bb.user_id) as borrowed_count
                   FROM borrowed_books bb
                   JOIN users u ON bb.user_id = u.student_id
                   GROUP BY bb.user_id''')

            rows = cur.fetchall()
            for row in rows:
                result.append((row[0], row[1], row[2])) # student_id, name, borrowed_count
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()
            return result
    else:
        print("Error! Cannot create the database connection.")


def list_all_borrowed():
    conn = create_connection("library.db")
    result = []
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(
                '''SELECT u.student_id, u.name, b.isbn, b.title, b.author, b.genre
                   FROM borrowed_books bb
                   JOIN users u ON bb.user_id = u.student_id
                   JOIN books b ON bb.isbn = b.isbn
                   GROUP BY bb.isbn, bb.user_id''')

            rows = cur.fetchall()
            for row in rows:
                result.append((row[0], row[1], row[2], row[3], row[4], row[5])) # student_id, name, isbn, title, author, genre
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()
            return result
    else:
        print("Error! Cannot create the database connection.")
        return None

def validate_admin(username, password):
    conn = create_connection("library.db")
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute("SELECT password FROM admin WHERE name = ?", (username,))
            result = cur.fetchone()

            if result is None:
                return "Admin does not exist!"
            elif result[0] != password:
                return "Password is incorrect!"
            else:
                return "Success"
        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error occurred."
        finally:
            conn.close()
    else:
        return "Error! Cannot create the database connection."


def delete_admin(name):
    conn = create_connection("library.db")
    if conn is not None:
        try:
            cur = conn.cursor()
            sql_delete_admin = '''DELETE FROM admin WHERE name = ?'''
            cur.execute(sql_delete_admin, (name,))
            conn.commit()
            if cur.rowcount > 0:
                return "Admin deleted successfully."
            else:
                return "No such admin found."
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()
    else:
        return "Error! Cannot create the database connection."


def delete_user(student_id):
    conn = create_connection("library.db")
    if conn is not None:
        try:
            cur = conn.cursor()
            sql_delete_borrowed = '''DELETE FROM borrowed_books WHERE user_id = ?'''
            cur.execute(sql_delete_borrowed, (student_id,))
            sql_delete_user = '''DELETE FROM users WHERE student_id = ?'''
            cur.execute(sql_delete_user, (student_id,))
            conn.commit()
            if cur.rowcount > 0:
                return "User and related records deleted successfully."
            else:
                return "No such user found."
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()
    else:
        return "Error! Cannot create the database connection."


def delete_book(isbn):
    conn = create_connection("library.db")
    if conn is not None:
        try:
            cur = conn.cursor()
            sql_delete_borrowed = '''DELETE FROM borrowed_books WHERE isbn = ?'''
            cur.execute(sql_delete_borrowed, (isbn,))
            sql_delete_book = '''DELETE FROM books WHERE isbn = ?'''
            cur.execute(sql_delete_book, (isbn,))
            conn.commit()
            if cur.rowcount > 0:
                return "Book and related records deleted successfully."
            else:
                return "No such book found."
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()
    else:
        return "Error! Cannot create the database connection."
