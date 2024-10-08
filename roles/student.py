from admin import save_data as admin_save_data
from admin import view_groups as admin_view_groups
from managers.con_manager import read_data


def load_students():
    '''Load students data from the 'students.json' file.'''
    return read_data('students.json')


def save_students(students):
    '''Save updated students data to the 'students.json' file.'''
    admin_save_data({"students": students}, 'students.json')


def find_student(username, password):
    '''Find and return a student by username from the list of students.'''
    for student in load_students():
        if student['login'] * 1 == username * 1 and password * 1 == student['password'] * 1:
            return student
    return None


def view_groups(student):
    '''Display the groups that the student is a member of.'''
    print("Your Groups:")
    for group in student['groups']:
        print(f"- {group}")


def view_balance(student):
    '''Display the student's current balance.'''
    print(f"Your Balance: ${student['balance']:.2f}")


def get_valid_age():
    '''Prompt the user to enter a valid age (positive integer).'''
    while True:
        try:
            age = int(input("Enter new age: "))
            if age > 0:
                return age
            else:
                print("Age must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer for age.")


def get_valid_email():
    '''Prompt the user to enter a valid email address.'''
    while True:
        email = input("Enter new email: ")
        if (
                email.count('@') == 1 and  # Checks if there is exactly one '@' symbol
                email[0] != '@' and  # Ensures the email doesn't start with '@'
                email.count('.') > 0 and  # Checks if there is at least one '.'
                email.rfind('.') > email.find('@')  # Ensures the last '.' comes after the '@'
        ):
            return email
        else:
            print("Invalid email format. Please enter a valid email address.")


def update_personal_info(student):
    '''Update the student's personal information (name, age, email).'''
    print("Update Personal Information:")
    name = input("Enter new name: ")
    age = get_valid_age()
    email = get_valid_email()

    student['personal_info'] = {
        "name": name,
        "age": age,
        "email": email
    }
    print("Personal information updated successfully!")


def student_menu(username):
    '''Display the student menu and handle user choices.'''
    students = load_students()
    student = find_student(username, students)

    if student is None:
        print("Student not found!")
        return

    while True:
        print("\nStudent Menu:")
        print("1. View All Groups")
        print("2. View Balance")
        print("3. Update Personal Information")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            admin_view_groups(student)
        elif choice == '2':
            view_balance(student)
        elif choice == '3':
            update_personal_info(student)
            save_students(students)
        elif choice == '4':
            break
        else:
            print("Invalid choice! Please try again.")


def student_login():
    '''Handle student login and direct them to the student menu if credentials are valid.'''
    username = input("Enter your id: ").strip()
    password = input("Enter your password: ").strip()
    student = find_student(username=username, password=password)
    print(student)
    if student is None:
        print("Student not found!")
    else:
        student_menu(username)
