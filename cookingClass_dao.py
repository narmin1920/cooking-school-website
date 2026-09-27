import sqlite3

def get_all_classes():
    conn = sqlite3.connect("cooking_school.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT * FROM cooking_class"
    cursor.execute(query)
    classes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return classes

def create_class(manager_id, title, cuisine, difficulty, duration, dietary, chef_name, ingredients,
    description, img1, img2, img3):
    conn = sqlite3.connect("cooking_school.db")
    cursor = conn.cursor()
    
    query = "INSERT INTO cooking_class (manager_id, title, cuisine, difficulty, duration, dietary, chef_name, ingredients, description, img1, img2, img3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (
        manager_id, title, cuisine, difficulty, duration, dietary, chef_name, 
        ingredients, description, img1, img2, img3
    ))
    conn.commit()
    
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id

def get_class_id(class_id):
    conn = sqlite3.connect("cooking_school.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT * FROM cooking_class WHERE id = ?"
    cursor.execute(query, (class_id,))
    cooking_class = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return cooking_class

def get_classes_by_manager(manager_id):
    conn = sqlite3.connect("cooking_school.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT * FROM cooking_class WHERE manager_id = ?"
    cursor.execute(query, (manager_id,))
    classes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return classes