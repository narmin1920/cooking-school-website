import sqlite3


def create_enrollment(student_id, session_id):
    conn = sqlite3.connect("cooking_school.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO enrollments (student_id, session_id, rating) VALUES (?, ?, ?)",
        (student_id, session_id, 0)
    )

    conn.commit()

    enrollment_id = cursor.lastrowid

    conn.close()

    return enrollment_id


def get_enrollment(student_id, session_id):

    conn = sqlite3.connect("cooking_school.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM enrollments WHERE student_id = ? AND session_id = ?",
        (student_id, session_id)
    )

    enrollment = cursor.fetchone()

    conn.close()

    return enrollment


def cancel_enrollment(student_id, session_id):

    conn = sqlite3.connect("cooking_school.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM enrollments WHERE student_id = ? AND session_id = ?",
        (student_id, session_id)
    )

    conn.commit()
    conn.close()


def get_enrollments_by_student(student_id):

    conn = sqlite3.connect("cooking_school.db")
    cursor = conn.cursor()

    cursor.execute("SELECT enrollments.id AS enrollment_id, class_session.id AS session_id, class_session.day, class_session.start_time, class_session.max_capacity, cooking_class.id AS class_id, cooking_class.title, cooking_class.cuisine, cooking_class.duration, cooking_class.chef_name, class_session.kichen AS kitchen_name FROM enrollments JOIN class_session ON enrollments.session_id = class_session.id JOIN cooking_class ON class_session.class_id = cooking_class.id WHERE enrollments.student_id = ?", (student_id,))

    enrollments = cursor.fetchall()

    conn.close()

    return enrollments


def get_enrollments_by_session(session_id):

    conn = sqlite3.connect("cooking_school.db")
    cursor = conn.cursor()

    cursor.execute("SELECT enrollments.id AS enrollment_id, users.id AS student_id, users.first_name, users.last_name, users.email FROM enrollments JOIN users ON enrollments.student_id = users.id WHERE enrollments.session_id = ?", (session_id,))

    enrollments = cursor.fetchall()

    conn.close()

    return enrollments


def count_enrollments(session_id):

    conn = sqlite3.connect("cooking_school.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM enrollments WHERE session_id = ?",
        (session_id,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def update_rating(student_id, session_id, rating):
    conn = sqlite3.connect("cooking_school.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE enrollments SET rating = ? WHERE student_id = ? AND session_id = ?", (rating, student_id, session_id))

    conn.commit()
    conn.close()

def get_class_average_rating(class_id):
    conn = sqlite3.connect("cooking_school.db")
    cursor = conn.cursor()

    cursor.execute("SELECT AVG(enrollments.rating) FROM enrollments JOIN class_session ON enrollments.session_id = class_session.id WHERE class_session.class_id = ? AND enrollments.rating > 0", (class_id,))

    average = cursor.fetchone()[0]

    conn.close()

    return average

def get_students_for_manager(manager_id):
    conn = sqlite3.connect("cooking_school.db")
    cursor = conn.cursor()

    cursor.execute("SELECT cooking_class.title, class_session.day, class_session.start_time, users.first_name, users.last_name, users.email FROM enrollments JOIN class_session ON enrollments.session_id = class_session.id JOIN cooking_class ON class_session.class_id = cooking_class.id JOIN users ON enrollments.student_id = users.id WHERE cooking_class.manager_id = ? ORDER BY cooking_class.title", (manager_id,))

    students = cursor.fetchall()

    conn.close()

    return students