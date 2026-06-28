from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from collections import defaultdict

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

    # Calculate weekly on-time percentage
    weekly_data = defaultdict(lambda: {'on_time': 0, 'late': 0})
    for a in assignments:
        if a['done'] and a['completed_date']:
            completed = datetime.strptime(a['completed_date'], '%Y-%m-%d').date()
            deadline = datetime.strptime(a['deadline'], '%Y-%m-%d').date()
            week_label = completed.strftime('%Y-W%U')

            if completed <= deadline:
                weekly_data[week_label]['on_time'] += 1
            else:
                weekly_data[week_label]['late'] += 1

    labels = sorted(weekly_data.keys())
    percentages = []
    for week in labels:
        total = weekly_data[week]['on_time'] + weekly_data[week]['late']
        pct = (weekly_data[week]['on_time'] / total * 100) if total > 0 else 0
        percentages.append(round(pct, 1))

    return render_template('index.html', assignments=assignments, labels=labels, percentages=percentages)

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
    app.run(debug=True, port=5001)