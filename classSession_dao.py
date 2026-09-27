import sqlite3

def create_session(class_id, day, start_time, kitchen, max_capacity):
  query = "INSERT INTO class_session(class_id, day, start_time, kitchen, max_capacity) VALUES(?, ?, ?, ?, ?)"
  conn = sqlite3.connect("cooking_school.db")
  cursor = conn.cursor()
  
  cursor.execute(query, (class_id, day, start_time, kitchen, max_capacity))
  session_id = cursor.lastrowid
  
  conn.commit()
  
  cursor.close()
  conn.close()
  
  return session_id

def get_session_by_id(session_id):
  query = 'SELECT * FROM class_session WHERE "id"=?'
  
  conn = sqlite3.connect("cooking_school.db")
  cursor = conn.cursor()
  
  cursor.execute(query, (session_id,))
  session = cursor.fetchone()
  
  cursor.close()
  conn.close()
  
  return session

def get_sessions_by_class(class_id):
  query = "SELECT * FROM class_session WHERE class_id=?"
  
  conn = sqlite3.connect("cooking_school.db")
  cursor = conn.cursor()
  
  cursor.execute(query, (class_id,))
  sessions = cursor.fetchall()
  
  cursor.close()
  conn.close()
  
  return sessions
