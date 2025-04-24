import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from app.repository import User
import re
from tkinter import simpledialog
import base64

class UserInterface:
    def center_window(self, width=1000, height=700):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def __init__(self, repository):
        self.repository = repository
        self.window = tk.Tk()
        self.window.title("Face Recognition System")
        self.center_window()
        
        self.colors = {
            "primary": "#4285F4",  
            "primary_dark": "#3367D6", 
            "accent": "#EA4335",  
            "accent_dark": "#C62828",  
            "background": "#F5F5F5",  
            "card": "#FFFFFF",  
            "text": "#202124",  
            "text_secondary": "#5F6368",  
            "divider": "#DADCE0", 
            "success": "#34A853",  
            "warning": "#FBBC05",
        }
        
  
        self.window.configure(bg=self.colors["background"])
        
        self.style = ttk.Style()
        self.style.theme_use('clam')   
        self.style.configure("TLabel", 
                           background=self.colors["background"],
                           foreground=self.colors["text"],
                           font=("Segoe UI", 11))
        
        self.style.configure("Title.TLabel", 
                           background=self.colors["background"],
                           foreground=self.colors["primary"],
                           font=("Segoe UI", 24, "bold"))
        
        self.style.configure("Subtitle.TLabel", 
                           background=self.colors["background"],
                           foreground=self.colors["text_secondary"],
                           font=("Segoe UI", 12))
        
        self.style.configure("TButton", 
                             font=("Segoe UI", 11),
                             background=self.colors["primary"],
                             foreground="white",
                             padding=(25, 12),
                             relief="flat",
                             borderwidth=0)
        self.style.map("TButton",
                      background=[("active", self.colors["primary_dark"]),
                                 ("pressed", self.colors["primary_dark"])])
        
        self.style.configure("Accent.TButton", 
                             font=("Segoe UI", 11),
                             background=self.colors["accent"],
                             foreground="white",
                             padding=(25, 12))
        self.style.map("Accent.TButton",
                      background=[("active", self.colors["accent_dark"]),
                                 ("pressed", self.colors["accent_dark"])])

        self.style.configure("Menu.TButton", 
                           font=("Segoe UI", 11),
                           background=self.colors["primary"],
                           foreground="white",
                           padding=(25, 10))
        self.style.map("Menu.TButton",
                      background=[("active", self.colors["primary_dark"]),
                                 ("pressed", self.colors["primary_dark"])])
        
        self.style.configure("Success.TButton", 
                           font=("Segoe UI", 11),
                           background=self.colors["success"],
                           foreground="white",
                           padding=(20, 10))
        self.style.map("Success.TButton",
                      background=[("active", "#2E7D32"),
                                 ("pressed", "#2E7D32")])
        
        self.style.configure("TEntry", 
                           font=("Segoe UI", 11),
                           fieldbackground="white",
                           bordercolor=self.colors["divider"],
                           lightcolor=self.colors["divider"],
                           darkcolor=self.colors["divider"],
                           borderwidth=1,
                           relief="solid")
        self.style.map("TEntry",
                      bordercolor=[("focus", self.colors["primary"])])
        
        self.style.configure("Danger.TButton", 
                           font=("Segoe UI", 11),
                           background="#E53935",  
                           foreground="white",
                           padding=(25, 12))
        self.style.map("Danger.TButton",
                     background=[("active", "#C62828"),  
                                ("pressed", "#B71C1C")])  
        
        self.window.option_add('*TButton.borderRadius', 20)
        self.create_oval_button_style() 
        self.frames = {}
        
        self.illustration_image = None
        possible_image_paths = [
            "illustration.png",  
            os.path.join("app", "illustration.png"),  
        ]
        image_loaded = False
        for image_path in possible_image_paths:
            if os.path.exists(image_path):
                try:
                    img = Image.open(image_path)
                    img = img.resize((450, 450), Image.LANCZOS)
                    self.illustration_image = ImageTk.PhotoImage(img)
                    print(f"Successfully loaded image from: {image_path}")
                    image_loaded = True
                    break
                except Exception as e:
                    print(f"Error loading image from {image_path}: {e}")
        
        if not image_loaded:
            print("Could not find illustration image in any location. Using placeholder.")
            self.download_illustration()
            
        
        self.create_main_menu()
        self.create_login_frame()
        self.create_register_frame()
        self.create_identity_frame()
        self.create_forgot_password_frame()
        
        self.show_frame("main_menu")

    def create_oval_button_style(self):
        def _create_oval_button(widget, fill_color, hover_color):
            canvas = tk.Canvas(widget, borderwidth=0, highlightthickness=0, bg=self.colors["background"])
            canvas.pack(fill="both", expand=True)
            
            def _on_enter(event):
                canvas.itemconfig("oval", fill=hover_color)
            
            def _on_leave(event):
                canvas.itemconfig("oval", fill=fill_color)
            
            def _on_press(event):
                canvas.itemconfig("oval", fill=hover_color)
            
            def _on_release(event):
                canvas.itemconfig("oval", fill=hover_color)
                if "command" in widget.config():
                    widget.config("command")()
            
            canvas.bind("<Enter>", _on_enter)
            canvas.bind("<Leave>", _on_leave)
            canvas.bind("<ButtonPress-1>", _on_press)
            canvas.bind("<ButtonRelease-1>", _on_release)
            
            canvas.create_oval(0, 0, 0, 0, fill=fill_color, outline="", tags=("oval",))

            canvas.create_text(0, 0, text=widget["text"], fill="white", font=("Segoe UI", 11), tags=("text",))
            
            def _update_shape(event=None):
                canvas.coords("oval", 0, 0, widget.winfo_width(), widget.winfo_height())
                canvas.coords("text", widget.winfo_width()/2, widget.winfo_height()/2)
            
            widget.bind("<Configure>", _update_shape)
            _update_shape()
            
            return canvas
        
        def _create_custom_button(parent, widget_class, **kw):
            btn = ttk.Button.__new__(ttk.Button)
            ttk.Button.__init__(btn, parent, **kw)
            
            if "style" in kw and kw["style"] == "Accent.TButton":
                _create_oval_button(btn, self.colors["accent"], self.colors["accent_dark"])
            elif "style" in kw and kw["style"] == "Success.TButton":
                _create_oval_button(btn, self.colors["success"], "#2E7D32")
            elif "style" in kw and kw["style"] == "Danger.TButton":
                _create_oval_button(btn, "#E53935", "#C62828")
            else:
                _create_oval_button(btn, self.colors["primary"], self.colors["primary_dark"])
            return btn
        
    def train_face_model(self):
        import cv2
        import numpy as np
        import os

        path = 'data'
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        def get_images_and_labels(path):
            image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
            face_samples = []
            ids = []

            for image_path in image_paths:
                img = cv2.imread(image_path)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    face_samples.append(gray[y:y+h, x:x+w])
                    id = int(os.path.split(image_path)[-1].split('.')[1])
                    ids.append(id)
            return face_samples, ids

        faces, ids = get_images_and_labels(path)
        if faces:
            recognizer.train(faces, np.array(ids))
            if not os.path.exists("data"):
                os.makedirs("data")
            recognizer.save(os.path.join('data', 'trainer.yml'))
            print(f"{len(np.unique(ids))} kullanıcı için model eğitildi.")
        else:
            print("No facial images were found.")

    def validate_password(self, password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one capital letter."
        if not re.search(r"[a-z]", password):
            return False, "The password must contain at least one lowercase letter."
        if not re.search(r"\d", password):
            return False, "The password must contain at least one number."
        return True, ""

    def check_username_exists(self, username):
        for user in self.repository.users:
            if user.username == username:
                return True
        return False

    def create_main_menu(self):
        main_frame = tk.Frame(self.window, bg=self.colors["background"])
        main_frame.pack(fill="both", expand=True)
        
        left_frame = tk.Frame(main_frame, bg=self.colors["background"], width=500)
        left_frame.pack(side="left", fill="both", expand=True)
        
        right_frame = tk.Frame(main_frame, bg=self.colors["background"], width=500)
        right_frame.pack(side="right", fill="both", expand=True)
        
        left_frame.pack_propagate(False)
        right_frame.pack_propagate(False)
        
        illustration_container = tk.Frame(left_frame, bg=self.colors["background"])
        illustration_container.place(relx=0.5, rely=0.5, anchor="center")
        
        if self.illustration_image:
            illustration_label = tk.Label(illustration_container, image=self.illustration_image, bg=self.colors["background"])
            illustration_label.pack(padx=20)
        else:
            placeholder = tk.Label(illustration_container, 
                                 text="Face Recognition System", 
                                 font=("Segoe UI", 24, "bold"),
                                 fg=self.colors["primary"],
                                 bg=self.colors["background"])
            placeholder.pack(pady=50)
            
            subtitle = tk.Label(illustration_container, 
                              text="Secure and easy access", 
                              font=("Segoe UI", 16),
                              fg=self.colors["text_secondary"],
                              bg=self.colors["background"])
            subtitle.pack()
        
        content_frame = tk.Frame(right_frame, bg=self.colors["background"])
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        header = ttk.Label(content_frame, text="Welcome", style="Title.TLabel")
        header.pack(pady=(0, 10))
        
        subheader = ttk.Label(content_frame, text="Please select an option", style="Subtitle.TLabel")
        subheader.pack(pady=(0, 30))
        
        card_frame = tk.Frame(content_frame, bg=self.colors["card"], 
                            highlightbackground=self.colors["divider"],
                            highlightthickness=1,
                            relief="ridge", 
                            bd=1)
        card_frame.config(relief="ridge", bd=1)
        
        button_width = 18
        
        login_button = ttk.Button(card_frame, text="Login",
                                style="Accent.TButton",
                                command=lambda: self.show_frame("login"),
                                width=button_width)
        
        register_button = ttk.Button(card_frame, text="Register",
                                   style="TButton",
                                   command=lambda: self.show_frame("register"),
                                   width=button_width)
        
        face_login_button = ttk.Button(card_frame, text="Face Login",
                                     style="Menu.TButton",
                                     command=self.face_login_process,
                                     width=button_width)
        
        exit_button = ttk.Button(card_frame, text="Exit",
                               style="Danger.TButton",
                               command=self.exit_application,
                               width=button_width)
        
        card_frame.pack(padx=30, pady=20, ipadx=40, ipady=30)
        login_button.pack(pady=10, ipady=5)
        register_button.pack(pady=10, ipady=5)
        face_login_button.pack(pady=10, ipady=5)
        exit_button.pack(pady=10, ipady=5)
        
        self.frames["main_menu"] = main_frame

    def face_login_process(self):
        result = self.repository.face_login()
        if isinstance(result, User):
            messagebox.showinfo("Login Successful", f"Welcome {result.username}!")
            self.show_frame("identity")
        elif result == "unknown":
            messagebox.showerror("Login Failed", "Unknown face detected.")
        elif result == "max_attempts":
            messagebox.showerror("Login Failed", "Maximum recognition attempts reached.")
        else:
            messagebox.showerror("Login Failed", "Face recognition failed.")

        
    def register_face_for_current_user(self):
        user = self.repository.currentUser
        if not user:
            messagebox.showerror("Error", "Please login first.")
            return

        face_id = self.repository.users.index(user) + 1
        user.face_id = face_id
        self.repository.save_to_file()

        try:
            from app.face_register import register_face
            register_face(face_id)
            messagebox.showinfo("Success", "Face data registered successfully.")
            self.train_face_model()

        except Exception as e:
            messagebox.showerror("Error", f"Error registering face data:\n{str(e)}")
            
    def create_login_frame(self):
        login_frame = tk.Frame(self.window, bg=self.colors["background"])
        login_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(login_frame, bg=self.colors["background"], width=500)
        left_frame.pack(side="left", fill="both", expand=True)
        
        right_frame = tk.Frame(login_frame, bg=self.colors["background"], width=500)
        right_frame.pack(side="right", fill="both", expand=True)
        
        left_frame.pack_propagate(False)
        right_frame.pack_propagate(False)

        illustration_container = tk.Frame(left_frame, bg=self.colors["background"])
        illustration_container.place(relx=0.5, rely=0.5, anchor="center")
        
        if self.illustration_image:
            illustration_label = tk.Label(illustration_container, image=self.illustration_image, bg=self.colors["background"])
            illustration_label.pack(padx=20)
        else:
            placeholder = tk.Label(illustration_container, 
                                 text="Face Recognition System", 
                                 font=("Segoe UI", 24, "bold"),
                                 fg=self.colors["primary"],
                                 bg=self.colors["background"])
            placeholder.pack(pady=50)
            
            subtitle = tk.Label(illustration_container, 
                              text="Secure and easy access", 
                              font=("Segoe UI", 16),
                              fg=self.colors["text_secondary"],
                              bg=self.colors["background"])
            subtitle.pack()

        content_frame = tk.Frame(right_frame, bg=self.colors["background"])
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        header = ttk.Label(content_frame, text="Login", style="Title.TLabel")
        header.pack(pady=(0, 5))
        
        subheader = ttk.Label(content_frame, text="Please enter your credentials", style="Subtitle.TLabel")
        subheader.pack(pady=(0, 15))

        card_frame = tk.Frame(content_frame, bg=self.colors["card"], 
                            highlightbackground=self.colors["divider"],
                            highlightthickness=1,
                            relief="ridge", 
                            bd=1)
        card_frame.pack(padx=20, pady=10, ipadx=20, ipady=15)

        form = tk.Frame(card_frame, bg=self.colors["card"])
        form.pack(pady=5)

        username_frame = tk.Frame(form, bg=self.colors["card"])
        username_frame.pack(fill="x", pady=5)
        
        ttk.Label(username_frame, text="Username:", style="TLabel", background=self.colors["card"]).pack(anchor="w", pady=(0, 2))
        username_entry = ttk.Entry(username_frame, width=22)
        username_entry.pack(fill="x", ipady=3)

        password_frame = tk.Frame(form, bg=self.colors["card"])
        password_frame.pack(fill="x", pady=5)
        
        ttk.Label(password_frame, text="Password:", style="TLabel", background=self.colors["card"]).pack(anchor="w", pady=(0, 2))
        password_entry = ttk.Entry(password_frame, show="*", width=22)
        password_entry.pack(fill="x", ipady=3)

        button_width = 15
        button_container = tk.Frame(card_frame, bg=self.colors["card"])
        button_container.pack(pady=5)

        login_button = ttk.Button(button_container, text="Login", 
                                style="Accent.TButton",
                                command=lambda: self.login_user(username_entry, password_entry),
                                width=button_width)
        login_button.grid(row=0, column=0, pady=5, padx=5, ipady=3)
                  
        face_login_button = ttk.Button(button_container, 
                                     text="Face Login", 
                                     style="Menu.TButton",
                                     command=self.face_login_process,
                                     width=button_width)
        face_login_button.grid(row=0, column=1, pady=5, padx=5, ipady=3)

        forgot_frame = tk.Frame(card_frame, bg=self.colors["card"])
        forgot_frame.pack(pady=3)
        
        forgot = ttk.Label(forgot_frame, text="Forgot Password", 
                          foreground=self.colors["primary"],
                          background=self.colors["card"], 
                          cursor="hand2",
                          font=("Segoe UI", 9, "underline"))
        forgot.pack()
        forgot.bind("<Button-1>", lambda e: self.show_frame("forgot_password"))

        nav_frame = tk.Frame(login_frame, bg=self.colors["background"])
        nav_frame.place(relx=0.5, rely=0.85, anchor="center")
        
        back_button = ttk.Button(nav_frame, text="Main Menu", 
                               style="TButton",
                               command=lambda: self.show_frame("main_menu"),
                               width=15)
        back_button.pack(pady=5, ipady=3)

        self.frames["login"] = login_frame

    def create_register_frame(self):
        register_frame = tk.Frame(self.window, bg=self.colors["background"])
        register_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(register_frame, bg=self.colors["background"], width=500)
        left_frame.pack(side="left", fill="both", expand=True)
        
        right_frame = tk.Frame(register_frame, bg=self.colors["background"], width=500)
        right_frame.pack(side="right", fill="both", expand=True)

        left_frame.pack_propagate(False)
        right_frame.pack_propagate(False)

        illustration_container = tk.Frame(left_frame, bg=self.colors["background"])
        illustration_container.place(relx=0.5, rely=0.5, anchor="center")
        
        if self.illustration_image:
            illustration_label = tk.Label(illustration_container, image=self.illustration_image, bg=self.colors["background"])
            illustration_label.pack(padx=20)
        else:
            placeholder = tk.Label(illustration_container, 
                                 text="Face Recognition System", 
                                 font=("Segoe UI", 24, "bold"),
                                 fg=self.colors["primary"],
                                 bg=self.colors["background"])
            placeholder.pack(pady=50)
            
            subtitle = tk.Label(illustration_container, 
                              text="Secure and easy access", 
                              font=("Segoe UI", 16),
                              fg=self.colors["text_secondary"],
                              bg=self.colors["background"])
            subtitle.pack()

        content_frame = tk.Frame(right_frame, bg=self.colors["background"])
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        header = ttk.Label(content_frame, text="Register", style="Title.TLabel")
        header.pack(pady=(0, 5))
        
        subheader = ttk.Label(content_frame, text="Create a new account", style="Subtitle.TLabel")
        subheader.pack(pady=(0, 15))

        card_frame = tk.Frame(content_frame, bg=self.colors["card"], 
                            highlightbackground=self.colors["divider"],
                            highlightthickness=1,
                            relief="ridge", 
                            bd=1)
        card_frame.pack(padx=20, pady=10, ipadx=20, ipady=15)

        form = tk.Frame(card_frame, bg=self.colors["card"])
        form.pack(pady=5)

        username_frame = tk.Frame(form, bg=self.colors["card"])
        username_frame.pack(fill="x", pady=5)
        
        ttk.Label(username_frame, text="Username:", style="TLabel", background=self.colors["card"]).pack(anchor="w", pady=(0, 2))
        username_entry = ttk.Entry(username_frame, width=25)
        username_entry.pack(fill="x", ipady=3)

        password_frame = tk.Frame(form, bg=self.colors["card"])
        password_frame.pack(fill="x", pady=5)
        
        ttk.Label(password_frame, text="Password:", style="TLabel", background=self.colors["card"]).pack(anchor="w", pady=(0, 2))
        password_entry = ttk.Entry(password_frame, show="*", width=25)
        password_entry.pack(fill="x", ipady=3)

        confirm_password_frame = tk.Frame(form, bg=self.colors["card"])
        confirm_password_frame.pack(fill="x", pady=5)
        
        ttk.Label(confirm_password_frame, text="Confirm Password:", style="TLabel", background=self.colors["card"]).pack(anchor="w", pady=(0, 2))
        confirm_password_entry = ttk.Entry(confirm_password_frame, show="*", width=25)
        confirm_password_entry.pack(fill="x", ipady=3)

        email_frame = tk.Frame(form, bg=self.colors["card"])
        email_frame.pack(fill="x", pady=5)
        
        ttk.Label(email_frame, text="Email:", style="TLabel", background=self.colors["card"]).pack(anchor="w", pady=(0, 2))
        email_entry = ttk.Entry(email_frame, width=25)
        email_entry.pack(fill="x", ipady=3)

        password_info = ttk.Label(card_frame, 
                                text="Password: at least 8 characters, 1 uppercase letter, 1 lowercase letter, 1 digit",
                                foreground=self.colors["text_secondary"],
                                background=self.colors["card"],
                                wraplength=350,
                                font=("Segoe UI", 9),
                                justify="center")
        password_info.pack(pady=5)

        button_width = 15
        button_container = tk.Frame(card_frame, bg=self.colors["card"])
        button_container.pack(pady=5)

        ttk.Button(button_container, text="Register", style="Accent.TButton",
                  command=lambda: self.register_user(username_entry, password_entry, confirm_password_entry, email_entry),
                  width=button_width).pack(pady=5, ipady=3)

        back_button = ttk.Button(content_frame, text="Main Menu", style="TButton",
                               command=lambda: self.show_frame("main_menu"),
                               width=button_width)
        back_button.pack(pady=5, ipady=3)

        self.frames["register"] = register_frame
        
    def create_identity_frame(self):
        identity_frame = tk.Frame(self.window, bg=self.colors["background"])
        identity_frame.pack(fill="both", expand=True)

        header_frame = tk.Frame(identity_frame, bg=self.colors["primary"], height=120)
        header_frame.pack(fill="x")
        
        title_label = ttk.Label(header_frame, 
                              text="User Profile", 
                              font=("Segoe UI", 20, "bold"),
                              foreground="white",
                              background=self.colors["primary"])
        title_label.place(relx=0.5, rely=0.5, anchor="center")

        content_frame = tk.Frame(identity_frame, bg=self.colors["background"])
        content_frame.pack(fill="both", expand=True, padx=40, pady=30)
        
        left_column = tk.Frame(content_frame, bg=self.colors["background"], width=450)
        left_column.pack(side="left", fill="both", padx=(0, 20))

        right_column = tk.Frame(content_frame, bg=self.colors["background"], width=450)
        right_column.pack(side="right", fill="both")

        profile_card = tk.Frame(left_column, bg=self.colors["card"], 
                              highlightbackground=self.colors["divider"],
                              highlightthickness=1,
                              relief="ridge", 
                              bd=1)
        profile_card.pack(fill="x", pady=20, ipady=20)

        info_header = ttk.Label(profile_card, 
                              text="Account Information", 
                              style="ProfileTitle.TLabel")
        info_header.pack(anchor="nw", padx=30, pady=(20, 15))
        
        header_divider = ttk.Separator(profile_card, orient="horizontal")
        header_divider.pack(fill="x", padx=30, pady=5)
        
        info_frame = tk.Frame(profile_card, bg=self.colors["card"])
        info_frame.pack(fill="x", padx=30)

        info_grid = tk.Frame(info_frame, bg=self.colors["card"])
        info_grid.pack(fill="x", pady=10)

        ttk.Label(info_grid, text="Username:", style="ProfileInfo.TLabel", width=15).grid(row=0, column=0, sticky="w", pady=10)
        self.username_label = ttk.Label(info_grid, text="", style="ProfileInfo.TLabel")
        self.username_label.grid(row=0, column=1, sticky="w", pady=10)
        
        ttk.Label(info_grid, text="Email:", style="ProfileInfo.TLabel", width=15).grid(row=1, column=0, sticky="w", pady=10)
        self.email_label = ttk.Label(info_grid, text="", style="ProfileInfo.TLabel")
        self.email_label.grid(row=1, column=1, sticky="w", pady=10)
        
        ttk.Label(info_grid, text="Registration Date:", style="ProfileInfo.TLabel", width=15).grid(row=2, column=0, sticky="w", pady=10)
        self.registration_date_label = ttk.Label(info_grid, text="", style="ProfileInfo.TLabel")
        self.registration_date_label.grid(row=2, column=1, sticky="w", pady=10)

        face_card = tk.Frame(right_column, bg=self.colors["card"], 
                           highlightbackground=self.colors["divider"],
                           highlightthickness=1,
                           relief="ridge", 
                           bd=1)
        face_card.pack(fill="x", pady=20, ipady=20)

        face_header = ttk.Label(face_card, 
                              text="Face Recognition Settings", 
                              style="ProfileTitle.TLabel")
        face_header.pack(anchor="nw", padx=30, pady=(20, 15))

        face_divider = ttk.Separator(face_card, orient="horizontal")
        face_divider.pack(fill="x", padx=30, pady=5)

        face_frame = tk.Frame(face_card, bg=self.colors["card"])
        face_frame.pack(fill="x", padx=30, pady=10)
        
        face_register_button = ttk.Button(face_frame, 
                                       text="Register Face", 
                                       style="Success.TButton", 
                                       command=self.register_face_for_current_user,
                                       width=25)
        face_register_button.pack(pady=10, ipady=5, fill="x")

        update_button = ttk.Button(face_frame, 
                                 text="Update Face Data", 
                                 style="TButton", 
                                 command=self.update_face_data,
                                 width=25)
        update_button.pack(pady=10, ipady=5, fill="x")

        delete_button = ttk.Button(face_frame, 
                                 text="Delete Face Data", 
                                 style="Danger.TButton", 
                                 command=self.delete_face_data,
                                 width=25)
        delete_button.pack(pady=10, ipady=5, fill="x")

        nav_frame = tk.Frame(identity_frame, bg=self.colors["background"])
        nav_frame.place(relx=0.5, rely=0.85, anchor="center")
        
        back_button = ttk.Button(nav_frame, 
                               text="Main Menu", 
                               style="TButton",
                               command=lambda: self.show_frame("main_menu"),
                               width=15)
        back_button.pack(pady=5, ipady=5)

        logout_button = ttk.Button(nav_frame, 
                                 text="Logout", 
                                 style="Danger.TButton",
                                 command=self.logout_user,
                                 width=15)
        logout_button.pack(pady=5, ipady=5)

        self.frames["identity"] = identity_frame

    def edit_profile(self):
        if self.repository.isLoggedIn:
            user = self.repository.currentUser
            messagebox.showinfo("Info", "Profile editing feature coming soon!")
        else:
            messagebox.showerror("Error", "Please login first.")

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()  
        self.frames[frame_name].pack(fill="both", expand=True)  
        
        if frame_name == "identity" and self.repository.isLoggedIn:
            user = self.repository.currentUser
            self.username_label.config(text=f"Username: {user.username}")
            self.email_label.config(text=f"Email: {user.mail}")
            self.registration_date_label.config(text=f"Registration Date: {user.registration_date}")

    def register_user(self, username_entry, password_entry, confirm_password_entry, email_entry):
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        mail = email_entry.get()

        if not username or not password or not confirm_password or not mail:
            messagebox.showerror("Error", "All fields are required!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if self.check_username_exists(username):
            messagebox.showerror("Error", "Username already exists!")
            return

        is_valid, error_message = self.validate_password(password)
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return

        code = self.repository.send_email_verification_code(mail)

        user_input = simpledialog.askstring("Email Verification", f"Enter the 6-digit code sent to {mail}:")

        if user_input == code:
            user = User(username, password, mail)
            self.repository.register(user)
            messagebox.showinfo("Success", "Verification successful, user registered!")
            self.show_frame("login")
        else:
            messagebox.showerror("Error", "Invalid verification code! Registration cancelled.")

    def login_user(self, username_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required!")
            return

        self.repository.login(username, password)
        if self.repository.isLoggedIn:
            messagebox.showinfo("Success", "Login successful")
            self.show_frame("identity")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def logout_user(self):
        self.repository.logout()
        messagebox.showinfo("Success", "Logged out successfully")
        self.show_frame("main_menu")
    
    def update_face_data(self):
        user = self.repository.currentUser
        if not user or not user.face_id:
            messagebox.showerror("Error", "Please register your face first.")
            return

        self.repository.delete_face_data(user.face_id)

        from app.face_register import register_face
        register_face(user.face_id)
        self.train_face_model()

        messagebox.showinfo("Success", "Face data updated successfully.")

    def delete_face_data(self):
        user = self.repository.currentUser
        if not user or not user.face_id:
            messagebox.showerror("Error", "No face data found.")
            return

        self.repository.delete_face_data(user.face_id)
        user.face_id = None
        self.repository.save_to_file()
        self.train_face_model()

        messagebox.showinfo("Success", "Face data deleted successfully.")

    def create_forgot_password_frame(self):
        frame = tk.Frame(self.window, bg=self.colors["background"])
        frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(frame, bg=self.colors["background"], width=500)
        left_frame.pack(side="left", fill="both", expand=True)
        
        right_frame = tk.Frame(frame, bg=self.colors["background"], width=500)
        right_frame.pack(side="right", fill="both", expand=True)
        
        left_frame.pack_propagate(False)
        right_frame.pack_propagate(False)
  
        illustration_container = tk.Frame(left_frame, bg=self.colors["background"])
        illustration_container.place(relx=0.5, rely=0.5, anchor="center")
        
        if self.illustration_image:
            illustration_label = tk.Label(illustration_container, image=self.illustration_image, bg=self.colors["background"])
            illustration_label.pack(padx=20)
        else:
            
            placeholder = tk.Label(illustration_container, 
                                 text="Face Recognition System", 
                                 font=("Segoe UI", 24, "bold"),
                                 fg=self.colors["primary"],
                                 bg=self.colors["background"])
            placeholder.pack(pady=50)
            
            subtitle = tk.Label(illustration_container, 
                              text="Secure and easy access", 
                              font=("Segoe UI", 16),
                              fg=self.colors["text_secondary"],
                              bg=self.colors["background"])
            subtitle.pack()

        content_frame = tk.Frame(right_frame, bg=self.colors["background"])
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        header = ttk.Label(content_frame, text="Forgot Password", style="Title.TLabel")
        header.pack(pady=(0, 10))
        
        subheader = ttk.Label(content_frame, text="Enter your email to reset your password", style="Subtitle.TLabel")
        subheader.pack(pady=(0, 20))

        card_frame = tk.Frame(content_frame, bg=self.colors["card"], 
                            highlightbackground=self.colors["divider"],
                            highlightthickness=1,
                            relief="ridge", 
                            bd=1)
        card_frame.pack(padx=20, pady=10, ipadx=20, ipady=20)

        form = tk.Frame(card_frame, bg=self.colors["card"])
        form.pack(pady=5)

        email_frame = tk.Frame(form, bg=self.colors["card"])
        email_frame.pack(fill="x", pady=5)
        
        ttk.Label(email_frame, text="Email:", style="TLabel", background=self.colors["card"]).pack(anchor="w", pady=(0, 2))
        email_entry = ttk.Entry(email_frame, width=25)
        email_entry.pack(fill="x", ipady=3)

        code_frame = tk.Frame(form, bg=self.colors["card"])
        code_frame.pack(fill="x", pady=5)
        
        ttk.Label(code_frame, text="Code:", style="TLabel", background=self.colors["card"]).pack(anchor="w", pady=(0, 2))
        code_entry = ttk.Entry(code_frame, width=25)
        code_entry.pack(fill="x", ipady=3)

        password_frame = tk.Frame(form, bg=self.colors["card"])
        password_frame.pack(fill="x", pady=5)
        
        ttk.Label(password_frame, text="New Password:", style="TLabel", background=self.colors["card"]).pack(anchor="w", pady=(0, 2))
        new_password_entry = ttk.Entry(password_frame, show="*", width=25)
        new_password_entry.pack(fill="x", ipady=3)

        instructions_frame = tk.Frame(card_frame, bg=self.colors["card"])
        instructions_frame.pack(fill="x", pady=5)
        
        instructions = ttk.Label(instructions_frame, 
                               text="1. Enter your email and click 'Send Code'\n2. Enter the code sent to your email\n3. Enter your new password",
                               foreground=self.colors["text_secondary"],
                               background=self.colors["card"],
                               justify="left")
        instructions.pack(pady=5, padx=5, anchor="w")

        button_width = 15
        button_container = tk.Frame(card_frame, bg=self.colors["card"])
        button_container.pack(pady=10)

        ttk.Button(button_container, text="Send Code", style="TButton",
                  command=lambda: self.send_reset_code(email_entry, code_entry, new_password_entry),
                  width=button_width).pack(pady=5, ipady=3, side="left", padx=5)

        self.reset_button = ttk.Button(button_container, text="Reset Password", style="Accent.TButton",
                                      command=lambda: self.reset_password(email_entry, code_entry, new_password_entry),
                                      width=button_width)
        self.reset_button.pack(pady=5, ipady=3, side="left", padx=5)

        back_button = ttk.Button(content_frame, text="Main Menu", style="TButton",
                               command=lambda: self.show_frame("main_menu"),
                               width=button_width)
        back_button.pack(pady=10, ipady=3)

        self.frames["forgot_password"] = frame

    def send_reset_code(self, email_entry, code_entry, new_password_entry):
        email = email_entry.get()
        
        if not email:
            messagebox.showerror("Error", "Please enter your email address.")
            return
            
        email_exists = False
        for user in self.repository.users:
            if user.mail == email:
                email_exists = True
                break
                
        if not email_exists:
            messagebox.showerror("Error", "Email not found in our records.")
            return
            
        reset_code = self.repository.generate_reset_code()
        result = self.repository.send_reset_code(email)
        
        if result:
            messagebox.showinfo("Success", f"Verification code has been sent to {email}.")
            code_entry.delete(0, tk.END)
            code_entry.focus()
        else:
            messagebox.showerror("Error", "Failed to send verification code.")
    
    def reset_password(self, email_entry, code_entry, new_password_entry):
        """Reset user password with verification code"""
        email = email_entry.get()
        code = code_entry.get()
        new_password = new_password_entry.get()
        
        if not email or not code or not new_password:
            messagebox.showerror("Error", "All fields are required.")
            return
            
        is_valid, error_message = self.validate_password(new_password)
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return
            
        result = self.repository.verify_reset_code(email, code)
        
        if result:
            self.repository.reset_password(email, new_password)
            messagebox.showinfo("Success", "Password has been reset successfully. You can now login with your new password.")
            self.show_frame("login")
        else:
            messagebox.showerror("Error", "Invalid or expired verification code.")

    def download_illustration(self):
        """Download a placeholder illustration if the local image is not available"""
        try:
            if not os.path.exists("data"):
                os.makedirs("data")
                
            img = Image.new('RGB', (450, 450), color=(73, 109, 137))
            img.save(os.path.join("data", "illustration.png"))
            
            img = img.resize((450, 450), Image.LANCZOS)
            self.illustration_image = ImageTk.PhotoImage(img)
            print("Created placeholder illustration")
        except Exception as e:
            print(f"Error creating illustration: {e}")
            self.illustration_image = None

    def exit_application(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.window.destroy()

    def run(self):
        self.window.mainloop()