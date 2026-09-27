from flask import Flask, flash, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from users_dao import create_new_user, get_users_by_email, get_users_by_id
import cookingClass_dao, enrollments_dao, classSession_dao
import time

app = Flask(__name__)

app.config["SECRET_KEY"] = "NamrminSemsarian"  

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

def time_to_minutes(time_string):
    hours, minutes = time_string.split(":")
    return int(hours) * 60 + int(minutes)

@app.route("/")
def home():
  classes_db = cookingClass_dao.get_all_classes()
  return render_template("home.html", classes=classes_db)

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    row = get_users_by_email(email)

    if row is None or not check_password_hash(row["password"], password):
      flash("Invalid email or password.", category="error")
      return redirect(url_for("login"))

    login_user(User(row["id"], row["first_name"], row["last_name"], row["email"], row["password"], row["role"]))
    return redirect(url_for("home"))

  return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  if request.method == "POST":
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email", "").strip()
    role = request.form.get("role", "")
    password = request.form.get("password", "")
    password2 = request.form.get("password2", "")

    if len(email) < 4:
      flash("Email must be greater than 3 characters.", category="error")
      return redirect(url_for("signup"))

    if password != password2:
      flash("Passwords do not match.", category="error")
      return redirect(url_for("signup"))

    if role not in ["student", "manager"]:
      flash("Invalid role selected.", category="error")
      return redirect(url_for("signup"))

    if get_users_by_email(email) is not None:
      flash("An account with this email already exists.", category="error")
      return redirect(url_for("signup"))

    create_new_user(first_name, last_name, email, generate_password_hash(password), role)
    flash("Your account was created. Please log in.", category="success")
    return redirect(url_for("login"))
        
  return render_template("signup.html")

@login_manager.user_loader
def load_user(user_id):
  row = get_users_by_id(user_id)
  if row is None:
    return None
  return User(row["id"], row["first_name"], row["last_name"], row["email"], row["password"], row["role"])
  
@app.route("/manager")
@login_required
def manager_area():
  if current_user.role != "manager":
    return redirect(url_for("home"))
  students = enrollments_dao.get_students_for_manager(current_user.id)
  classes = cookingClass_dao.get_classes_by_manager(current_user.id)
  return render_template("manager_profile.html", classes=classes, students=students)

@app.route("/student")
@login_required
def student_area():
    if current_user.role != "student":
        return redirect(url_for("home"))

    my_enrollments = enrollments_dao.get_enrollments_by_student(current_user.id)  
    return render_template("student.profile.html", enrollments=my_enrollments)

@app.route("/classes/create", methods=["GET", "POST"])
@login_required
def create_cooking_class():
  if not current_user.is_manager:
    return redirect(url_for("home"))

  if request.method == "POST":
    title = request.form.get("title", "").strip()
    cuisine = request.form.get("cuisine", "").strip()
    difficulty = request.form.get("difficulty", "")
    dietary = request.form.get("dietary_category", "")
    chef_name = request.form.get("chef", "").strip()
    description = request.form.get("description", "").strip()
    ingredient1 = request.form.get("ingredient1", "").strip()
    ingredient2 = request.form.get("ingredient2", "").strip()
    ingredient3 = request.form.get("ingredient3", "").strip()
    ingredient4 = request.form.get("ingredient4", "").strip()     
    img1 = request.files.get("img1")
    img2 = request.files.get("img2")
    img3 = request.files.get("img3")
    
    if not all([img1, img2, img3]):
      flash("Please upload all 3 photos.", category="error")
      return redirect(url_for("create_cooking_class"))
    
    filename1 = img1.filename
    filename2 = img2.filename
    filename3 = img3.filename

    img1.save("static/images/classes/" + filename1)
    img2.save("static/images/classes/" + filename2)
    img3.save("static/images/classes/" + filename3)
    
    try:
      duration = int(request.form.get("duration", "0"))
    except ValueError:
      duration = 0

    if not all([title, cuisine, difficulty, dietary, chef_name, description, ingredient1, ingredient2, ingredient3, ingredient4]) or duration < 1:
      flash("Please complete every field with valid values.", category="error")
      return redirect(url_for("create_cooking_class"))
    
    ingredients = ", ".join([ingredient1, ingredient2, ingredient3, ingredient4])
    
    cookingClass_dao.create_class(
      current_user.id, title, cuisine, difficulty, duration, dietary,
      chef_name, ingredients, description, filename1, filename2, filename3
    )
    flash("Cooking class created.", category="success")
    return redirect(url_for("manager_area"))

  return render_template("create_class.html")

@app.route("/enroll/<int:session_id>", methods=["POST"])
@login_required
def enroll(session_id):
    if current_user.role != "student":
        flash("Only students can enroll in classes.", category="error")
        return redirect(url_for("home"))
      
    session = classSession_dao.get_session_by_id(session_id)
    if session is None:
        flash("Session not found.", category="error")
        return redirect(url_for("home"))  
      
    existing = enrollments_dao.get_enrollment(current_user.id, session_id)
    if existing is not None:
        flash("You are already enrolled in this session.", category="error")
        return redirect(url_for("class_detail", class_id=session[1]))
        
    enrolled_count = enrollments_dao.count_enrollments(session_id)
    if enrolled_count >= session[5]:
      flash("This session is full, you cannot enroll.", category="error")
      return redirect(url_for("class_detail", class_id=session[1]))

    my_enrollments = enrollments_dao.get_enrollments_by_student(current_user.id)
    if len(my_enrollments) >= 4:
        flash("You can enroll in a maximum of 4 sessions per week.", category="error")
        return redirect(url_for("student_area"))

    cooking_class = cookingClass_dao.get_class_id(session[1])

    new_day = session[2]
    new_start = session[3]
    new_start_minutes = time_to_minutes(new_start)
    new_end_minutes = new_start_minutes + cooking_class["duration"]
    
    for enrollment in my_enrollments:
      enrolled_day = enrollment[2]
      enrolled_start = enrollment[3]
      enrolled_duration = enrollment[8]

      if enrolled_day == new_day:
        enrolled_start_minutes = time_to_minutes(enrolled_start)
        enrolled_end_minutes = enrolled_start_minutes + enrolled_duration

        if (new_start_minutes < enrolled_end_minutes and enrolled_start_minutes < new_end_minutes):
            flash("This session overlaps with another session you are enrolled in.", category="error")
            return redirect(url_for("class_detail", class_id=session[1]))

    enrollments_dao.create_enrollment(current_user.id, session_id)
    flash("Successfully enrolled in the session!", category="success")
    return redirect(url_for("student_area"))
    
@app.route("/logout")
@login_required
def logout():
  logout_user()
  flash("You logged out.", category="success")
  return redirect(url_for("home"))

@app.route("/classes/<int:class_id>")
def class_detail(class_id):
    c = cookingClass_dao.get_class_id(class_id)
    if not c:
        flash("Class not found.", category="error")
        return redirect(url_for("home"))

    sessions = classSession_dao.get_sessions_by_class(class_id)
    average_rating = enrollments_dao.get_class_average_rating(class_id)

    return render_template("class_detail.html", c=c, sessions=sessions, average_rating=average_rating)

@app.route("/classes/<int:class_id>/sessions/create", methods=["GET", "POST"])
@login_required
def create_session(class_id):
    if current_user.role != "manager":
        return redirect(url_for("home"))

    c = cookingClass_dao.get_class_id(class_id)
    if not c:
      flash("Class not found.", category="error")
      return redirect(url_for("home"))
      
    if c['manager_id'] != current_user.id:
      return redirect(url_for("home"))
    
    if request.method == "POST":
        day = request.form.get("day", "")
        start_time = request.form.get("start_time", "")
        kitchen = request.form.get("kitchen", "").strip()

        try:
            max_capacity = int(request.form.get("max_capacity", "0"))
        except ValueError:
            max_capacity = 0

        if not day or not start_time or not kitchen or max_capacity < 1:
            flash("Please complete all session fields.", category="error")
            return redirect(url_for("create_session", class_id=class_id))

        classSession_dao.create_session(class_id, day, start_time, kitchen, max_capacity)
        flash("Session created.", category="success")
        return redirect(url_for("class_detail", class_id=class_id))

    return render_template("create_session.html", c=c)

@app.route("/cancel/<int:session_id>", methods=["POST"])
@login_required
def cancel_enrollment(session_id):
    enrollments_dao.cancel_enrollment(current_user.id, session_id)
    flash("Successfully cancelled your enrollment.", category="success")
    return redirect(url_for("student_area"))
  
@app.route("/rate/<int:session_id>", methods=["POST"])
@login_required
def rate_session(session_id):
    if current_user.role != "student":
        return redirect(url_for("home"))

    enrollment = enrollments_dao.get_enrollment(current_user.id, session_id)
    if enrollment is None:
        flash("You can only rate a session you attended.", category="error")
        return redirect(url_for("student_area"))

    try:
        rating = int(request.form.get("rating", "0"))
    except ValueError:
        rating = 0
    
    if rating < 1 or rating > 5:
        flash("Rating must be between 1 and 5.", category="error")
        return redirect(url_for("student_area"))

    enrollments_dao.update_rating(current_user.id, session_id, rating)
    flash("Thank you for your rating!", category="success")
    return redirect(url_for("student_area"))

if __name__ == "__main__":
  app.run(debug=True)