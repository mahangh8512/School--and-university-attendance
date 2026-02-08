import sqlite3

def init_db():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS grade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS major (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade_id INTEGER,
            UNIQUE(name, grade_id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            father_name TEXT,
            father_phone TEXT,
            mother_phone TEXT,
            student_code TEXT,
            grade_id INTEGER,
            major_id INTEGER,
            FOREIGN KEY(grade_id) REFERENCES grade(id),
            FOREIGN KEY(major_id) REFERENCES major(id)
        )
    ''')
    # Ensure mother_phone column exists for older DBs
    c.execute("PRAGMA table_info(students)")
    cols = [r[1] for r in c.fetchall()]
    if 'mother_phone' not in cols:
        try:
            c.execute('ALTER TABLE students ADD COLUMN mother_phone TEXT')
        except Exception:
            # Some SQLite versions may not allow ALTER in certain states; ignore if fails
            pass
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            date TEXT,
            status TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    ''')
    # Ensure grade rows for 10,11,12 exist so UI can rely on them
    try:
        for g in ("10", "11", "12"):
            c.execute("INSERT OR IGNORE INTO grade (name) VALUES (?)", (g,))
    except Exception:
        pass

    # If older DB had major table without grade_id, try to add the column
    try:
        c.execute("PRAGMA table_info(major)")
        major_cols = [r[1] for r in c.fetchall()]
        if 'grade_id' not in major_cols:
            try:
                c.execute('ALTER TABLE major ADD COLUMN grade_id INTEGER')
            except Exception:
                pass
    except Exception:
        pass
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
