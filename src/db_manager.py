import sqlite3

def create_db():
    conn = sqlite3.connect('db/usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            imagen_rostro BLOB,
            fecha_registro TEXT,
            fecha_vencimiento TEXT,
            role TEXT DEFAULT 'cliente',
            ci TEXT,
            contrasenia TEXT,
            ingresos INTEGER DEFAULT 0
        )
    ''')
    # Si la columna ya existe, no pasa nada; si no, la añade.
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN ingresos INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass  # Ya existe
    conn.commit()
    conn.close()

def insert_user(nombre, imagen_rostro, fecha_registro, fecha_vencimiento, role='cliente', ci=None, contrasenia=None):
    conn = sqlite3.connect('db/usuarios.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nombre, imagen_rostro, fecha_registro, fecha_vencimiento, role, ci, contrasenia) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (nombre, imagen_rostro, fecha_registro, fecha_vencimiento, role, ci, contrasenia)
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

def increment_ingresos(user_id):
    conn =sqlite3.connect('db/usuarios.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET ingresos = ingresos + 1 WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

def update_user(user_id, new_nombre, new_inicio, new_fecha_vencimiento, new_role=None, new_ci=None):
    conn = sqlite3.connect('db/usuarios.db')
    cursor = conn.cursor()
    # Construir la consulta dinámicamente según los campos proporcionados
    fields = []
    values = []
    if new_nombre is not None:
        fields.append("nombre=?")
        values.append(new_nombre)
    if new_inicio is not None:
        fields.append("fecha_registro=?")
        values.append(new_inicio)
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

def delete_user(user_id):
    conn = sqlite3.connect('db/usuarios.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

def drop_usuarios_table():
    conn = sqlite3.connect('db/usuarios.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS usuarios")
    conn.commit()