from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import time

app = Flask(__name__)
CORS(app)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://todouser:todopass@localhost:5432/todoapp')

def get_db_connection():
    """Get database connection with retry logic"""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
            return conn
        except psycopg2.OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Database connection attempt {attempt + 1} failed, retrying in 5 seconds...")
                time.sleep(5)
            else:
                raise e

def init_db():
    """Initialize database with todos table"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                task TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM todos ORDER BY created_at DESC')
        todos = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify([dict(todo) for todo in todos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos', methods=['POST'])
def add_todo():
    """Add a new todo"""
    try:
        data = request.get_json()
        task = data.get('task', '').strip()
        
        if not task:
            return jsonify({'error': 'Task cannot be empty'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            'INSERT INTO todos (task) VALUES (%s) RETURNING *',
            (task,)
        )
        
        new_todo = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify(dict(new_todo)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo (toggle completion or edit task)"""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if todo exists
        cur.execute('SELECT * FROM todos WHERE id = %s', (todo_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'error': 'Todo not found'}), 404
        
        # Update todo
        if 'completed' in data:
            cur.execute(
                'UPDATE todos SET completed = %s WHERE id = %s RETURNING *',
                (data['completed'], todo_id)
            )
        elif 'task' in data:
            task = data['task'].strip()
            if not task:
                cur.close()
                conn.close()
                return jsonify({'error': 'Task cannot be empty'}), 400
            
            cur.execute(
                'UPDATE todos SET task = %s WHERE id = %s RETURNING *',
                (task, todo_id)
            )
        else:
            cur.close()
            conn.close()
            return jsonify({'error': 'No valid fields to update'}), 400
        
        updated_todo = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify(dict(updated_todo))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('DELETE FROM todos WHERE id = %s RETURNING *', (todo_id,))
        deleted_todo = cur.fetchone()
        
        if not deleted_todo:
            cur.close()
            conn.close()
            return jsonify({'error': 'Todo not found'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Todo deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        return jsonify({'status': 'healthy'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)