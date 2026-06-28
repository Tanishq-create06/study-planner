from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

assignments = []

@app.route('/')
def home():
    today = datetime.now().date()
    for a in assignments:
        deadline_date = datetime.strptime(a['deadline'], '%Y-%m-%d').date()
        days_left = (deadline_date - today).days
        a['days_left'] = days_left

        if a['done']:
            a['status_color'] = 'done'
        elif days_left <= 5:
            a['status_color'] = 'red'
        elif days_left <= 10:
            a['status_color'] = 'yellow'
        else:
            a['status_color'] = 'green'

    return render_template('index.html', assignments=assignments)

@app.route('/add', methods=['POST'])
def add_assignment():
    title = request.form['title']
    subject = request.form['subject']
    deadline = request.form['deadline']

    assignments.append({
        'id': len(assignments),
        'title': title,
        'subject': subject,
        'deadline': deadline,
        'done': False,
        'completed_date': None
    })
    return redirect(url_for('home'))

@app.route('/complete/<int:assignment_id>')
def complete_assignment(assignment_id):
    for a in assignments:
        if a['id'] == assignment_id:
            a['done'] = True
            a['completed_date'] = datetime.now().date().isoformat()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)