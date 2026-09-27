from flask_login import UserMixin

class User(UserMixin):

  def __init__(self, id, first_name, last_name, email, password, role):
    self.id = id
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password
    self.role = role
    
  @property
  def is_manager(self):
    return self.role == "manager"

  @property
  def is_student(self):
    return self.role == "student"