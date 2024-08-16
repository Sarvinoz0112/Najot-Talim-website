import json
import random
from datetime import datetime
from decimal import Decimal

from manegers.con_manager import open_file

def read_json():
    try:
        with open_file(filename='users.json') as file:
            json_data = json.load(file)
            return json_data
    except FileNotFoundError:
        with open_file(filename='users.json') as file:
            json.dump({}, file, indent=4)
            return {}

def admin_login():
    all_users: dict = read_json()
    username = input('Username: ').strip().lower()
    password = input('Password: ').strip()
    for user in all_users['admins']:
        if user['username'] == username and user['password'] == password:
            with open_file(filename='users.json', mode='w') as file:
                json.dump(all_users, file, indent=4)
                print("Logged in!")
                main_menu()
        return False


def save_data(data, filename):
    '''Save data to a JSON file with proper handling of Decimal values.'''

    def decimal_default(obj):
        if isinstance(obj, Decimal):
            return float(obj)

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, default=decimal_default)


def load_data(filename):
    '''Load data from a JSON file and convert balance values to Decimal.'''
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            for item in data:
                item['balance'] = Decimal(item['balance'])
            return data
    except FileNotFoundError:
        return []


def generate_login():
    '''Generate a random 6-digit login string.'''
    return f'{random.randint(100000, 999999)}'


def generate_password():
    '''Generate a random 6-digit password string.'''
    return f'{random.randint(100000, 999999)}'


def is_valid_email(email):
    '''Check if the provided email address is valid.'''
    return (
            email.count('@') == 1 and
            email[0] != '@' and
            email.count('.') > 0 and
            email.rfind('.') > email.find('@')
    )


def is_valid_gender(gender):
    '''Check if the provided gender is valid.'''
    valid_genders = ['Male', 'Female']
    return gender in valid_genders


def create_group():
    '''Create a new group with details provided by the user.'''
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
            elif start_time_dt < datetime.now():
                print("Start time must be in the future.")
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
    print(f"Group {name} created.")


def view_groups():
    '''View details of all existing groups.'''
    groups = load_data('groups.json')
    if not groups:
        print("No groups found.")
    else:
        for group in groups:
            print(f"Name: {group['name']}, Teacher: {group['teacher']}, "
                  f"Start Time: {group['start_time']}, End Time: {group['end_time']}, "
                  f"Students: {len(group['students'])}/{group['max_student']}, Status: {group['status']}")


def delete_group():
    '''Delete a group based on the name provided by the user.'''
    groups = load_data('groups.json')
    while True:
        group_name = input("Enter the name of the group to delete: ")
        if any(group['name'] == group_name for group in groups):
            break
        else:
            print("No group with that name found. Please try again.")

    updated_groups = [group for group in groups if group['name'] != group_name]
    save_data(updated_groups, 'groups.json')
    print(f"Group {group_name} deleted.")


def create_student():
    '''Create a new student with details provided by the user.'''
    students = list(load_data('students.json'))

    full_name = input("Full name: ")

    while True:
        gmail = input("Gmail: ")
        if is_valid_email(gmail):
            break
        else:
            print("Invalid email format. Please try again.")

    while True:
        phone = input("Phone number: ")
        if phone.isdigit():
            break
        else:
            print("Please enter a valid phone number.")

    while True:
        gender = input("Gender (Male/Female): ").capitalize()
        if is_valid_gender(gender):
            break
        else:
            print("Invalid gender. Please enter Male or Female.")

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
        "balance": Decimal('0.00'),
        'is_login': False
    }

    students.append(new_student)
    save_data(students, 'students.json')
    print(f"Student created: {full_name} | Login: {login} | Password: {password}")


def view_students():
    '''View details of all existing students.'''
    students = load_data('students.json')
    if not students:
        print("No students found.")
    else:
        for student in students:
            print(f"Name: {student['full_name']}, Login: {student['login']}, Balance: {student['balance']}")


def delete_student():
    '''Delete a student based on the login provided by the user.'''
    students = load_data('students.json')
    while True:
        student_login = input("Enter the login of the student to delete: ")
        if any(student['login'] == student_login for student in students):
            break
        else:
            print("No student with that login found. Please try again.")

    updated_students = [student for student in students if student['login'] != student_login]
    save_data(updated_students, 'students.json')
    print(f"Student with login {student_login} deleted.")


def add_student_to_group():
    '''Add a student to a group if there's space available.'''
    students = load_data('students.json')
    groups = load_data('groups.json')

    while True:
        student_login = input("Enter the login of the student to add: ")
        student = next((s for s in students if s['login'] == student_login), None)
        if student:
            break
        else:
            print("No student with that login found. Please try again.")

    while True:
        group_name = input("Enter the name of the group: ")
        group = next((g for g in groups if g['name'] == group_name), None)
        if group:
            break
        else:
            print("No group with that name found. Please try again.")

    if len(group['students']) < group['max_student']:
        group['students'].append(student_login)
        save_data(groups, 'groups.json')
        print(f"Student {student_login} added to group {group_name}.")
    else:
        print(f"Group {group_name} is full.")


def search_student():
    '''Search for a student by name or login and display their details.'''
    students = load_data('students.json')
    search_key = input("Enter student name or login: ")

    result = [s for s in students if search_key in s['full_name'] or search_key == s['login']]

    if result:
        for student in result:
            print(
                f"Name: {student['full_name']}, Login: {student['login']}, Gmail: {student['gmail']}, Balance: {student['balance']}")
    else:
        print("No student found.")


def accept_payment():
    '''Accept a payment from a student and update their balance.'''
    students = load_data('students.json')

    while True:
        student_login = input("Enter the login of the student to accept payment from: ")
        student = next((s for s in students if s['login'] == student_login), None)
        if student:
            break
        else:
            print("No student with that login found. Please try again.")

    while True:
        try:
            amount = Decimal(input("Enter the payment amount: "))
            if amount < 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive amount.")

    student['balance'] += amount
    save_data(students, 'students.json')
    print(f"{amount} added to the balance of student {student_login}.")


def refill_balance():
    '''Refill a student's balance with a specified amount.'''
    students = load_data('students.json')

    while True:
        student_login = input("Enter the login of the student to refill balance: ")
        student = next((s for s in students if s['login'] == student_login), None)
        if student:
            break
        else:
            print("No student with that login found. Please try again.")

    while True:
        try:
            amount = Decimal(input("Enter the refill amount: "))
            if amount < 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive amount.")

    student['balance'] += amount
    save_data(students, 'students.json')
    print(f"Student {student_login}'s balance refilled by {amount}.")


def get_student_balance():
    '''Display the balance of a student.'''
    students = load_data('students.json')

    while True:
        student_login = input("Enter the login of the student: ")
        student = next((s for s in students if s['login'] == student_login), None)
        if student:
            print(f"Student {student_login}'s balance: {student['balance']}")
            break
        else:
            print("No student with that login found. Please try again.")


def view_groups():
    '''View details of all existing groups.'''
    groups = load_data('groups.json')
    if not groups:
        print("No groups found.")
    else:
        for group in groups:
            print(f"Name: {group['name']}, Teacher: {group['teacher']}, "
                  f"Start Time: {group['start_time']}, End Time: {group['end_time']}, "
                  f"Students: {len(group['students'])}/{group['max_student']}, Status: {group['status']}")


def main_menu():
    '''Display the main menu and handle user input.'''
    while True:
        print("\nMain Menu:")
        print("1. Create Group")
        print("2. View Groups")
        print("3. Delete Group")
        print("4. Create Student")
        print("5. View Students")
        print("6. Delete Student")
        print("7. Add Student to Group")
        print("8. Search Student")
        print("9. Accept Payment")
        print("10. Refill Balance")
        print("11. Get Student Balance")
        print("12. Exit")

        choice = input("Choose an option: ")

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
        elif choice == '10':
            refill_balance()
        elif choice == '11':
            get_student_balance()
        elif choice == '12':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main_menu()
