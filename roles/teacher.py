import json
from datetime import datetime

from admin import view_groups as admin_view_groups
from manegers.con_manager import open_file


def load_data(filename):
    '''Load data from a JSON file, returning an empty list if the file is not found.'''
    try:
        with open_file(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def load_groups():
    '''Load groups from a JSON file and convert date strings to datetime objects.'''
    groups = load_data('groups.json')
    for item in groups:
        item['start_time'] = datetime.strptime(item['start_time'], "%Y-%m-%d %H:%M:%S")
        item['end_time'] = datetime.strptime(item['end_time'], "%Y-%m-%d %H:%M:%S")
        item['students'] = [str(student) for student in item.get('students', [])]
    return groups


groups = load_groups()


def teacher_login():
    '''Handle teacher login by checking username and password against the stored data.'''
    teachers = load_data('users.json')

    username = input("Enter teacher username: ")
    password = input("Enter teacher password: ")

    for teacher in teachers:
        if teacher['username'] == username and teacher['password'] == password:
            print("Login successful!")
            teacher_menu(username)
            return
    print("Invalid username or password!")


class Teacher:
    def __init__(self, username):
        '''Initialize a Teacher object with a username.'''
        self.username = username

    def view_groups(self):
        '''View all groups using the admin view_groups function.'''
        admin_view_groups()

    def view_students_by_group(self, group_name):
        '''View students in a specific group.'''
        group = next((g for g in groups if g['name'] == group_name), None)
        if group:
            print(f"Students in {group_name}:")
            for student in group['students']:
                print(f"- {student}")
        else:
            print(f"Group {group_name} does not exist.")

    def start_lesson(self):
        '''Start a lesson for a chosen group and provide options to end the lesson or go back.'''
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
        '''End a lesson for the specified group.'''
        print(f"Lesson for {group_name} has been ended.")


def teacher_menu(username):
    '''Display the teacher menu and handle user choices.'''
    teacher = Teacher(username)
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
