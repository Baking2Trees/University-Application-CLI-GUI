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

