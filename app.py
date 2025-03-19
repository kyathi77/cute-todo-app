# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

# Store tasks in memory (in a real app, you'd use a database)
tasks = []
categories = ["Personal", "Work", "School", "Shopping"]

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks, categories=categories)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    category = request.form.get('category')
    if task:
        tasks.append({
            'id': len(tasks),
            'title': task,
            'completed': False,
            'category': category,
            'date_added': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'priority': request.form.get('priority', 'medium')
        })
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = not tasks[task_id]['completed']
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        # Update the IDs of remaining tasks
        for i, task in enumerate(tasks):
            task['id'] = i
    return redirect(url_for('index'))

@app.route('/filter/<category>')
def filter_by_category(category):
    filtered_tasks = tasks
    if category != 'all':
        filtered_tasks = [task for task in tasks if task['category'] == category]
    return render_template('task_list.html', tasks=filtered_tasks)

if __name__ == '__main__':
    app.run(debug=True)