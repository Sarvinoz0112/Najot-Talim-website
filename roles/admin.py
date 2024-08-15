import random
import json
from decimal import Decimal
from datetime import datetime

def save_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
        
def load_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def generate_login():
    return f'user{random.randint(1000, 9999)}'

def generate_password():
    return f'pass{random.randint(1000, 9999)}'

def create_group():
    groups = load_data('groups.json')
    
    name = input("Group name: ")
    teacher = input("Teacher: ")
    
    while True:
        try:
            max_student = int(input("Maximum number of students: "))
            if max_student <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer.")
    
    while True:
        start_time = input("Start time (YYYY-MM-DD HH:MM:SS): ")
        end_time = input("End time (YYYY-MM-DD HH:MM:SS): ")
        
        try:
            start_time_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_time_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            if start_time_dt >= end_time_dt:
                print("Start time must be before end time.")
            else:
                break
        except ValueError:
            print("Invalid time format. Please use YYYY-MM-DD HH:MM:SS format.")
    
    status = input("Status: ")
    
    new_group = {
        "name": name,
        "teacher": teacher,
        "max_student": max_student,
        "start_time": start_time,
        "end_time": end_time,
        "status": status,
        "students": []
    }
    
    groups.append(new_group)
    save_data(groups, 'groups.json')
    print(f"Group '{name}' created.")

def view_groups():
    groups = load_data('groups.json')
    if not groups:
        print("No groups found.")
    else:
        for group in groups:
            print(f"Name: {group['name']}, Teacher: {group['teacher']}, "
                  f"Start Time: {group['start_time']}, End Time: {group['end_time']}, "
                  f"Students: {len(group['students'])}/{group['max_student']}, Status: {group['status']}")

def delete_group():
    groups = load_data('groups.json')
    while True:
        group_name = input("Enter the name of the group to delete: ")
        if any(group['name'] == group_name for group in groups):
            break
        else:
            print("No group found with that name. Please try again.")
    
    updated_groups = [group for group in groups if group['name'] != group_name]
    save_data(updated_groups, 'groups.json')
    print(f"Group '{group_name}' deleted.")

def create_student():
    students = load_data('students.json')
    
    full_name = input("Full name: ")
    gmail = input("Gmail: ")
    
    while True:
        phone = input("Phone number: ")
        if phone.isdigit():
            break
        else:
            print("Please enter a valid phone number (digits only).")
    
    gender = input("Gender: ")
    
    while True:
        try:
            age = int(input("Age: "))
            if age <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer for age.")
    
    login = generate_login()
    password = generate_password()
    
    new_student = {
        "full_name": full_name,
        "gmail": gmail,
        "phone": phone,
        "gender": gender,
        "age": age,
        "login": login,
        "password": password,
        "balance": Decimal('0.00')
    }
    
    students.append(new_student)
    save_data(students, 'students.json')
    print(f"Student created: {full_name} | Login: {login} | Password: {password}")

def view_students():
    students = load_data('students.json')
    if not students:
        print("No students found.")
    else:
        for student in students:
            print(f"Name: {student['full_name']}, Login: {student['login']}, Balance: {student['balance']}")

def delete_student():
    students = load_data('students.json')
    while True:
        student_login = input("Enter the login of the student to delete: ")
        if any(student['login'] == student_login for student in students):
            break
        else:
            print("No student found with that login. Please try again.")
    
    updated_students = [student for student in students if student['login'] != student_login]
    save_data(updated_students, 'students.json')
    print(f"Student with login '{student_login}' deleted.")

def add_student_to_group():
    students = load_data('students.json')
    groups = load_data('groups.json')
    
    while True:
        student_login = input("Enter the login of the student to add: ")
        student = next((s for s in students if s['login'] == student_login), None)
        if student:
            break
        else:
            print("No student found with that login. Please try again.")
    
    while True:
        group_name = input("Enter the name of the group: ")
        group = next((g for g in groups if g['name'] == group_name), None)
        if group:
            break
        else:
            print("No group found with that name. Please try again.")
    
    if len(group['students']) < group['max_student']:
        group['students'].append(student_login)
        save_data(groups, 'groups.json')
        print(f"Student '{student_login}' added to group '{group_name}'.")
    else:
        print(f"Group '{group_name}' is full.")

def search_student():
    students = load_data('students.json')
    search_key = input("Enter student name or login to search: ")
    
    result = [s for s in students if search_key in s['full_name'] or search_key == s['login']]
    
    if result:
        for student in result:
            print(f"Name: {student['full_name']}, Login: {student['login']}, Gmail: {student['gmail']}, Balance: {student['balance']}")
    else:
        print("No student found.")

def accept_payment():
    students = load_data('students.json')
    
    while True:
        student_login = input("Enter the login of the student for payment: ")
        student = next((s for s in students if s['login'] == student_login), None)
        if student:
            break
        else:
            print("No student found with that login. Please try again.")
    
    while True:
        try:
            amount = Decimal(input("Enter payment amount: "))
            if amount < 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive amount.")
    
    student['balance'] += amount
    save_data(students, 'students.json')
    print(f"Added {amount} to the balance of student '{student_login}'.")

def admin_menu():
    while True:
        print("\nAdmin Menu")
        print("1. Create Group")
        print("2. View Groups")
        print("3. Delete Group")
        print("4. Create Student")
        print("5. View Students")
        print("6. Delete Student")
        print("7. Add Student to Group")
        print("8. Search Students")
        print("9. Accept Payment")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            create_group()
        elif choice == '2':
            view_groups()
        elif choice == '3':
            delete_group()
        elif choice == '4':
            create_student()
        elif choice == '5':
            view_students()
        elif choice == '6':
            delete_student()
        elif choice == '7':
            add_student_to_group()
        elif choice == '8':
            search_student()
        elif choice == '9':
            accept_payment()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    admin_menu()
