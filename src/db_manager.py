import sqlite3

def create_db():
    conn = sqlite3.connect('db/usuarios.db')
    cursor = conn.cursor()
    # Crear la tabla con todas las columnas si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            imagen_rostro BLOB,
            fecha_registro TEXT,
            fecha_vencimiento TEXT,
            role TEXT DEFAULT 'cliente',
            ci TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(nombre, imagen_rostro, fecha_registro, fecha_vencimiento, role='cliente', ci=None):
    conn = sqlite3.connect('db/usuarios.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nombre, imagen_rostro, fecha_registro, fecha_vencimiento, role, ci) VALUES (?, ?, ?, ?, ?, ?)",
        (nombre, imagen_rostro, fecha_registro, fecha_vencimiento, role, ci)
    )
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('db/usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    users = cursor.fetchall()
    conn.close()
    return users

def update_user(user_id, new_nombre, new_fecha_vencimiento, new_role=None, new_ci=None):
    conn = sqlite3.connect('db/usuarios.db')
    cursor = conn.cursor()
    # Construir la consulta dinámicamente según los campos proporcionados
    fields = []
    values = []
    if new_nombre is not None:
        fields.append("nombre=?")
        values.append(new_nombre)
    if new_fecha_vencimiento is not None:
        fields.append("fecha_vencimiento=?")
        values.append(new_fecha_vencimiento)
    if new_role is not None:
        fields.append("role=?")
        values.append(new_role)
    if new_ci is not None:
        fields.append("ci=?")
        values.append(new_ci)
    values.append(user_id)
    sql = f"UPDATE usuarios SET {', '.join(fields)} WHERE id=?"
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def clear_faces_db():
    conn = sqlite3.connect('db/usuarios.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios")
    conn.commit()
    conn.close()

def drop_usuarios_table():
    conn = sqlite3.connect('db/usuarios.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS usuarios")
    conn.commit()