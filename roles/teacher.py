import json
from decimal import Decimal
from datetime import datetime
from contextlib import contextmanager
from admin import view_groups as admin_view_groups

@contextmanager
def open_file(filename, mode):
    try:
        file = open(filename, mode)
        yield file
    finally:
        file.close()

def load_groups():
    try:
        with open_file('groups.json', 'r') as file:
            data = json.load(file)
            for item in data:
                item['start_time'] = datetime.strptime(item['start_time'], "%Y-%m-%d %H:%M:%S")
                item['end_time'] = datetime.strptime(item['end_time'], "%Y-%m-%d %H:%M:%S")
                item['students'] = [str(student) for student in item.get('students', [])]
            return data
    except FileNotFoundError:
        return []

groups = load_groups()

class Teacher:
    def __init__(self, username):
        self.username = username

    def view_groups(self):
        admin_view_groups()

    def view_students_by_group(self, group_name):
        group = next((g for g in groups if g['name'] == group_name), None)
        if group:
            print(f"Students in {group_name}:")
            for student in group['students']:
                print(f"- {student}")
        else:
            print(f"Group {group_name} does not exist.")
    
    def start_lesson(self):
        self.view_groups()
        group_name = input("Select a group: ")
        if next((g for g in groups if g['name'] == group_name), None):
            while True:
                choice = input(f"Starting lesson for {group_name}. Choose an option:\n1. End Lesson\n2. Go Back\n")
                if choice == "1":
                    self.end_lesson(group_name)
                    break
                elif choice == "2":
                    break
                else:
                    print("Invalid choice, please try again.")
        else:
            print(f"Group {group_name} does not exist.")
    
    def end_lesson(self, group_name):
        print(f"Lesson for {group_name} has been ended.")

def teacher_menu():
    teacher = Teacher("teacher1")
    while True:
        print("\nTeacher Menu:")
        print("1. View All Groups")
        print("2. View Students by Group")
        print("3. Start Lesson")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        if choice == "1":
            teacher.view_groups()
        elif choice == "2":
            group_name = input("Enter group name: ")
            teacher.view_students_by_group(group_name)
        elif choice == "3":
            teacher.start_lesson()
        elif choice == "4":
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    teacher_menu()
