import json
import os
import bcrypt
from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime
import random
import string
import cv2
import glob

class User:
    def __init__(self, username, password, mail, face_id=None):
        self.username = username
        self.password = password
        self.mail = mail
        self.registration_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.reset_code = None
        self.reset_code_expiry = None
        self.face_id = face_id

class UserRepository:
    def __init__(self):
        self.users = []
        self.isLoggedIn = False
        self.currentUser = {}

        self.loadUsers()

    def loadUsers(self):
        if os.path.exists("secret.key") and not os.path.exists(os.path.join("secrets", "secret.key")):
            if not os.path.exists("secrets"):
                os.makedirs("secrets")
            with open("secret.key", "rb") as old_key_file:
                key_data = old_key_file.read()
                with open(os.path.join("secrets", "secret.key"), "wb") as new_key_file:
                    new_key_file.write(key_data)
            key = key_data
        elif not os.path.exists(os.path.join("secrets", "secret.key")):
            print("Key file not found")
            key = self.generate_key()
            self.save_key(key)
        else:
            key = self.load_key()

        if os.path.exists(os.path.join("data", "users.json")):
            try:
                with open(os.path.join("data", "users.json"), 'r') as file: 
                    data = file.read()
                    if data:
                        try:
                            fernet = Fernet(key)
                            decrypted_data = fernet.decrypt(data.encode()).decode()
                            users = json.loads(decrypted_data)
                            for user_data in users:
                                user = json.loads(user_data)
                                newUser = User(username=user['username'], password=user['password'], mail=user['mail'], face_id=user.get("face_id"))
                                self.users.append(newUser)
                        except InvalidToken:
                            print("Invalid token error")
                            self.users = [] 
                            self.save_to_file() 
            except Exception as e:
                print(f"Error loading users: {e}")
    
    def send_email_verification_code(self, email):
        code = ''.join(random.choices(string.digits, k=6))
        print(f"[DEBUG] {email} Verification code: {code}")  
        return code

    def face_login(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            recognizer.read(os.path.join("data", "trainer.yml"))
        except:
            print("Trainer File Not Found!")
            return None
        cap = cv2.VideoCapture(0)
        authenticated_user = None
        unknown_detected = False
        
        failed_attempts = 0
        max_attempts = 50

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                roi_gray = gray[y:y+h, x:x+w]
                predicted_id, confidence = recognizer.predict(roi_gray)

                print(f"Predicted ID: {predicted_id}, Confidence: {confidence}")
                
                if confidence < 50:
                    matched_user = next((user for user in self.users if user.face_id == predicted_id), None)
                    if matched_user:
                        self.currentUser = matched_user
                        self.isLoggedIn = True
                        authenticated_user = matched_user
                        break
                    else:
                        print("ID recognized but user not found.")
                        unknown_detected = True
                        failed_attempts += 1
                else:
                    print("Face not recognized, confidence value low.")
                    unknown_detected = True
                    failed_attempts += 1
            
            cv2.imshow('Face Recognition', frame)
            
            if failed_attempts >= max_attempts:
                print(f"Maximum recognition attempts ({max_attempts}) reached.")
                break

            if authenticated_user or cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if failed_attempts >= max_attempts:
            return "max_attempts"
        elif not authenticated_user and unknown_detected:
            print("Unidentified face!")
            return "unknown"

        return authenticated_user

    def save_to_file(self):
        list = []
        for user in self.users:
            list.append(json.dumps(user.__dict__))

        encrypted_data = json.dumps(list)
        key = self.load_key()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(encrypted_data.encode()).decode()

        with open(os.path.join("data", "users.json"), 'w') as file:
            file.write(encrypted_data)

        self.save_key(key)

    def generate_key(self):
        return Fernet.generate_key()

    def save_key(self, key):
        if not os.path.exists("secrets"):
            os.makedirs("secrets")
        with open(os.path.join("secrets", "secret.key"), "wb") as key_file:
            key_file.write(key)

    def load_key(self):
        return open(os.path.join("secrets", "secret.key"), "rb").read()

    def register(self, user: User):
        for existing_user in self.users:
            if existing_user.username == user.username:
                print("This username already exists!")
                return False

        hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
        user.password = hashed_password.decode()
        self.users.append(user)
        self.save_to_file()
        print('User registered successfully')
        return True

    def login(self, username, password):
        for user in self.users:
            if user.username == username and bcrypt.checkpw(password.encode(), user.password.encode()):
                self.isLoggedIn = True
                self.currentUser = user
                print('Login successful')
                break

    def logout(self):
        self.isLoggedIn = False
        self.currentUser = {}
        print('Logged out successfully')

    def identity(self):
        if self.isLoggedIn:
            print(f'Username: {self.currentUser.username}')
        else:
            print('Not logged in')
        return self.currentUser

    def generate_reset_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def send_reset_code(self, email):
        for user in self.users:
            if user.mail == email:
                user.reset_code = self.generate_reset_code()
                user.reset_code_expiry = datetime.now().timestamp() + 300  
                print(f"Reset code for {email}: {user.reset_code}") 
                return True
        return False

    def verify_reset_code(self, email, code):
        for user in self.users:
            if user.mail == email and user.reset_code == code:
                if datetime.now().timestamp() < user.reset_code_expiry:
                    return True
        return False

    def reset_password(self, email, new_password):
        for user in self.users:
            if user.mail == email:
                hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                user.password = hashed_password.decode()
                user.reset_code = None
                user.reset_code_expiry = None
                self.save_to_file()
                return True
        return False
      
    def delete_face_data(self, face_id):
        files = glob.glob(f"data/User.{face_id}.*.jpg")
        for file in files:
            os.remove(file)
        print(f"Face data for Face ID {face_id} has been deleted.")