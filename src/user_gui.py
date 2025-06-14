import tkinter as tk
from tkinter import messagebox
from db_manager import get_users
from PIL import Image, ImageTk
import cv2
import numpy as np
import face_recognition
from face_utils import get_face_encoding
from datetime import datetime
import pygame

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

    # Centrar ventana
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

    # Instrucciones
    instructions_label = tk.Label(
        main_frame,
        text="Posicione su rostro frente a la cámara para verificar su membresía",
        font=("Arial", 12),
        bg="#2C3E50",
        fg="#BDC3C7"
    )
    instructions_label.pack(pady=(0, 20))

    # Frame para cámara
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

    # Frame de estado
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

    # Label para fecha de vencimiento
    expiry_label = tk.Label(
        status_frame,
        text="",
        font=("Arial", 12),
        bg="#2C3E50",
        fg="#BDC3C7"
    )
    expiry_label.pack()

    def play_sound(sound_type):
        """Reproduce el sonido correspondiente"""
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
                fecha_vencimiento = user[4]
                nombre = user[1]
                hoy = datetime.now().strftime('%Y-%m-%d')
                
                if hoy <= fecha_vencimiento:
                    status_label.config(text="✅ Membresía Activa", fg="#27AE60")
                    name_label.config(text=f"Bienvenido/a, {nombre}")
                    expiry_label.config(text=f"Válida hasta: {fecha_vencimiento}")

                    play_sound("active")

                    return True    
                else:
                    status_label.config(text="❌ Membresía Vencida", fg="#E74C3C")
                    name_label.config(text=f"Hola, {nombre}")
                    expiry_label.config(text=f"Venció el: {fecha_vencimiento}", fg="#E74C3C")
                    
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
            
            current_time = datetime.now().timestamp()
            
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(frame, "Verificando...", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                if current_time - last_check_time > 2:
                    face_img = frame[y:y + h, x:x + w]
                    check_membership_in_frame(face_img)
                    last_check_time = current_time
            else:
                cv2.putText(frame, "Posicione su rostro en el centro", (50, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.putText(frame, "Asegurese de tener buena iluminacion", (50, 100), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                
                # Reset status when no face detected
                if current_time - last_check_time > 3:
                    status_label.config(text="Esperando verificación...", fg="#F39C12")
                    name_label.config(text="")
                    expiry_label.config(text="")
            
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img)
            camera_label.imgtk = imgtk
            camera_label.configure(image=imgtk)
        
        root.after(30, update_camera)

    back_button = tk.Button(
        main_frame,
        text="🔙 Volver al Menú Principal",
        font=("Arial", 12, "bold"),
        bg="#34495E",
        fg="white",
        cursor="hand2",
        command=lambda: (cap.release(), root.destroy())
    )
    back_button.pack(side="bottom", pady=10)

    def on_closing():
        cap.release()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    update_camera()
    root.mainloop()