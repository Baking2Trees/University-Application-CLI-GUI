"""University Application CLI and GUI system."""
# pylint: disable=missing-class-docstring,missing-function-docstring,too-few-public-methods,broad-exception-caught,no-else-return

import sys
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
        except Exception:
            print("Database file could not be loaded. Starting with empty data.")
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
    if not password[0].isupper():
        return False

    letters = re.findall(r"[a-zA-Z]", password)
    if len(letters) < 5:
        return False

    if not password[-3:].isdigit():
        return False

    return True

def sync_student_to_file(current_student):
    all_students = Database.load_all_students()
    for i, student in enumerate(all_students):
        if student.id == current_student.id:
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
    def __init__(self):
        self.students = Database.load_all_students()

    def run(self):
        while True:
            print("")
            print("=============================================")
            print("      UNIVERSITY SYSTEM MAIN MENU")
            print("=============================================")
            print("(A) Admin Subsystem")
            print("(S) Student Subsystem")
            print("(X) Exit Application")
            choice = input("==========> System Select: ").strip().lower()

            if choice == "a":
                self.admin_menu()
            elif choice == "s":
                self.student_subsystem()
            elif choice == "x":
                print("Exiting... Thank You.")
                sys.exit()
            else:
                print("Invalid option.")

    def admin_menu(self):
        while True:
            print("")
            print("--- ADMIN SYSTEM MENU ---")
            print("(c) Clear Database")
            print("(g) Group Students By Grade")
            print("(p) Partition Students Into Pass/Fail")
            print("(r) Remove A Student")
            print("(s) Show All Students")
            print("(b) Back to Main Menu")
            print("(x) Exit Application")
            choice = input("==========> Admin Select: ").strip().lower()

            self.students = Database.load_all_students()

            if choice == "s":
                self.view_all_students()
            elif choice == "p":
                self.categorize_pass_fail()
            elif choice == "g":
                self.group_students() # This is the Grouping logic
            elif choice == "r":
                self.remove_student()
            elif choice == "c":
                self.clear_database()
            elif choice == "b":
                break
            elif choice == "x":
                print("Exiting application...")
                sys.exit()
            else:
                print("Invalid option.")

    def view_all_students(self):
        print("")
        print("Student List")
        if len(self.students) == 0:
            print("< Nothing to Display >")
        for s in self.students:
            print(s.name + " : " + s.id + " --> Email: " + s.email)

    def categorize_pass_fail(self):
        print("")
        print("PASS/FAIL Partition")
        pass_list = []
        fail_list = []
        for s in self.students:
            avg = s.get_average_mark()
            info = s.name + " (" + s.id + ")"
            if avg >= 50:
                pass_list.append(info)
            else:
                fail_list.append(info)
        print("FAIL -> " + str(fail_list))
        print("PASS -> " + str(pass_list))

    def group_students(self):
        print("")
        print("Grade Grouping")
        if len(self.students) == 0:
            print("< Nothing to Display >")
            return

        groups = {"HD": [], "D": [], "C": [], "P": [], "Z": []}
        temp_sub = Subject()
        for s in self.students:
            avg = s.get_average_mark()
            grade = temp_sub.calculate_grades(avg)
            groups[grade].append(
                f"{s.name} :: {s.id} --> GRADE: {grade} - MARK: {avg:.2f}"
            )

        order = ["HD", "D", "C", "P", "Z"]

        for g in order:
            if len(groups[g]) > 0:
                print(f"\n{g} -->")
                for entry in groups[g]:
                    print("  " + entry)

    def remove_student(self):
        sid = input("Remove by ID: ")
        found = False
        for s in self.students:
            if s.id == sid:
                found = True
                confirm = input("Are you sure? (y/n): ").strip().lower()
                if confirm == "y":
                    self.students.remove(s)
                    Database.save_all_students(self.students)
                    print("Removing Student " + sid + " Account...")
                elif confirm == "n":
                    print("Operation cancelled...")
                else:
                    print("Invalid input! Please enter y or n...")
                break
        if not found:
            print("Student " + sid + " does not exist")

    def clear_database(self):
        confirm = input("Are you sure? (y/n): ").strip().lower()
        if confirm == "y":
            Database.clear_all_students()
            print("Students data cleared.")
        elif confirm == "n":
            print("Operation cancelled...")
        else:
            print("Invalid input! Please enter y or n...")

    def student_subsystem(self):
        while True:
            print("")
            print("--- STUDENT SYSTEM MENU ---")
            print("(l) Login")
            print("(r) Register")
            print("(b) Back to Main Menu")
            print("(x) Exit Application")
            choice = input("==========> Student Select: ").strip().lower()

            if choice == "r":
                self.register_student()
            elif choice == "l":
                logged_in = self.login_student()
                if logged_in is not None:
                    print("")
                    print("Student logged in successfully!")
                    self.student_course_menu(logged_in)
            elif choice == "b":
                break
            elif choice == "x":
                print("Exiting application...")
                sys.exit()
            else:
                print("Invalid option.")

    def register_student(self):
        print("")
        print("Student Sign Up")

        email = input("Email: ")
        password = input("Password: ")

        # 1: Validate format
        if not (validate_email(email) and validate_password(password)):
            print("Incorrect email or password format. Please try again.")
            return

        # 2: Check for duplicates
        self.students = Database.load_all_students()
        for s in self.students:
            if s.email == email:
                print("Student " + s.name + " already exists")
                return

        # 3: Only now show success message
        print("Email and password formats acceptable")

        name = input("Name: ")
        new_s = Student(name, email, password)
        self.students.append(new_s)
        Database.save_all_students(self.students)

        print("Enrolling Student " + name)

    def login_student(self):
        print("")
        print("Student Sign In")
        email = input("Email: ")
        password = input("Password: ")
        self.students = Database.load_all_students()
        for s in self.students:
            if s.email == email and s.password == password:
                return s
        print("Student does not exist")
        return None

    def student_course_menu(self, student):
        while True:
            print("")
            print("--- STUDENT SUBJECT ENROLMENT MENU ---")
            print("(c) Change Password")
            print("(e) Enrol in a Subject (Max: 4)")
            print("(r) Remove a Subject")
            print("(s) Show Enroled Subjects")
            print("(b) Back to Main Menu")
            print("(x) Exit Application")
            choice = input("==========> Student Select: ").strip().lower()

            if choice == "e":
                self.enrol_subject(student)
            elif choice == "r":
                self.remove_subject(student)
            elif choice == "s":
                self.view_enrolments(student)
            elif choice == "c":
                self.change_password(student)
            elif choice == "b":
                break
            elif choice == "x":
                print("Exiting application...")
                sys.exit()
            else:
                print("Invalid option.")

    def enrol_subject(self, student):
        if len(student.subjects) >= 4:
            print("Students are allowed to enrol in 4 subjects only")
        else:
            new_sub = Subject()
            student.subjects.append(new_sub)
            sync_student_to_file(student)
            print("Enrolling in Subject-" + new_sub.id)
            print("You are now enrolled in " + str(len(student.subjects)) + " out of 4 subjects")

    def remove_subject(self, student):
        sid = input("Remove Subject by ID: ")
        found = False
        for sub in student.subjects:
            if sub.id == sid:
                student.subjects.remove(sub)
                sync_student_to_file(student)
                print("Dropping Subject-" + sid)
                found = True
                break
        if not found:
            print("Subject not found")

    def view_enrolments(self, student):
        print("Showing " + str(len(student.subjects)) + " subjects")
        for sub in student.subjects:
            print(sub)

    def change_password(self, student):
        new_p = input("New Password: ")
        conf_p = input("Confirm Password: ")
        if new_p == conf_p and validate_password(new_p):
            student.password = new_p
            sync_student_to_file(student)
            print("Password updated successfully")
        else:
            print("Passwords do not match or invalid format")

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

        if not validate_email(email):
            messagebox.showerror("Error", "Incorrect email format")
            return

        students = Database.load_all_students()

        for s in students:
            if s.email == email and s.password == pwd:
                self.current_student = s
                self.show_enrol_screen()
                return

        messagebox.showerror("Error", "Invalid credentials")

    def show_enrol_screen(self):
        # unbind 'Enter' after login screen
        self.root.unbind("<Return>")

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

        if sid is None:
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

        if new_p is None or conf_p is None:
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
            except Exception:
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
