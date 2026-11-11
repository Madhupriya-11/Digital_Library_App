from flask import Flask, render_template, request, redirect, url_for
from database import get_all_notes, get_all_qna, add_question, add_answer, init_db, seed_data
import sqlite3

app = Flask(__name__)

# Initialize and seed database on startup
init_db()
seed_data()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Check if a user submitted a search query
    query = request.form.get('search_query') if request.method == 'POST' else None
    
    if query:
        conn = sqlite3.connect('library.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE title LIKE ? OR subject LIKE ? OR class_level LIKE ?", 
                       (f'%{query}%', f'%{query}%', f'%{query}%'))
        notes = [dict(row) for row in cursor.fetchall()]
        conn.close()
    else:
        notes = get_all_notes()

    qna_list = get_all_qna()
    return render_template('index.html', notes=notes, qna=qna_list)

@app.route('/upload_note', methods=['POST'])
def upload_note():
    title = request.form.get('title')
    subject = request.form.get('subject')
    class_level = request.form.get('class_level')
    pdf_link = request.form.get('pdf_link')
    
    if title and subject and class_level and pdf_link:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes (title, subject, class_level, pdf_link) VALUES (?, ?, ?, ?)",
                       (title, subject, class_level, pdf_link))
        conn.commit()
        conn.close()
        
    return redirect(url_for('index'))

@app.route('/add_doubt', methods=['POST'])
def add_doubt():
    question = request.form.get('question')
    author = request.form.get('author', 'Anonymous')
    if question:
        add_question(question, author)
    return redirect(url_for('index'))
@app.route('/answer_doubt', methods=['POST'])
def answer_doubt():
    qna_id = request.form.get('qna_id')
    answer = request.form.get('answer')
    if qna_id and answer:
        add_answer(qna_id, answer)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)