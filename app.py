from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "students.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            course TEXT NOT NULL,
            year INTEGER
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def index():
    connection = get_db_connection()

    students = connection.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template("index.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        course = request.form["course"]
        year = request.form["year"]

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO students (name, email, phone, course, year)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, course, year))

        connection.commit()
        connection.close()

        return redirect(url_for("index"))

    return render_template("add_student.html")


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    connection = get_db_connection()

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if student is None:
        connection.close()
        return "Student not found", 404

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        course = request.form["course"]
        year = request.form["year"]

        connection.execute("""
            UPDATE students
            SET name = ?, email = ?, phone = ?, course = ?, year = ?
            WHERE id = ?
        """, (name, email, phone, course, year, student_id))

        connection.commit()
        connection.close()

        return redirect(url_for("index"))

    connection.close()

    return render_template("edit_student.html", student=student)


@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    connection = get_db_connection()

    connection.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
