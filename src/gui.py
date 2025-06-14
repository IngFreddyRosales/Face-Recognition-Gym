import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from db_manager import insert_user, get_users, update_user, clear_faces_db
from datetime import datetime, timedelta
import cv2
import numpy as np
from face_utils import  get_face_encoding

def run_admin_gui():
    root = tk.Tk()
    root.title("Panel de Administración")
    root.geometry("900x800")
    root.configure(bg="#34495E")
    root.resizable(False, False)

    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (800 // 2)
    y = (root.winfo_screenheight() // 2) - (700 // 2)
    root.geometry(f"800x700+{x}+{y}")

    cap = cv2.VideoCapture(0)  # Cambié a cámara local para mejor compatibilidad
    captured_face = {'img': None}

    # Frame principal
    main_frame = tk.Frame(root, bg="#34495E")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Título
    title_label = tk.Label(
        main_frame,
        text="👨‍💼 Panel de Administración",
        font=("Arial", 24, "bold"),
        bg="#34495E",
        fg="#ECF0F1"
    )
    title_label.pack(pady=(0, 20))

    # Frame para cámara
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

    # Estado de captura
    capture_status = tk.Label(
        main_frame,
        text="📸 Listo para capturar",
        font=("Arial", 12),
        bg="#34495E",
        fg="#F39C12"
    )
    capture_status.pack(pady=(0, 10))

    # Frame para formulario
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

    # Campos del formulario
    tk.Label(form_frame, text="👤 Nombre completo:", font=("Arial", 11), bg="#34495E", fg="#ECF0F1").grid(row=0, column=0, sticky="w", padx=10, pady=10)
    entry_nombre = tk.Entry(form_frame, font=("Arial", 11), width=25)
    entry_nombre.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(form_frame, text="📅 Fecha de vencimiento:", font=("Arial", 11), bg="#34495E", fg="#ECF0F1").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_vencimiento = tk.Entry(form_frame, font=("Arial", 11), width=25)
    entry_vencimiento.grid(row=1, column=1, padx=10, pady=10)

    # Botón para fecha automática
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

    # Placeholder para fecha
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
        print(f"Encoding: {encoding}")
        
        if encoding is not None:
            encoding_bytes = encoding.tobytes()
            insert_user(nombre, encoding_bytes, fecha_registro, fecha_vencimiento)
            messagebox.showinfo("✅ Éxito", f"Usuario '{nombre}' registrado exitosamente.")
            entry_nombre.delete(0, tk.END)
            entry_vencimiento.delete(0, tk.END)
            entry_vencimiento.insert(0, "YYYY-MM-DD")
            entry_vencimiento.config(fg="gray")
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
        
        # Frame con scrollbar
        canvas = tk.Canvas(top, bg="#34495E")
        scrollbar = ttk.Scrollbar(top, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#34495E")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        headers = ["ID", "Nombre", "Fecha Registro", "Fecha Vencimiento", "Estado", "Acciones"]
        for i, header in enumerate(headers):
            tk.Label(scrollable_frame, text=header, font=("Arial", 12, "bold"), 
                    bg="#2C3E50", fg="#ECF0F1", relief="ridge", bd=1).grid(row=0, column=i, sticky="ew", padx=1, pady=1)
        
        # Datos de usuarios
        for i, user in enumerate(users, 1):
            fecha_vencimiento = user[4]
            hoy = datetime.now().strftime('%Y-%m-%d')
            estado = "✅ Activa" if hoy <= fecha_vencimiento else "❌ Vencida"
            estado_color = "#27AE60" if hoy <= fecha_vencimiento else "#E74C3C"
            
            tk.Label(scrollable_frame, text=str(user[0]), bg="#ECF0F1", relief="ridge", bd=1).grid(row=i, column=0, sticky="ew", padx=1, pady=1)
            tk.Label(scrollable_frame, text=user[1], bg="#ECF0F1", relief="ridge", bd=1).grid(row=i, column=1, sticky="ew", padx=1, pady=1)
            tk.Label(scrollable_frame, text=user[3], bg="#ECF0F1", relief="ridge", bd=1).grid(row=i, column=2, sticky="ew", padx=1, pady=1)
            tk.Label(scrollable_frame, text=user[4], bg="#ECF0F1", relief="ridge", bd=1).grid(row=i, column=3, sticky="ew", padx=1, pady=1)
            tk.Label(scrollable_frame, text=estado, bg="#ECF0F1", fg=estado_color, relief="ridge", bd=1).grid(row=i, column=4, sticky="ew", padx=1, pady=1)
            tk.Button(scrollable_frame, text="✏️ Editar", bg="#3498DB", fg="white", 
                     command=lambda user_id=user[0], nombre=user[1], vencimiento=user[4]: edit_user(user_id, nombre, vencimiento)).grid(row=i, column=5, padx=5, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def edit_user(user_id, current_nombre, current_vencimiento):
        edit_win = tk.Toplevel(root)
        edit_win.title("✏️ Editar Usuario")
        edit_win.geometry("400x300")
        edit_win.configure(bg="#34495E")
        
        tk.Label(edit_win, text="✏️ Editar Usuario", font=("Arial", 18, "bold"), bg="#34495E", fg="#ECF0F1").pack(pady=20)
        
        tk.Label(edit_win, text="👤 Nombre:", bg="#34495E", fg="#ECF0F1").pack()
        entry_nombre_edit = tk.Entry(edit_win, font=("Arial", 12), width=30)
        entry_nombre_edit.insert(0, current_nombre)
        entry_nombre_edit.pack(pady=5)
        
        tk.Label(edit_win, text="📅 Fecha de Vencimiento:", bg="#34495E", fg="#ECF0F1").pack()
        entry_vencimiento_edit = tk.Entry(edit_win, font=("Arial", 12), width=30)
        entry_vencimiento_edit.insert(0, current_vencimiento)
        entry_vencimiento_edit.pack(pady=5)
        
        def save_changes():
            new_nombre = entry_nombre_edit.get().strip()
            new_vencimiento = entry_vencimiento_edit.get().strip()
            
            if not new_nombre or not new_vencimiento:
                messagebox.showerror("❌ Error", "Todos los campos son obligatorios.")
                return
            
            try:
                datetime.strptime(new_vencimiento, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("❌ Error", "Formato de fecha inválido. Use YYYY-MM-DD")
                return
            
            update_user(user_id, new_nombre, new_vencimiento)
            messagebox.showinfo("✅ Éxito", "Usuario actualizado correctamente.")
            edit_win.destroy()
        
        tk.Button(edit_win, text="💾 Guardar Cambios", command=save_changes, 
                 bg="#27AE60", fg="white", font=("Arial", 12), cursor="hand2").pack(pady=20)

    def clear_database():
        result = messagebox.askyesno("⚠️ Confirmación", 
                                   "¿Está seguro de que desea eliminar TODOS los usuarios?\n\nEsta acción no se puede deshacer.")
        if result:
            clear_faces_db()
            messagebox.showinfo("✅ Éxito", "Base de datos limpiada correctamente.")

    # Frame de botones
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
        command=lambda: (cap.release(), root.destroy())
    )
    back_button.pack(side="bottom", pady=20)

    def on_closing():
        cap.release()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    update_camera()
    root.mainloop()
