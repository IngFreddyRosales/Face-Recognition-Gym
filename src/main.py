import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from db_manager import insert_user, get_users, update_user, clear_faces_db, delete_user
from datetime import datetime, timedelta
import cv2
import numpy as np
from face_utils import get_face_encoding
import face_recognition
import pygame

def run_main_menu():
    # create_db()  # Asegurarse de que la base de datos esté creada
    root = tk.Tk()
    root.title("Sistema de Membresía - Gimnasio")
    root.geometry("500x400")
    root.configure(bg="#2C3E50")
    root.resizable(False, False)
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (500 // 2)
    y = (root.winfo_screenheight() // 2) - (400 // 2)
    root.geometry(f"500x400+{x}+{y}")

    main_frame = tk.Frame(root, bg="#2C3E50")
    main_frame.pack(expand=True, fill="both", padx=40, pady=40)

    title_label = tk.Label(
        main_frame, 
        text="🏋️ Sistema de Membresía", 
        font=("Arial", 28, "bold"), 
        bg="#2C3E50", 
        fg="#ECF0F1"
    )
    title_label.pack(pady=(0, 10))

    subtitle_label = tk.Label(
        main_frame, 
        text="Gestión de acceso y membresías", 
        font=("Arial", 14), 
        bg="#2C3E50", 
        fg="#BDC3C7"
    )
    subtitle_label.pack(pady=(0, 40))

    button_style = {
        "font": ("Arial", 16, "bold"),
        "width": 20,
        "height": 2,
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2"
    }

    admin_btn = tk.Button(
        main_frame,
        text="👨‍💼 Administrador",
        bg="#3498DB",
        fg="white",
        activebackground="#2980B9",
        activeforeground="white",
        command=lambda: (root.destroy(), run_admin_gui()),
        **button_style
    )
    admin_btn.pack(pady=15)

    user_btn = tk.Button(
        main_frame,
        text="👤 Verificar Membresía",
        bg="#27AE60",
        fg="white",
        activebackground="#229954",
        activeforeground="white",
        command=lambda: (root.destroy(), run_user_gui()),
        **button_style
    )
    user_btn.pack(pady=15)

    def on_enter_admin(e):
        admin_btn.config(bg="#2980B9")
    def on_leave_admin(e):
        admin_btn.config(bg="#3498DB")
    def on_enter_user(e):
        user_btn.config(bg="#229954")
    def on_leave_user(e):
        user_btn.config(bg="#27AE60")

    admin_btn.bind("<Enter>", on_enter_admin)
    admin_btn.bind("<Leave>", on_leave_admin)
    user_btn.bind("<Enter>", on_enter_user)
    user_btn.bind("<Leave>", on_leave_user)

    info_label = tk.Label(
        main_frame,
        text="Seleccione el modo de acceso deseado",
        font=("Arial", 12),
        bg="#2C3E50",
        fg="#95A5A6"
    )
    info_label.pack(side="bottom", pady=(40, 0))

    root.mainloop()

def run_admin_gui():
    root = tk.Tk()
    root.title("Panel de Administración")
    root.geometry("900x800")
    root.configure(bg="#34495E")
    root.resizable(False, False)

    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (800 // 2)
    y = (root.winfo_screenheight() // 2) - (700 // 2)
    root.geometry(f"800x700+{x}+{y}")

    cap = cv2.VideoCapture(0)
    captured_face = {'img': None}

    main_frame = tk.Frame(root, bg="#34495E")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    title_label = tk.Label(
        main_frame,
        text="👨‍💼 Panel de Administración",
        font=("Arial", 24, "bold"),
        bg="#34495E",
        fg="#ECF0F1"
    )
    title_label.pack(pady=(0, 20))

    camera_frame = tk.LabelFrame(
        main_frame,
        text="📹 Vista de Cámara",
        font=("Arial", 12, "bold"),
        bg="#34495E",
        fg="#ECF0F1",
        bd=2,
        relief="groove"
    )
    camera_frame.pack(pady=(0, 20))

    camera_label = tk.Label(camera_frame, width=300, height=180, bg="black")
    camera_label.pack(padx=20, pady=20)

    capture_status = tk.Label(
        main_frame,
        text="📸 Listo para capturar",
        font=("Arial", 12),
        bg="#34495E",
        fg="#F39C12"
    )
    capture_status.pack(pady=(0, 10))

    form_frame = tk.LabelFrame(
        main_frame,
        text="📝 Registro de Usuario",
        font=("Arial", 12, "bold"),
        bg="#34495E",
        fg="#ECF0F1",
        bd=2,
        relief="groove"
    )
    form_frame.pack(fill="x", pady=(0, 20))

    tk.Label(form_frame, text="👤 Nombre completo:", font=("Arial", 11), bg="#34495E", fg="#ECF0F1").grid(row=0, column=0, sticky="w", padx=10, pady=10)
    entry_nombre = tk.Entry(form_frame, font=("Arial", 11), width=25)
    entry_nombre.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(form_frame, text="📅 Fecha de vencimiento:", font=("Arial", 11), bg="#34495E", fg="#ECF0F1").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_vencimiento = tk.Entry(form_frame, font=("Arial", 11), width=25)
    entry_vencimiento.grid(row=1, column=1, padx=10, pady=10)

    
    tk.Label(form_frame, text="🔑 Rol:", font=("Arial", 11), bg="#34495E", fg="#ECF0F1").grid(row=2, column=0, sticky="w", padx=10, pady=10)
    role_var = tk.StringVar(value="cliente")
    role_menu = ttk.Combobox(form_frame, textvariable=role_var, values=["cliente", "admin"], state="readonly", font=("Arial", 11), width=23)
    role_menu.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(form_frame, text="🪪 CI:", font=("Arial", 11), bg="#34495E", fg="#ECF0F1").grid(row=3, column=0, sticky="w", padx=10, pady=10)
    entry_ci = tk.Entry(form_frame, font=("Arial", 11), width=25)
    entry_ci.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(form_frame, text="🔒 Contraseña:", font=("Arial", 11), bg="#34495E", fg="#ECF0F1").grid(row=4, column=0, sticky="w", padx=10, pady=10)
    entry_contrasenia = tk.Entry(form_frame, font=("Arial", 11), width=25, show="*")
    entry_contrasenia.grid(row=4, column=1, padx=10, pady=10)

    def set_default_date():
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        entry_vencimiento.delete(0, tk.END)
        entry_vencimiento.insert(0, future_date)

    tk.Button(
        form_frame,
        text="📅 +30 días",
        command=set_default_date,
        bg="#9B59B6",
        fg="white",
        font=("Arial", 9),
        cursor="hand2"
    ).grid(row=1, column=2, padx=5, pady=10)

    entry_vencimiento.insert(0, "YYYY-MM-DD")
    entry_vencimiento.config(fg="gray")

    def on_date_focus_in(event):
        if entry_vencimiento.get() == "YYYY-MM-DD":
            entry_vencimiento.delete(0, tk.END)
            entry_vencimiento.config(fg="black")

    def on_date_focus_out(event):
        if entry_vencimiento.get() == "":
            entry_vencimiento.insert(0, "YYYY-MM-DD")
            entry_vencimiento.config(fg="gray")

    entry_vencimiento.bind("<FocusIn>", on_date_focus_in)
    entry_vencimiento.bind("<FocusOut>", on_date_focus_out)

    def update_camera():
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Rostro detectado", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            if len(faces) == 0:
                cv2.putText(frame, "Posicione su rostro en el centro", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img)
            camera_label.imgtk = imgtk
            camera_label.configure(image=imgtk)
        root.after(20, update_camera)

    def capture_face_from_stream():
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("❌ Error", "No se pudo acceder a la cámara.")
            return
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            face_img = frame[y:y + h, x:x + w]
            captured_face['img'] = face_img
            capture_status.config(text="✅ Rostro capturado correctamente", fg="#27AE60")
            messagebox.showinfo("✅ Éxito", "Rostro capturado correctamente.")
        else:
            capture_status.config(text="❌ No se detectó rostro", fg="#E74C3C")
            messagebox.showerror("❌ Error", "No se detectó un rostro. Asegúrese de estar bien iluminado.")

    def register_user():
        nombre = entry_nombre.get().strip()
        fecha_vencimiento = entry_vencimiento.get().strip()
        role = role_var.get()
        ci = entry_ci.get().strip()
        contrasenia = entry_contrasenia.get().strip()
        if not nombre or not fecha_vencimiento or fecha_vencimiento == "YYYY-MM-DD":
            messagebox.showerror("❌ Error", "Todos los campos son obligatorios.")
            return
        if captured_face['img'] is None:
            messagebox.showerror("❌ Error", "Primero debe capturar el rostro.")
            return
        try:
            datetime.strptime(fecha_vencimiento, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("❌ Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            return
        fecha_registro = datetime.now().strftime('%Y-%m-%d')
        encoding = get_face_encoding(captured_face['img'])
        if encoding is not None:
            encoding_bytes = encoding.tobytes()
            insert_user(nombre, encoding_bytes, fecha_registro, fecha_vencimiento, role, ci, contrasenia)
            messagebox.showinfo("✅ Éxito", f"Usuario '{nombre}' registrado exitosamente.")
            entry_nombre.delete(0, tk.END)
            entry_vencimiento.delete(0, tk.END)
            entry_vencimiento.insert(0, "YYYY-MM-DD")
            entry_vencimiento.config(fg="gray")
            role_var.set("cliente")
            entry_ci.delete(0, tk.END)
            entry_contrasenia.delete(0, tk.END)
            captured_face['img'] = None
            capture_status.config(text="📸 Listo para capturar", fg="#F39C12")
        else:
            messagebox.showerror("❌ Error", "No se pudo procesar el rostro. Intente nuevamente.")

    def show_users():
        users = get_users()
        if not users:
            messagebox.showinfo("ℹ️ Información", "No hay usuarios registrados.")
            return
        top = tk.Toplevel(root)
        top.title("👥 Usuarios Registrados")
        top.geometry("900x500")
        top.configure(bg="#34495E")
        canvas = tk.Canvas(top, bg="#34495E")
        scrollbar = ttk.Scrollbar(top, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#34495E")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        headers = ["ID", "Nombre", "Fecha Registro", "Fecha Vencimiento", "Rol", "CI", "Estado","Ingresos"]
        for i, header in enumerate(headers):
            tk.Label(scrollable_frame, text=header, font=("Arial", 12, "bold"), 
                    bg="#2C3E50", fg="#ECF0F1", relief="ridge", bd=1).grid(row=0, column=i, sticky="ew", padx=1, pady=1)
        for i, user in enumerate(users, 1):
            fecha_vencimiento = user[4]
            hoy = datetime.now().strftime('%Y-%m-%d')
            estado = "✅ Activa" if hoy <= fecha_vencimiento else "❌ Vencida"
            estado_color = "#27AE60" if hoy <= fecha_vencimiento else "#E74C3C"
            tk.Label(scrollable_frame, text=str(user[0]), bg="#ECF0F1", relief="ridge", bd=1).grid(row=i, column=0, sticky="ew", padx=1, pady=1)  # ID
            tk.Label(scrollable_frame, text=user[1], bg="#ECF0F1", relief="ridge", bd=1).grid(row=i, column=1, sticky="ew", padx=1, pady=1)      # Nombre
            tk.Label(scrollable_frame, text=user[3], bg="#ECF0F1", relief="ridge", bd=1).grid(row=i, column=2, sticky="ew", padx=1, pady=1)      # Fecha Registro
            tk.Label(scrollable_frame, text=user[4], bg="#ECF0F1", relief="ridge", bd=1).grid(row=i, column=3, sticky="ew", padx=1, pady=1)      # Fecha Vencimiento
            tk.Label(scrollable_frame, text=user[5], bg="#ECF0F1", relief="ridge", bd=1).grid(row=i, column=4, sticky="ew", padx=1, pady=1)      # Rol
            tk.Label(scrollable_frame, text=user[6], bg="#ECF0F1", relief="ridge", bd=1).grid(row=i, column=5, sticky="ew", padx=1, pady=1)      # CI
            tk.Label(scrollable_frame, text=estado, bg="#ECF0F1", fg=estado_color, relief="ridge", bd=1).grid(row=i, column=6, sticky="ew", padx=1, pady=1)  # Estado
            tk.Label(scrollable_frame, text=str(user[8]), bg="#ECF0F1", relief="ridge", bd=1).grid(row=i, column=7, sticky="ew", padx=1, pady=1)  # Ingresos
            tk.Button(scrollable_frame, text="✏️ Editar", bg="#3498DB", fg="white", 
                     command=lambda user_id=user[0], nombre=user[1], vencimiento=user[4], role=user[5], CI=user[6]: edit_user(user_id, nombre, vencimiento, role, CI)).grid(row=i, column=8, padx=5, pady=2)  # Acciones
            tk.Button(scrollable_frame, text="🗑️ Eliminar", bg="#E74C3C", fg="white",
                      command=lambda user_id=user[0]: delete_user_opcion(user_id, top)).grid(row=i, column=9, padx=5, pady=2)  # Eliminar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def edit_user(user_id, current_nombre, current_vencimiento, current_role, current_ci):
        edit_win = tk.Toplevel(root)
        edit_win.title("✏️ Editar Usuario")
        edit_win.geometry("420x400")
        edit_win.configure(bg="#34495E")

        # Canvas y scrollbar
        canvas = tk.Canvas(edit_win, bg="#34495E", highlightthickness=0)
        scrollbar = tk.Scrollbar(edit_win, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#34495E")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Contenido del formulario dentro de scrollable_frame ---
        tk.Label(scrollable_frame, text="✏️ Editar Usuario", font=("Arial", 18, "bold"), bg="#34495E", fg="#ECF0F1").pack(pady=20)
        tk.Label(scrollable_frame, text="👤 Nombre:", bg="#34495E", fg="#ECF0F1").pack()
        entry_nombre_edit = tk.Entry(scrollable_frame, font=("Arial", 12), width=30)
        entry_nombre_edit.insert(0, current_nombre)
        entry_nombre_edit.pack(pady=5)
        tk.Label(scrollable_frame, text="📅 Fecha de Vencimiento:", bg="#34495E", fg="#ECF0F1").pack()
        entry_vencimiento_edit = tk.Entry(scrollable_frame, font=("Arial", 12), width=30)
        entry_vencimiento_edit.insert(0, current_vencimiento)
        entry_vencimiento_edit.pack(pady=5)

        tk.Label(scrollable_frame, text="🔑 Rol:", bg="#34495E", fg="#ECF0F1").pack()
        role_var_edit = tk.StringVar(value=current_role)
        role_menu_edit = ttk.Combobox(scrollable_frame, textvariable=role_var_edit, values=["cliente", "admin"], state="readonly", font=("Arial", 12), width=28)
        role_menu_edit.pack(pady=5)
        role_menu_edit.set(current_role)

        tk.Label(scrollable_frame, text="🪪 CI:", bg="#34495E", fg="#ECF0F1").pack()
        entry_ci_edit = tk.Entry(scrollable_frame, font=("Arial", 12), width=30)
        entry_ci_edit.insert(0, current_ci if current_ci else "")
        entry_ci_edit.pack(pady=5)
    
        def save_changes():
            new_nombre = entry_nombre_edit.get().strip()
            new_vencimiento = entry_vencimiento_edit.get().strip()
            new_role = role_var_edit.get()
            new_ci = entry_ci_edit.get().strip()
            if not new_nombre or not new_vencimiento:
                messagebox.showerror("❌ Error", "Todos los campos son obligatorios.")
                return
            try:
                datetime.strptime(new_vencimiento, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("❌ Error", "Formato de fecha inválido. Use YYYY-MM-DD")
                return
            update_user(user_id, new_nombre, new_vencimiento, new_role, new_ci)
            messagebox.showinfo("✅ Éxito", "Usuario actualizado correctamente.")
            edit_win.destroy()
        tk.Button(scrollable_frame, text="💾 Guardar Cambios", command=save_changes, 
                bg="#27AE60", fg="white", font=("Arial", 12), cursor="hand2").pack(pady=20)
        
    def delete_user_opcion(user_id, top):
        result = messagebox.askyesno("⚠️ Confirmación", "¿Está seguro de que desea eliminar este usuario?\n\nEsta acción no se puede deshacer.")
        if result:
            delete_user(user_id)
            messagebox.showinfo("✅ Éxito", "Usuario eliminado correctamente.")
            top.destroy()
            show_users()


    def clear_database():
        result = messagebox.askyesno("⚠️ Confirmación", 
                                   "¿Está seguro de que desea eliminar TODOS los usuarios?\n\nEsta acción no se puede deshacer.")
        if result:
            clear_faces_db()
            messagebox.showinfo("✅ Éxito", "Base de datos limpiada correctamente.")

    buttons_frame = tk.Frame(main_frame, bg="#34495E")
    buttons_frame.pack(fill="x")

    button_style = {
        "font": ("Arial", 12, "bold"),
        "height": 2,
        "width": 20,
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2"
    }

    tk.Button(buttons_frame, text="📸 Capturar Rostro", command=capture_face_from_stream, 
             bg="#E67E22", fg="white", **button_style).pack(side="left", padx=5, pady=10)
    tk.Button(buttons_frame, text="💾 Registrar Usuario", command=register_user, 
             bg="#27AE60", fg="white", **button_style).pack(side="left", padx=5, pady=10)
    tk.Button(buttons_frame, text="👥 Ver Usuarios", command=show_users, 
             bg="#3498DB", fg="white", **button_style).pack(side="left", padx=5, pady=10)
    tk.Button(buttons_frame, text="🗑️ Limpiar BD", command=clear_database, 
             bg="#E74C3C", fg="white", **button_style).pack(side="left", padx=5, pady=10)
    back_button = tk.Button(
        main_frame,
        text="🔙 Volver al Menú Principal",
        font=("Arial", 12, "bold"),
        bg="#34495E",
        fg="white",
        cursor="hand2",
        command=lambda: (cap.release(), root.destroy(), run_main_menu())
    )
    back_button.pack(side="bottom", pady=20)

    def on_closing():
        cap.release()
        root.destroy()
        run_main_menu()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    update_camera()
    root.mainloop()

    

def run_user_gui():
    root = tk.Tk()
    root.title("🔍 Verificación de Membresía")
    root.geometry("900x800")
    root.configure(bg="#2C3E50")
    root.resizable(False, False)
    pygame.mixer.init()
    try:
        sound_active = pygame.mixer.Sound('sounds/luvvoice.com-20250527-kqJQWR.mp3')
        sound_expired = pygame.mixer.Sound('sounds/luvvoice.com-20250527-36z3rd.mp3')
        sound_not_found = pygame.mixer.Sound('sounds/luvvoice.com-20250527-pqzjxW.mp3')
    except:
        messagebox.showerror("Error", "No se pudo cargar el sonido. Asegúrese de que los archivos existan.")
        return
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (700 // 2)
    y = (root.winfo_screenheight() // 2) - (600 // 2)
    root.geometry(f"700x600+{x}+{y}")
    cap = cv2.VideoCapture(0)
    main_frame = tk.Frame(root, bg="#2C3E50")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    title_label = tk.Label(
        main_frame,
        text="🔍 Verificación de Membresía",
        font=("Arial", 24, "bold"),
        bg="#2C3E50",
        fg="#ECF0F1"
    )
    title_label.pack(pady=(0, 20))
    instructions_label = tk.Label(
        main_frame,
        text="Posicione su rostro frente a la cámara para verificar su membresía",
        font=("Arial", 12),
        bg="#2C3E50",
        fg="#BDC3C7"
    )
    instructions_label.pack(pady=(0, 20))
    camera_frame = tk.LabelFrame(
        main_frame,
        text="📹 Cámara de Verificación",
        font=("Arial", 12, "bold"),
        bg="#2C3E50",
        fg="#ECF0F1",
        bd=2,
        relief="groove"
    )
    camera_frame.pack(pady=(0, 20))
    camera_label = tk.Label(camera_frame, width=300, height=180, bg="black")
    camera_label.pack(padx=10, pady=10)
    status_frame = tk.LabelFrame(
        main_frame,
        text="📊 Estado de Membresía",
        font=("Arial", 12, "bold"),
        bg="#2C3E50",
        fg="#ECF0F1",
        bd=2,
        relief="groove"
    )
    status_frame.pack(fill="x", pady=(0, 10))
    status_label = tk.Label(
        status_frame,
        text="Esperando verificación...",
        font=("Arial", 20, "bold"),
        bg="#2C3E50",
        fg="#F39C12"
    )
    status_label.pack(pady=10)
    name_label = tk.Label(
        status_frame,
        text="",
        font=("Arial", 16),
        bg="#2C3E50",
        fg="#ECF0F1"
    )
    name_label.pack(pady=(0, 10))
    expiry_label = tk.Label(
        status_frame,
        text="",
        font=("Arial", 12),
        bg="#2C3E50",
        fg="#BDC3C7"
    )
    expiry_label.pack()
    def play_sound(sound_type):
        try:
            if sound_type == "active" and sound_active:
                sound_active.play()
            elif sound_type == "expired" and sound_expired:
                sound_expired.play()
            elif sound_type == "not_found" and sound_not_found:
                sound_not_found.play()
        except Exception as e:
            print(f"Error reproduciendo audio: {e}")
    def bytes_to_encoding(encoding_bytes):
        try:
            arr = np.frombuffer(encoding_bytes, dtype=np.float64)
            if arr.size == 128:
                return arr
        except Exception:
            pass
        return None
    def check_membership_in_frame(face_img):
        face_encoding = get_face_encoding(face_img)
        if face_encoding is None:
            return False
        users = get_users()
        for user in users:
            db_encoding_bytes = user[2]
            db_encoding = bytes_to_encoding(db_encoding_bytes)
            if db_encoding is None:
                continue
            match = face_recognition.compare_faces([db_encoding], face_encoding, tolerance=0.5)[0]
            if match:
                nombre = user[1]
                fecha_vencimiento = user[4]
                hoy = datetime.now().strftime('%Y-%m-%d')
                if hoy <= fecha_vencimiento:
                    status_label.config(text="✅ Membresía Activa", fg="#27AE60")
                    name_label.config(text=f"Bienvenido, {nombre}")
                    expiry_label.config(text=f"Válido hasta: {fecha_vencimiento}")
                    play_sound("active")
                else:
                    status_label.config(text="❌ Membresía Vencida", fg="#E74C3C")
                    name_label.config(text=f"Usuario: {nombre}")
                    expiry_label.config(text=f"Venció el: {fecha_vencimiento}")
                    play_sound("expired")
                return True
        status_label.config(text="❓ Usuario No Encontrado", fg="#95A5A6")
        name_label.config(text="Rostro no reconocido en el sistema")
        expiry_label.config(text="Contacte al administrador para registrarse")
        play_sound("not_found")
        return False
    face_cascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')
    last_check_time = 0
    def update_camera():
        nonlocal last_check_time
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img)
            camera_label.imgtk = imgtk
            camera_label.configure(image=imgtk)
            if len(faces) > 0:
                now = datetime.now().timestamp()
                if now - last_check_time > 2:
                    (x, y, w, h) = faces[0]
                    face_img = frame[y:y + h, x:x + w]
                    check_membership_in_frame(face_img)
                    last_check_time = now
        root.after(30, update_camera)
    back_button = tk.Button(
        main_frame,
        text="🔙 Volver al Menú Principal",
        font=("Arial", 12, "bold"),
        bg="#34495E",
        fg="white",
        cursor="hand2",
        command=lambda: (cap.release(), root.destroy(), run_main_menu())
    )
    back_button.pack(side="bottom", pady=10)
    def on_closing():
        cap.release()
        root.destroy()
        run_main_menu()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    update_camera()
    root.mainloop()

if __name__ == "__main__":
    run_main_menu()