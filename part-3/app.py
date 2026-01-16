"""
Part 3: Flask-SQLAlchemy ORM
============================
Say goodbye to raw SQL! Use Python classes to work with databases.

What You'll Learn:
- Setting up Flask-SQLAlchemy
- Creating Models (Python classes = database tables)
- ORM queries instead of raw SQL
- Relationships between tables (One-to-Many)

Prerequisites: Complete part-1 and part-2
Install: pip install flask-sqlalchemy
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =============================================================================
# MODELS
# =============================================================================

# Teacher Model
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    courses = db.relationship('Course', backref='teacher', lazy=True)

    def __repr__(self):
        return f'<Teacher {self.name}>'

# Course Model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)

    students = db.relationship('Student', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.name}>'

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'

# =============================================================================
# ROUTES
# =============================================================================

# ---------------- STUDENTS ----------------
@app.route('/')
def index():
    students = Student.query.order_by(Student.name).all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student = Student(
            name=request.form['name'],
            email=request.form['email'],
            course_id=request.form['course_id']
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))

    courses = Course.query.all()
    return render_template('add.html', courses=courses)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.course_id = request.form['course_id']
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('index'))

    courses = Course.query.all()
    return render_template('edit.html', student=student, courses=courses)

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'danger')
    return redirect(url_for('index'))

# ---------------- COURSES ----------------
@app.route('/courses')
def courses():
    all_courses = Course.query.limit(10).all()
    return render_template('courses.html', courses=all_courses)

@app.route('/add-course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course = Course(
            name=request.form['name'],
            description=request.form['description'],
            teacher_id=request.form['teacher_id']
        )
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully!', 'success')
        return redirect(url_for('courses'))

    teachers = Teacher.query.all()
    return render_template('add_course.html', teachers=teachers)

# ---------------- TEACHERS ----------------
@app.route('/teachers')
def teachers():
    teacher_list = Teacher.query.filter(Teacher.name.like('%a%')).all()
    return render_template('teachers.html', teachers=teacher_list)

# ✅ ADD TEACHER + COURSE TOGETHER
@app.route('/add-teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':

        # 1️⃣ Create Teacher
        teacher = Teacher(
            name=request.form['teacher_name'],
            email=request.form['teacher_email']
        )
        db.session.add(teacher)
        db.session.commit()   # get teacher.id

        # 2️⃣ Create Course for that Teacher
        course = Course(
            name=request.form['course_name'],
            description=request.form['course_description'],
            teacher_id=teacher.id
        )
        db.session.add(course)
        db.session.commit()

        flash('Teacher and Course added successfully!', 'success')
        return redirect(url_for('teachers'))

    return render_template('add_teacher.html')

@app.route('/edit-teacher/<int:id>', methods=['GET', 'POST'])
def edit_teacher(id):
    teacher = Teacher.query.get_or_404(id)

    if request.method == 'POST':
        teacher.name = request.form['name']
        teacher.email = request.form['email']
        db.session.commit()
        flash('Teacher updated successfully!', 'success')
        return redirect(url_for('teachers'))

    return render_template('edit_teacher.html', teacher=teacher)

@app.route('/delete-teacher/<int:id>')
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    flash('Teacher deleted successfully!', 'danger')
    return redirect(url_for('teachers'))

# =============================================================================
# DATABASE INITIALIZATION
# =============================================================================
def init_db():
    with app.app_context():
        db.create_all()

        if Teacher.query.count() == 0:
            t1 = Teacher(name='Dr. Sharma', email='sharma@gmail.com')
            t2 = Teacher(name='Prof. Mehta', email='mehta@gmail.com')
            db.session.add_all([t1, t2])
            db.session.commit()

        if Course.query.count() == 0:
            courses = [
                Course(name='Python Basics', description='Intro to Python', teacher_id=1),
                Course(name='Web Development', description='Flask & Web', teacher_id=2),
                Course(name='Data Science', description='Data Analysis', teacher_id=1),
            ]
            db.session.add_all(courses)
            db.session.commit()

# =============================================================================
# RUN APP
# =============================================================================
if __name__ == '__main__':
    init_db()
    app.run(debug=True)




# =============================================================================
# ORM vs RAW SQL COMPARISON:
# =============================================================================
#
# Operation      | Raw SQL                          | SQLAlchemy ORM
# ---------------|----------------------------------|---------------------------
# Get all        | SELECT * FROM students           | Student.query.all()
# Get by ID      | SELECT * WHERE id = ?            | Student.query.get(id)
# Filter         | SELECT * WHERE name = ?          | Student.query.filter_by(name='John')
# Insert         | INSERT INTO students VALUES...   | db.session.add(student)
# Update         | UPDATE students SET...           | student.name = 'New'; db.session.commit()
# Delete         | DELETE FROM students WHERE...    | db.session.delete(student)
#
# =============================================================================
# COMMON QUERY METHODS:
# =============================================================================
#
# Student.query.all()                    - Get all records
# Student.query.first()                  - Get first record
# Student.query.get(1)                   - Get by primary key
# Student.query.get_or_404(1)            - Get or show 404 error
# Student.query.filter_by(name='John')   - Filter by exact value
# Student.query.filter(Student.name.like('%john%'))  - Filter with LIKE
# Student.query.order_by(Student.name)   - Order results
# Student.query.count()                  - Count records
#
# =============================================================================


# =============================================================================
# EXERCISE:
# =============================================================================
#
# 1. Add a `Teacher` model with a relationship to Course
# 2. Try different query methods: `filter()`, `order_by()`, `limit()`
#
# =============================================================================
