import sqlite3
import random

# Connect to the database
connection = sqlite3.connect("database.db")
cursor = connection.cursor()


# -----------------------------
# 1. DEPARTMENTS TABLE
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
""")


# -----------------------------
# 2. STUDENTS TABLE
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(id)
)
""")


# -----------------------------
# 3. TEACHERS TABLE
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(id)
)
""")


# -----------------------------
# 4. COURSES TABLE
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
)
""")


# -----------------------------
# 5. ENROLLMENTS TABLE
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
)
""")


# -----------------------------
# DEPARTMENT DATA
# -----------------------------

departments = [
    (1, "Computer Science"),
    (2, "Electronics"),
    (3, "Mechanical"),
    (4, "Electrical"),
    (5, "Civil"),
]

cursor.executemany("""
INSERT OR IGNORE INTO departments (id, name)
VALUES (?, ?)
""", departments)


# -----------------------------
# TEACHER DATA
# -----------------------------

teacher_names = [
    "Arun", "Maya", "Rahul", "Priya", "Vishnu",
    "Anjali", "Suresh", "Meera", "Nikhil", "Asha"
]

teachers = []

for i, name in enumerate(teacher_names, start=1):
    department_id = random.randint(1, 5)
    teachers.append((i, name, department_id))

cursor.executemany("""
INSERT OR IGNORE INTO teachers (id, name, department_id)
VALUES (?, ?, ?)
""", teachers)


# -----------------------------
# COURSE DATA
# -----------------------------

course_names = [
    "Database Systems",
    "Machine Learning",
    "Computer Networks",
    "Operating Systems",
    "Artificial Intelligence",
    "Web Development",
    "Data Science",
    "Cyber Security",
    "Cloud Computing",
    "Software Engineering"
]

courses = []

for i, name in enumerate(course_names, start=1):
    teacher_id = random.randint(1, 10)
    courses.append((i, name, teacher_id))

cursor.executemany("""
INSERT OR IGNORE INTO courses (id, name, teacher_id)
VALUES (?, ?, ?)
""", courses)


# -----------------------------
# STUDENT DATA
# -----------------------------

first_names = [
    "Anu", "Rahul", "Sara", "Arjun", "Fathima",
    "Nikhil", "Aisha", "Vishnu", "Meera", "Adil",
    "Neha", "Rohan", "Ishaan", "Diya", "Amal",
    "Sneha", "Akhil", "Maya", "Farhan", "Arya"
]

students = []

for i in range(1, 101):
    name = random.choice(first_names) + " " + str(i)
    age = random.randint(18, 24)
    department_id = random.randint(1, 5)

    students.append(
        (i, name, age, department_id)
    )

cursor.executemany("""
INSERT OR IGNORE INTO students
(id, name, age, department_id)
VALUES (?, ?, ?, ?)
""", students)


# -----------------------------
# ENROLLMENT DATA
# -----------------------------

enrollments = []

enrollment_id = 1

for student_id in range(1, 101):

    number_of_courses = random.randint(2, 5)

    selected_courses = random.sample(
        range(1, 11),
        number_of_courses
    )

    for course_id in selected_courses:

        enrollments.append(
            (enrollment_id, student_id, course_id)
        )

        enrollment_id += 1


cursor.executemany("""
INSERT OR IGNORE INTO enrollments
(id, student_id, course_id)
VALUES (?, ?, ?)
""", enrollments)


# -----------------------------
# SAVE EVERYTHING
# -----------------------------

connection.commit()

connection.close()

print("Large database created successfully!")
print("100 students added.")
print("10 courses added.")
print("10 teachers added.")
print("5 departments added.")
print(f"{len(enrollments)} enrollments added.")