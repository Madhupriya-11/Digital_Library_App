from flask import Flask, render_template, request, redirect, url_for
from database import get_all_notes, get_all_qna, add_question, init_db, seed_data

app = Flask(__name__)

# Initialize and seed database on startup
init_db()
seed_data()

@app.route('/')
def index():
    notes = get_all_notes()
    qna_list = get_all_qna()
    return render_template('index.html', notes=notes, qna=qna_list)

@app.route('/add_doubt', methods=['POST'])
def add_doubt():
    question = request.form.get('question')
    author = request.form.get('author', 'Anonymous')
    if question:
        add_question(question, author)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)