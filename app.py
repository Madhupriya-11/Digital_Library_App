from flask import Flask, render_template, request
import requests
import sqlite3

app = Flask(__name__)

# ---------------------------------------------------------
# ROUTE 1: Home Page & Google Books API Search
# ---------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    books = []
    
    if request.method == 'POST':
        user_query = request.form.get('search_query')
        
        if user_query:
            url = f"https://www.googleapis.com/books/v1/volumes?q={user_query}&maxResults=6"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                for item in data.get('items', []):
                    info = item.get('volumeInfo', {})
                    books.append({
                        'title': info.get('title', 'Untitled'),
                        'authors': ", ".join(info.get('authors', ['Unknown'])),
                        'link': info.get('infoLink', '#'),
                        'thumbnail': info.get('imageLinks', {}).get('thumbnail', 'https://via.placeholder.com/128x192')
                    })

    return render_template('index.html', books=books)


# ---------------------------------------------------------
# ROUTE 2: Offline Study Notes
# ---------------------------------------------------------
@app.route('/notes')
def notes():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM notes")
        all_notes = cursor.fetchall()
    except sqlite3.OperationalError:
        all_notes = []
        
    conn.close()
    return render_template('notes.html', notes=all_notes)


# ---------------------------------------------------------
# ROUTE 3: Q&A Doubt Clearing Forum
# ---------------------------------------------------------
@app.route('/qna', methods=['GET', 'POST'])
def qna():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == 'POST':
        new_question = request.form.get('question')
        author_name = request.form.get('author', 'Student')
        
        if new_question:
            cursor.execute("INSERT INTO qna (question, author) VALUES (?, ?)", (new_question, author_name))
            conn.commit()

    try:
        cursor.execute("SELECT * FROM qna ORDER BY id DESC")
        all_questions = cursor.fetchall()
    except sqlite3.OperationalError:
        all_questions = []

    conn.close()
    return render_template('qna.html', questions=all_questions)


if __name__ == '__main__':
    app.run(debug=True, port=5000)