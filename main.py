from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

DATABASE = 'Full_Stack_Database.db'
 
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn
 
# Create tables if they do not exist
with get_db_connection() as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS organization_table
                 (Org_id INTEGER PRIMARY KEY,
                 Org_name TEXT NOT NULL,
                 API_KEY TEXT NOT NULL)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS agency_table
                 (Org_id INTEGER,
                 Agency_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                 Agency_name TEXT NOT NULL,
                 Agency_email TEXT NOT NULL,
                 FOREIGN KEY (Org_id) REFERENCES organization_table(Org_id))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS user_table
                 (Org_id INTEGER,
                 Emp_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                 Access_level TEXT NOT NULL,
                 User_name TEXT NOT NULL UNIQUE,
                 Password TEXT NOT NULL,
                 IsAdmin TEXT NOT NULL,
                 Application TEXT NOT NULL,
                 FOREIGN KEY (Org_id) REFERENCES organization_table(Org_id))''')
    conn.commit()
 
@app.route('/insert_organization', methods=['POST'])
def insert_organization():
    Org_name = request.form.get('Org_name')
    API_KEY = request.form.get('API_KEY')
    Org_id = request.form.get('Org_id')
    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO organization_table (Org_id, Org_name, API_KEY) VALUES (?, ?, ?)", (Org_id, Org_name, API_KEY))
            conn.commit()
        return jsonify({"message": "Inserted into organization_table"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route('/insert_agency', methods=['POST'])
def insert_agency():
    Org_id = request.form.get('Org_id')
    Agency_name = request.form.get('Agency_name')
    Agency_email = request.form.get('Agency_email')
    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO agency_table (Org_id, Agency_name, Agency_email) VALUES (?, ?, ?)", (Org_id, Agency_name, Agency_email))
            conn.commit()
        return jsonify({"message": "Inserted into agency_table"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route('/insert_user', methods=['POST'])
def insert_user():
    Org_id = request.form.get('Org_id')
    Access_level = request.form.get('Access_level')
    User_name = request.form.get('User_name')
    Password = request.form.get('Password')
    IsAdmin = request.form.get('IsAdmin')
    Application = request.form.get('Application')
    print(Org_id)
    print(Access_level)
    print(User_name)
    print(Password)
    print(Application)
    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO user_table (Org_id, Access_level, User_name, Password, IsAdmin, Application) VALUES (?, ?, ?, ?, ?, ?)", (Org_id, Access_level, User_name, Password, IsAdmin, Application))
            conn.commit()
        return jsonify({"message": "Inserted into user_table"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route('/login', methods=['POST'])
def select_user_by_credentials():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_table WHERE User_name = ? AND Password = ?", (username, password))
        rows = cursor.fetchall()
        conn.close()
        users = []
        for row in rows:
            user = dict(row)
            users.append(user)
        if users:
            return jsonify({"users": users}), 200
        else:
            return jsonify({"message": "No user found with provided credentials"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)