import sqlite3
import os

class Database:
    def __init__(self, db_name='school.db'):
        self.db_name = db_name
        self.conn = None
        self.create_tables()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def create_tables(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Tabela de usuários: id, nome de usuário, senha, função (professor/aluno), email
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        # Adicionar coluna de email se não existir (para bancos de dados existentes)
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN email TEXT NOT NULL DEFAULT ""')
        except sqlite3.OperationalError:
            pass  # Coluna já existe

        # Tabela de turmas: id, nome, id_professor
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                teacher_id INTEGER,
                FOREIGN KEY (teacher_id) REFERENCES users(id)
            )
        ''')

        # Tabela de alunos: id, nome, id_turma
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                class_id INTEGER,
                FOREIGN KEY (class_id) REFERENCES classes(id)
            )
        ''')

        # Tabela de aulas: id, id_turma, data, tópico
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER,
                date TEXT NOT NULL,
                topic TEXT NOT NULL,
                FOREIGN KEY (class_id) REFERENCES classes(id)
            )
        ''')

        # Tabela de presença: id, id_aula, id_aluno, presente (0/1)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lesson_id INTEGER,
                student_id INTEGER,
                present INTEGER NOT NULL,
                FOREIGN KEY (lesson_id) REFERENCES lessons(id),
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        ''')

        # Tabela de atividades: id, id_turma, nome, caminho_arquivo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER,
                name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                FOREIGN KEY (class_id) REFERENCES classes(id)
            )
        ''')

        conn.commit()
        conn.close()

    # Métodos de usuário
    def add_user(self, username, password, role, email):
        cursor = self.connect()
        cursor.execute('INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)', (username, password, role, email))
        self.conn.commit()
        self.close()

    def get_user(self, username):
        cursor = self.connect()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        self.close()
        return user

    # Métodos de turma
    def add_class(self, name, teacher_id):
        cursor = self.connect()
        cursor.execute('INSERT INTO classes (name, teacher_id) VALUES (?, ?)', (name, teacher_id))
        self.conn.commit()
        self.close()

    def get_classes_by_teacher(self, teacher_id):
        cursor = self.connect()
        cursor.execute('SELECT * FROM classes WHERE teacher_id = ?', (teacher_id,))
        classes = cursor.fetchall()
        self.close()
        return classes

    def get_all_classes(self):
        cursor = self.connect()
        cursor.execute('SELECT * FROM classes')
        classes = cursor.fetchall()
        self.close()
        return classes

    # Métodos de aluno
    def add_student(self, name, class_id):
        cursor = self.connect()
        cursor.execute('INSERT INTO students (name, class_id) VALUES (?, ?)', (name, class_id))
        self.conn.commit()
        self.close()

    def get_students_by_class(self, class_id):
        cursor = self.connect()
        cursor.execute('SELECT * FROM students WHERE class_id = ?', (class_id,))
        students = cursor.fetchall()
        self.close()
        return students

    # Métodos de aula
    def add_lesson(self, class_id, date, topic):
        cursor = self.connect()
        cursor.execute('INSERT INTO lessons (class_id, date, topic) VALUES (?, ?, ?)', (class_id, date, topic))
        self.conn.commit()
        self.close()

    def get_lessons_by_class(self, class_id):
        cursor = self.connect()
        cursor.execute('SELECT * FROM lessons WHERE class_id = ?', (class_id,))
        lessons = cursor.fetchall()
        self.close()
        return lessons

    # Métodos de presença
    def add_attendance(self, lesson_id, student_id, present):
        cursor = self.connect()
        cursor.execute('INSERT INTO attendance (lesson_id, student_id, present) VALUES (?, ?, ?)', (lesson_id, student_id, present))
        self.conn.commit()
        self.close()

    def get_attendance_by_lesson(self, lesson_id):
        cursor = self.connect()
        cursor.execute('SELECT students.name, attendance.present FROM attendance JOIN students ON attendance.student_id = students.id WHERE attendance.lesson_id = ?', (lesson_id,))
        attendance = cursor.fetchall()
        self.close()
        return attendance

    # Métodos de atividade
    def add_atividade(self, class_id, name, file_path):
        cursor = self.connect()
        cursor.execute('INSERT INTO atividades (class_id, name, file_path) VALUES (?, ?, ?)', (class_id, name, file_path))
        self.conn.commit()
        self.close()

    def get_atividades_by_class(self, class_id):
        cursor = self.connect()
        cursor.execute('SELECT * FROM atividades WHERE class_id = ?', (class_id,))
        atividades = cursor.fetchall()
        self.close()
        return atividades

    def get_all_users(self):
        cursor = self.connect()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        self.close()
        return users

    def delete_user(self, user_id):
        cursor = self.connect()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.conn.commit()
        self.close()
