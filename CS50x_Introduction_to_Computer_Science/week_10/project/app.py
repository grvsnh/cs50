import os
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'focusflow.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT DEFAULT 'General',
                completed INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                streak INTEGER DEFAULT 0,
                last_completed TEXT,
                target_days INTEGER DEFAULT 30,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/goals', methods=['GET', 'POST'])
def handle_goals():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.json or {}
        title = data.get('title', '').strip()
        category = data.get('category', 'General')
        if not title:
            return jsonify({"error": "Title is required"}), 400
        cursor.execute("INSERT INTO goals (title, category) VALUES (?, ?)", (title, category))
        conn.commit()
        goal_id = cursor.lastrowid
        cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
        return jsonify(dict(cursor.fetchone())), 201
    
    cursor.execute("SELECT * FROM goals ORDER BY completed ASC, id DESC")
    goals = [dict(row) for row in cursor.fetchall()]
    return jsonify(goals)

@app.route('/api/goals/<int:goal_id>', methods=['PUT', 'DELETE'])
def update_goal(goal_id):
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
        conn.commit()
        return jsonify({"success": True})
    
    data = request.json or {}
    if 'completed' in data:
        cursor.execute("UPDATE goals SET completed = ? WHERE id = ?", (int(bool(data['completed'])), goal_id))
    if 'title' in data:
        cursor.execute("UPDATE goals SET title = ? WHERE id = ?", (data['title'], goal_id))
    if 'category' in data:
        cursor.execute("UPDATE goals SET category = ? WHERE id = ?", (data['category'], goal_id))
    conn.commit()
    cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
    return jsonify(dict(cursor.fetchone()))

@app.route('/api/habits', methods=['GET', 'POST'])
def handle_habits():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.json or {}
        title = data.get('title', '').strip()
        target = int(data.get('target_days', 30))
        if not title:
            return jsonify({"error": "Title is required"}), 400
        cursor.execute("INSERT INTO habits (title, target_days) VALUES (?, ?)", (title, target))
        conn.commit()
        habit_id = cursor.lastrowid
        cursor.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
        return jsonify(dict(cursor.fetchone())), 201

    cursor.execute("SELECT * FROM habits ORDER BY id DESC")
    habits = [dict(row) for row in cursor.fetchall()]
    return jsonify(habits)

@app.route('/api/habits/<int:habit_id>/increment', methods=['POST'])
def increment_habit(habit_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
    habit = cursor.fetchone()
    if not habit:
        return jsonify({"error": "Habit not found"}), 404
        
    from datetime import date
    today_str = date.today().isoformat()
    new_streak = habit['streak'] + 1
    cursor.execute("UPDATE habits SET streak = ?, last_completed = ? WHERE id = ?", (new_streak, today_str, habit_id))
    conn.commit()
    
    cursor.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
    return jsonify(dict(cursor.fetchone()))

@app.route('/api/habits/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    return jsonify({"success": True})

@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.json or {}
        for k, v in data.items():
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (str(k), str(v)))
        conn.commit()
        
    cursor.execute("SELECT * FROM settings")
    settings_dict = {row['key']: row['value'] for row in cursor.fetchall()}
    return jsonify(settings_dict)

@app.route('/api/reset', methods=['POST'])
def reset_data():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM goals")
    cursor.execute("DELETE FROM habits")
    conn.commit()
    return jsonify({"success": True, "message": "Database reset cleanly."})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total, SUM(completed) as done FROM goals")
    goal_row = cursor.fetchone()
    total_goals = goal_row['total'] or 0
    done_goals = goal_row['done'] or 0
    
    cursor.execute("SELECT COUNT(*) as count, MAX(streak) as max_streak FROM habits")
    habit_row = cursor.fetchone()
    habit_count = habit_row['count'] or 0
    max_streak = habit_row['max_streak'] or 0
    
    return jsonify({
        "goals": {"total": total_goals, "completed": done_goals, "percent": int((done_goals / total_goals * 100) if total_goals > 0 else 0)},
        "habits": {"count": habit_count, "max_streak": max_streak}
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
