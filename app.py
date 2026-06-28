from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary in-memory storage (resets when server restarts)
assignments = []

@app.route('/')
def home():
    return render_template('index.html', assignments=assignments)

@app.route('/add', methods=['POST'])
def add_assignment():
    title = request.form['title']
    subject = request.form['subject']
    deadline = request.form['deadline']

    assignments.append({
        'title': title,
        'subject': subject,
        'deadline': deadline,
        'done': False
    })
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)