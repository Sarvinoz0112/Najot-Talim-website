import json
import smtplib
from email.mime.text import MIMEText

DATA_FILE = 'users.json'

SUPERADMIN_USERNAME = 'superadmin'
SUPERADMIN_PASSWORD = '0000'


def load_data():
    '''Loads data from the JSON file. Returns an empty dictionary if the file is not found.'''
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_data(data):
    '''Saves data to the JSON file.'''
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def validate_email(email):
    '''Validates the format of the email address.'''
    return (
            email.count('@') == 1 and  # Check for exactly one '@'
            email[0] != '@' and  # Check that it does not start with '@'
            email.count('.') > 0 and  # Ensure there is at least one '.'
            email.rfind('.') > email.find('@')  # Last '.' comes after '@'
    )


def superadmin_login():
    '''Prompts for SuperAdmin login credentials and calls the menu function if successful.'''
    username = input("SuperAdmin username: ")
    password = input("SuperAdmin password: ")

    if username == SUPERADMIN_USERNAME and password == SUPERADMIN_PASSWORD:
        superadmin_menu()
    else:
        print("Login failed!")


def superadmin_menu():
    '''Displays the SuperAdmin menu and handles user choices for managing admins, teachers, and sending emails.'''
    while True:
        print("\nSuperAdmin Menu:")
        print("1. Create Admin")
        print("2. View Admins")
        print("3. Delete Admin")
        print("4. Update Admin")
        print("5. Create Teacher")
        print("6. View Teachers")
        print("7. Delete Teacher")
        print("8. Update Teacher")
        print("9. Send Email")
        print("10. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            create_admin()
        elif choice == '2':
            view_admins()
        elif choice == '3':
            delete_admin()
        elif choice == '4':
            update_admin()
        elif choice == '5':
            create_teacher()
        elif choice == '6':
            view_teachers()
        elif choice == '7':
            delete_teacher()
        elif choice == '8':
            update_teacher()
        elif choice == '9':
            send_email()
        elif choice == '10':
            break
        else:
            print("Invalid choice!")


def create_admin():
    '''Prompts for admin details and adds a new admin to the data.'''
    data = load_data()
    admins = data.get('admins', [])

    full_name = input("Full Name: ")
    username = input("Username: ")
    password = input("Password: ")

    new_admin = {'full_name': full_name, 'username': username, 'password': password, 'is_login': False}
    admins.append(new_admin)
    data['admins'] = admins
    save_data(data)
    print("Admin created successfully!")


def view_admins():
    '''Displays a list of all admins.'''
    data = load_data()
    admins = data.get('admins', [])
    for idx, admin in enumerate(admins, start=1):
        print(f"{idx}. {admin['full_name']} ({admin['username']})")


def delete_admin():
    '''Prompts to select an admin to delete and removes it from the data.'''
    data = load_data()
    admins = data.get('admins', [])
    view_admins()

    admin_idx = int(input("Select the number of the Admin to delete: ")) - 1
    if 0 <= admin_idx < len(admins):
        admins.pop(admin_idx)
        data['admins'] = admins
        save_data(data)
        print("Admin deleted successfully!")
    else:
        print("Invalid selection!")


def update_admin():
    '''Prompts to select an admin to update and modifies their details.'''
    data = load_data()
    admins = data.get('admins', [])
    view_admins()

    admin_idx = int(input("Select the number of the Admin to update: ")) - 1
    if 0 <= admin_idx < len(admins):
        admins[admin_idx]['full_name'] = input("New Full Name: ")
        admins[admin_idx]['username'] = input("New Username: ")
        admins[admin_idx]['password'] = input("New Password: ")
        data['admins'] = admins
        save_data(data)
        print("Admin updated successfully!")
    else:
        print("Invalid selection!")


def create_teacher():
    '''Prompts for teacher details and adds a new teacher to the data.'''
    data = load_data()
    teachers = data.get('teachers', [])

    full_name = input("Full Name: ")
    gender = input("Gender (Male/Female): ").capitalize()
    email = input("Email: ")

    if not validate_email(email):
        print("Invalid email address!")
        return

    username = input("Username: ")
    password = input("Password: ")

    new_teacher = {'full_name': full_name, 'gender': gender, 'email': email, 'username': username, 'password': password}
    teachers.append(new_teacher)
    data['teachers'] = teachers
    save_data(data)
    print("Teacher created successfully!")


def view_teachers():
    '''Displays a list of all teachers.'''
    data = load_data()
    teachers = data.get('teachers', [])
    for idx, teacher in enumerate(teachers, start=1):
        print(f"{idx}. {teacher['full_name']} ({teacher['gender']}) - {teacher['email']}")


def delete_teacher():
    '''Prompts to select a teacher to delete and removes them from the data.'''
    data = load_data()
    teachers = data.get('teachers', [])
    view_teachers()

    teacher_idx = int(input("Select the number of the Teacher to delete: ")) - 1
    if 0 <= teacher_idx < len(teachers):
        teachers.pop(teacher_idx)
        data['teachers'] = teachers
        save_data(data)
        print("Teacher deleted successfully!")
    else:
        print("Invalid selection!")


def update_teacher():
    '''Prompts to select a teacher to update and modifies their details.'''
    data = load_data()
    teachers = data.get('teachers', [])
    view_teachers()

    teacher_idx = int(input("Select the number of the Teacher to update: ")) - 1
    if 0 <= teacher_idx < len(teachers):
        teachers[teacher_idx]['full_name'] = input("New Full Name: ")
        teachers[teacher_idx]['gender'] = input("New Gender: ")
        teachers[teacher_idx]['email'] = input("New Email: ")
        data['teachers'] = teachers
        save_data(data)
        print("Teacher updated successfully!")
    else:
        print("Invalid selection!")


def send_email():
    '''Prompts for email details and sends an email to selected teachers based on their gender.'''
    data = load_data()
    teachers = data.get('teachers', [])

    print("\n1. To all")
    print("2. To females only")
    print("3. To males only")
    choice = input("Choose an option: ")

    if choice == '1':
        recipients = [t['email'] for t in teachers]
    elif choice == '2':
        recipients = [t['email'] for t in teachers if t['gender'].lower() == 'female']
    elif choice == '3':
        recipients = [t['email'] for t in teachers if t['gender'].lower() == 'male']
    else:
        print("Invalid choice!")
        return

    subject = input("Email Subject: ")
    body = input("Email Body: ")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "maxmadaliyevasarvinoz2005@gmail.com"
    msg['To'] = ", ".join(recipients)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("maxmadaliyevasarvinoz2005@gmail.com", "dloe uzth pvly nfdw")
            server.sendmail("maxmadaliyevasarvinoz2005@gmail.com", recipients, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
