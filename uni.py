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
