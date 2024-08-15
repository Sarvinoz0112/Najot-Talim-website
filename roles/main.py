from superadmin import superadmin_login, superadmin_menu
from admin import admin_login, admin_menu
from teacher import teacher_login
from student import student_login  # Import the student_login function

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Login as SuperAdmin")
        print("2. Login as Admin")
        print("3. Login as Teacher")
        print("4. Login as Student")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            superadmin_login()
        elif choice == '2':
            admin_login()
        elif choice == '3':
            teacher_login()
        elif choice == '4':
            student_login()  # Call the student_login function
        elif choice == '5':
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()
