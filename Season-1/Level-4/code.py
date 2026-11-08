import re
import sqlite3
import os
from flask import Flask, request

app = Flask(__name__)
@app.route("/")
def source():
    DB_CRUD_ops().get_stock_info(request.args["input"])
    DB_CRUD_ops().get_stock_price(request.args["input"])
    DB_CRUD_ops().update_stock_price(request.args["input"], 0.0)
    DB_CRUD_ops().exec_multi_query(request.args["input"])
    DB_CRUD_ops().exec_user_script(request.args["input"])

ALLOWED_QUERY = re.compile(r"^SELECT (price|\*) FROM stocks WHERE symbol = '([A-Za-z0-9.]{1,10})'$")

class Connect(object):

    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        return connection

class Create(object):

    def __init__(self):
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            table_fetch = cur.execute(
                '''
                SELECT name 
                FROM sqlite_master 
                WHERE type='table'AND name='stocks';
                ''').fetchall()

            if table_fetch == []:
                cur.execute(
                    '''
                    CREATE TABLE stocks
                    (date text, symbol text, price real)
                    ''')

                cur.execute(
                    "INSERT INTO stocks VALUES ('2022-01-06', 'MSFT', 300.00)")
                db_con.commit()

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

def safe_select(cur, query):
    match = ALLOWED_QUERY.match(query.strip())
    if not match:
        return None
    if match.group(1) == "price":
        cur.execute("SELECT price FROM stocks WHERE symbol = ?", (match.group(2),))
    else:
        cur.execute("SELECT * FROM stocks WHERE symbol = ?", (match.group(2),))
    return cur.fetchall()

class DB_CRUD_ops(object):

    def get_stock_info(self, stock_symbol):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] get_stock_info\n"
            query = "SELECT * FROM stocks WHERE symbol = '{0}'".format(stock_symbol)
            res += "[QUERY] " + query + "\n"

            restricted_chars = ";%&^!#-"
            has_restricted_char = any([char in query for char in restricted_chars])
            correct_number_of_single_quotes = query.count("'") == 2

            if has_restricted_char or not correct_number_of_single_quotes:
                res += "CONFIRM THAT THE ABOVE QUERY IS NOT MALICIOUS TO EXECUTE"
            else:
                cur.execute("SELECT * FROM stocks WHERE symbol = ?", (stock_symbol,))
                query_outcome = cur.fetchall()
                for result in query_outcome:
                    res += "[RESULT] " + str(result)
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

    def get_stock_price(self, stock_symbol):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] get_stock_price\n"
            match = re.match(r"[A-Za-z0-9.]{1,10}", stock_symbol)
            if not match:
                return res + "[ERROR] invalid stock symbol\n"
            stock_symbol = match.group(0)

            res += "[QUERY] SELECT price FROM stocks WHERE symbol = '" + stock_symbol + "'\n"
            cur.execute("SELECT price FROM stocks WHERE symbol = ?", (stock_symbol,))
            query_outcome = cur.fetchall()
            for result in query_outcome:
                res += "[RESULT] " + str(result) + "\n"
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

    def update_stock_price(self, stock_symbol, price):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            if not isinstance(price, float):
                raise Exception("ERROR: stock price provided is not a float")

            res = "[METHOD EXECUTED] update_stock_price\n"
            res += "[QUERY] UPDATE stocks SET price = '%d' WHERE symbol = '%s'\n" % (price, stock_symbol)

            cur.execute("UPDATE stocks SET price = ? WHERE symbol = ?", (price, stock_symbol))
            db_con.commit()
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

    def exec_multi_query(self, query):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] exec_multi_query\n"
            for part in filter(None, query.split(';')):
                res += "[QUERY]" + part + "\n"
                query_outcome = safe_select(cur, part)
                if query_outcome is None:
                    return res + "[ERROR] query not allowed\n"
                for result in query_outcome:
                    res += "[RESULT] " + str(result) + " "
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

    def exec_user_script(self, query):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] exec_user_script\n"
            res += "[QUERY] " + query + "\n"
            query_outcome = safe_select(cur, query)
            if query_outcome is None:
                return res + "[ERROR] query not allowed"
            for result in query_outcome:
                res += "[RESULT] " + str(result)
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()
