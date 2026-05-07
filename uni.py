import random
import re
import pickle
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# ==========================================
# PART 1: MODELS
# ==========================================

class Student:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        # Create a 6-digit ID
        self.id = str(random.randint(1, 999999))
        while len(self.id) < 6:
            self.id = "0" + self.id
        self.subjects = []

    def get_average_mark(self):
        if len(self.subjects) == 0:
            return 0
        total_mark = 0
        for sub in self.subjects:
            total_mark = total_mark + sub.mark
        return total_mark / len(self.subjects)

class Subject:
    def __init__(self):
        # Create a 3-digit ID
        self.id = str(random.randint(1, 999))
        if len(self.id) == 1:
            self.id = "00" + self.id
        elif len(self.id) == 2:
            self.id = "0" + self.id

        self.mark = random.randint(25, 100)
        self.grade = self.calculate_grades(self.mark)

    def calculate_grades(self, mark):
        if mark >= 85:
            return "HD"
        elif mark >= 75:
            return "D"
        elif mark >= 65:
            return "C"
        elif mark >= 50:
            return "P"
        else:
            return "Z"

    def __str__(self):
        return f"[ Subject::{self.id} -- mark = {self.mark} -- grade = {self.grade:>2} ]"

# ==========================================
# PART 2: DATABASE TOOLS
# ==========================================

class Database:
    FILE_NAME = "students.data"

    @staticmethod
    def save_all_students(students_list):
        with open(Database.FILE_NAME, "wb") as f:
            pickle.dump(students_list, f)

    @staticmethod
    def load_all_students():
        if not os.path.exists(Database.FILE_NAME):
            Database.save_all_students([])
            return []

        try:
            with open(Database.FILE_NAME, "rb") as f:
                return pickle.load(f)
        except:
            return []

    @staticmethod
    def clear_all_students():
        Database.save_all_students([])

# ==========================================
# PART 3: UTILITIES
# ==========================================

def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@student\.uni\.edu\.au$"
    if re.match(pattern, email):
        return True
    return False

def validate_password(password):
    if len(password) < 8:
        return False
    if password[0].isupper() == False:
        return False

    letters = re.findall(r"[a-zA-Z]", password)
    if len(letters) < 5:
        return False

    if password[-3:].isdigit() == False:
        return False

    return True

def sync_student_to_file(current_student):
    all_students = Database.load_all_students()
    for i in range(len(all_students)):
        if all_students[i].id == current_student.id:
            all_students[i] = current_student
            break
    Database.save_all_students(all_students)

def generate_test_data():
    existing = Database.load_all_students()

    if len(existing) > 0:
        print()
        print("Database already has data. Overwriting...")

    s1 = Student("Somesh", "somesh@student.uni.edu.au", "Paaaa123")
    s2 = Student("Kelly", "kelly@student.uni.edu.au", "Paaaa123")
    s3 = Student("Madhava", "madhava@student.uni.edu.au", "Paaaa123")
    s4 = Student("Sahil", "sahil@student.uni.edu.au", "Secure123")

    s1.subjects.append(Subject())
    s1.subjects.append(Subject())

    s2.subjects.append(Subject())

    s3.subjects.append(Subject())
    s3.subjects.append(Subject())

    s4.subjects.append(Subject())

    Database.save_all_students([s1, s2, s3, s4])

    print(" ✅ Test data saved to students.data")
    students = Database.load_all_students()
    print("Number of students:", len(students))

def read_database():
    students = Database.load_all_students()
    print("Number of students:", len(students))
    for s in students:
        print("-", s.name, s.email)

def clear_database():
    Database.clear_all_students()
    print("Database cleared.")

# ==========================================
# PART 4: CONTROLLER (CLI)
# ==========================================

class CLIUniApp:
    pass

# ==========================================
# PART 5: VIEW (GUI)
# ==========================================

class GUIUniApp:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.title("GUIUniApp")
            self.root.geometry("500x400")
            self.current_student = None
            self.show_login_screen()
        except:
            print("GUI error: No display found.")
            raise

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()

        tk.Label(
            self.root,
            text="STUDENT LOGIN",
            font=("Arial", 18, "bold")
        ).pack(pady=25)

        tk.Label(self.root, text="Email:", font=("Arial", 11)).pack()
        self.email_entry = tk.Entry(self.root, width=35)
        self.email_entry.pack(pady=5, ipady=3)

        tk.Label(self.root, text="Password:", font=("Arial", 11)).pack()
        self.pass_entry = tk.Entry(self.root, show="*", width=35)
        self.pass_entry.pack(pady=5, ipady=3)

        tk.Button(
            self.root,
            text="Login",
            width=15,
            command=self.login_student
        ).pack(pady=20)

        self.root.bind("<Return>", lambda event: self.login_student())

    def login_student(self):
        email = self.email_entry.get()
        pwd = self.pass_entry.get()

        if email == "" or pwd == "":
            messagebox.showerror("Error", "Fields cannot be empty")
            return

        students = Database.load_all_students()
        for s in students:
            if s.email == email and s.password == pwd:
                self.current_student = s
                self.show_enrol_screen()
                return
        messagebox.showerror("Error", "Invalid credentials")

    def show_enrol_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome " + self.current_student.name).pack(pady=10)

        tk.Button(self.root, text="Enrol in Subject", command=self.enrol_subject).pack(pady=5)
        tk.Button(self.root, text="View Enrolments", command=self.view_enrolments).pack(pady=5)
        tk.Button(self.root, text="Remove Subject", command=self.remove_subject).pack(pady=5)
        tk.Button(self.root, text="Change Password", command=self.change_password).pack(pady=5)

        tk.Button(self.root, text="Logout", command=self.show_login_screen).pack(pady=20)

    def enrol_subject(self):
        if len(self.current_student.subjects) >= 4:
            messagebox.showwarning("Error", "Max 4 subjects allowed")
            return

        new_sub = Subject()
        self.current_student.subjects.append(new_sub)
        sync_student_to_file(self.current_student)

        messagebox.showinfo("Success", "Enrolled in Subject " + new_sub.id)

    def view_enrolments(self):
        sub_win = tk.Toplevel(self.root)
        sub_win.title("My Subjects")
        if len(self.current_student.subjects) == 0:
            tk.Label(sub_win, text="No subjects enrolled.").pack()
        else:
            for sub in self.current_student.subjects:
                tk.Label(sub_win, text=str(sub)).pack()
  
    def remove_subject(self):
        sid = simpledialog.askstring("Remove Subject", "Enter Subject ID:")

        if sid == None:
            return

        for sub in self.current_student.subjects:
            if sub.id == sid:
                self.current_student.subjects.remove(sub)
                sync_student_to_file(self.current_student)
                messagebox.showinfo("Success", "Dropping Subject-" + sid)
                return

        messagebox.showerror("Error", "Subject not found")
            
    def change_password(self):
        new_p = simpledialog.askstring("Change Password", "New Password:", show="*")
        conf_p = simpledialog.askstring("Change Password", "Confirm Password:", show="*")

        if new_p == None or conf_p == None:
            return

        if new_p == conf_p and validate_password(new_p):
            self.current_student.password = new_p
            sync_student_to_file(self.current_student)
            messagebox.showinfo("Success", "Password updated successfully")
        else:
            messagebox.showerror("Error", "Passwords do not match or invalid format")

# ==========================================
# PART 6: MAIN
# ==========================================

if __name__ == "__main__":
    while True:
        print("\n======================")
        print("Start (1) CLI, (2) GUI")

        print("\n--- Add-Ons ---")
        print("(3) Generate Test Data")
        print("(4) Read Database")
        print("(5) Clear Database")
        print("(X) Exit")

        mode = input("==========> Select option: ").strip().lower()

        if mode == "1":
            CLIUniApp().run()

        elif mode == "2":
            try:
                app = GUIUniApp()
                app.root.mainloop()
            except:
                print("GUI closed.")

        elif mode == "3":
            print("Generating sample data...")
            generate_test_data()

        elif mode == "4":
            read_database()

        elif mode == "5":
            clear_database()

        elif mode == "x":
            print("Exiting...")
            break

        else:
            print("Invalid option.")