import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    with sqlite3.connect('todo.db3') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0,
                position INTEGER NOT NULL DEFAULT 0,
                due_date TEXT
            )
        """)
        conn.commit()
        
init_db()

# Home page route
@app.route('/')
def index():
    conn = sqlite3.connect('todo.db3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos ORDER BY position ASC")
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Route for adding task
@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        conn = sqlite3.connect('todo.db3')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO todos (task) VALUES (?)', (task,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

# Route for marking task as done
@app.route('/done/<int:id>')
def done(id):
    conn = sqlite3.connect('todo.db3')
    cursor = conn.cursor()
    cursor.execute('UPDATE todos SET done = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Route for deleting task
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('todo.db3')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM todos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route("/save-order", methods=["POST"])
def save_order():
    data = request.get_json()
    order = data.get("order", [])  # This is a list of task IDs in the new order

    if not order:
        return {"success": False, "message": "Invalid order"}, 400

    # Example: Reordering the database based on the new order
    try:
        with sqlite3.connect("todo.db3") as conn:
            cursor = conn.cursor()

            # Update the database with the new order
            for index, task_id in enumerate(order):
                cursor.execute("UPDATE todos SET position = ? WHERE id = ?", (index, task_id))

            conn.commit()
        return {"success": True}
    except Exception as e:
        print("Error saving order:", e)
        return {"success": False, "message": "Server error"}, 500
    
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = sqlite3.connect("todo.db3")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, due_date FROM todos")
    tasks = [
        {"id": row[0], "title": row[1], "due_date": row[2]} 
        for row in cursor.fetchall()
    ]
    conn.close()
    return {"tasks": tasks}




if __name__ == '__main__':
    app.run(debug=True)