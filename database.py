import sqlite3

DB_NAME = "library.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Task 1: Create notes and qna tables[span_2](start_span)[span_2](end_span)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            class_level TEXT NOT NULL,
            pdf_link TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qna (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            author TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            answer TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def seed_data():
    """Task 2: Insert sample study items into notes[span_3](start_span)[span_3](end_span)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM notes")
    if cursor.fetchone()[0] == 0:
        sample_notes = [
            ("Class 10 Science Notes", "Science", "Class 10", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"),
            ("Kannada Grammar Reference", "Kannada", "Class 9", "https://ncert.nic.in/textbook.php"),
            ("Class 8 Mathematics Formulas", "Math", "Class 8", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"),
            ("Class 10 Social Science Summary", "Social Science", "Class 10", "https://ncert.nic.in/textbook.php")
        ]
        cursor.executemany("""
            INSERT INTO notes (title, subject, class_level, pdf_link)
            VALUES (?, ?, ?, ?)
        """, sample_notes)
        conn.commit()
        
    conn.close()

# Task 3: Helper Functions for Backend Import
def get_all_notes():
    """Returns all rows from the notes table as a list of dictionaries[span_4](start_span)[span_4](end_span)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_qna():
    """Returns all questions ordered by newest first[span_5](start_span)[span_5](end_span)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qna ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_question(question, author):
    """Inserts a new doubt into the qna table[span_6](start_span)[span_6](end_span)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO qna (question, author)
        VALUES (?, ?)
    """, (question, author))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    seed_data()

def add_answer(qna_id, answer_text):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE qna SET answer = ? WHERE id = ?", (answer_text, qna_id))
    conn.commit()
    conn.close()