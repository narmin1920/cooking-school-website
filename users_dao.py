import sqlite3

def get_all_users():
  users_query = "SELECT * FROM users"
  conn = sqlite3.connect("cooking_school.db")
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  
  cursor.execute(users_query)
  users = cursor.fetchall()
  
  cursor.close()
  conn.close()
  
  return users
  
def create_new_user(first_name, last_name, email, password, role):
  query = "INSERT INTO users (first_name, last_name, email, password, role) VALUES(?, ?, ?, ?, ?)"
  conn = sqlite3.connect("cooking_school.db")
  cursor = conn.cursor()
  
  cursor.execute(query, (first_name, last_name, email, password, role))
  conn.commit()
  
  cursor.close()
  conn.close()

def get_users_by_email(email):
  query = "SELECT * FROM users WHERE email=?"
  
  conn = sqlite3.connect("cooking_school.db")
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  
  cursor.execute(query, (email,))
  users = cursor.fetchone()
  
  cursor.close()
  conn.close()
  
  return users

def get_users_by_id(user_id):
  query = "SELECT * FROM users WHERE id=?"
  
  conn = sqlite3.connect("cooking_school.db")
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  
  cursor.execute(query, (user_id,))
  users = cursor.fetchone()
  
  cursor.close()
  conn.close()
  
  return users