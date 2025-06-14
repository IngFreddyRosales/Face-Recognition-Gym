import tkinter as tk
from tkinter import ttk
from gui import run_admin_gui
from user_gui import run_user_gui
from db_manager import create_db

def show_admin():

    root.destroy()
    run_admin_gui()

def show_user():
    root.destroy()
    run_user_gui()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Membresía - Gimnasio")
    root.geometry("500x400")
    root.configure(bg="#2C3E50")
    root.resizable(False, False)
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (500 // 2)
    y = (root.winfo_screenheight() // 2) - (400 // 2)
    root.geometry(f"500x400+{x}+{y}")

    # Frame principal
    main_frame = tk.Frame(root, bg="#2C3E50")
    main_frame.pack(expand=True, fill="both", padx=40, pady=40)

    # Título principal
    title_label = tk.Label(
        main_frame, 
        text="🏋️ Sistema de Membresía", 
        font=("Arial", 28, "bold"), 
        bg="#2C3E50", 
        fg="#ECF0F1"
    )
    title_label.pack(pady=(0, 10))

    # Subtítulo
    subtitle_label = tk.Label(
        main_frame, 
        text="Gestión de acceso y membresías", 
        font=("Arial", 14), 
        bg="#2C3E50", 
        fg="#BDC3C7"
    )
    subtitle_label.pack(pady=(0, 40))

    # Estilo de botones
    button_style = {
        "font": ("Arial", 16, "bold"),
        "width": 20,
        "height": 2,
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2"
    }

    # Botón Administrador
    admin_btn = tk.Button(
        main_frame,
        text="👨‍💼 Administrador",
        bg="#3498DB",
        fg="white",
        activebackground="#2980B9",
        activeforeground="white",
        command=show_admin,
        **button_style
    )
    admin_btn.pack(pady=15)

    # Botón Usuario
    user_btn = tk.Button(
        main_frame,
        text="👤 Verificar Membresía",
        bg="#27AE60",
        fg="white",
        activebackground="#229954",
        activeforeground="white",
        command=show_user,
        **button_style
    )
    user_btn.pack(pady=15)

    # Efectos hover
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

    # Información adicional
    info_label = tk.Label(
        main_frame,
        text="Seleccione el modo de acceso deseado",
        font=("Arial", 12),
        bg="#2C3E50",
        fg="#95A5A6"
    )
    info_label.pack(side="bottom", pady=(40, 0))

    root.mainloop()
