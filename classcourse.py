 # Devonte Harris
# 9/19/2024
# This program will allow the user to create and manage a class schedule for a selected term
# Python 


 



import mysql.connector
import bcrypt


def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Triplets03!!!',
        database='class_schedule'
    )


def sign_up(first_name, last_name, email, password):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        print("Email is already in use.")
        return False

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                   (first_name, last_name, email, hashed_password))
    connection.commit()
    print("User registered successfully.")
    cursor.close()
    connection.close()


def login(email, password):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT user_id, password FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
        print("Login successful.")
        return result[0]  
    else:
        print("Invalid credentials.")
        return None


def create_term(user_id, term, year):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM schedules WHERE user_id = %s AND term = %s AND year = %s", (user_id, term, year))
    if cursor.fetchone():
        print(f"{term} {year} already exists.")
        return False

    print(f"New term {term} {year} created.")
    return True


def add_course(user_id, term, year, course_number, course_title, credits, days):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO schedules (user_id, term, year, course_number, course_title, credits, days) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (user_id, term, year, course_number, course_title, credits, days))
    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM schedules WHERE user_id = %s AND term = %s AND year = %s", (user_id, term, year))
    course_count = cursor.fetchone()[0]

    if course_count < 4:
        print(f"You need {4 - course_count} more courses to meet the minimum requirement.")
    else:
        print(f"Course {course_number} added successfully.")
    
    cursor.close()
    connection.close()


def view_schedule(user_id, term, year):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT course_number, course_title, credits, days FROM schedules WHERE user_id = %s AND term = %s AND year = %s", (user_id, term, year))
    courses = cursor.fetchall()

    print(f"{term} {year} Semester")
    for course in courses:
        print(f"{course[0]} – {course[1]}, {course[2]} credits, {course[3]}")
    
    cursor.close()
    connection.close()


def manage_schedule(user_id, term, year):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT course_number, course_title FROM schedules WHERE user_id = %s AND term = %s AND year = %s", (user_id, term, year))
    courses = cursor.fetchall()

    print(f"Courses in {term} {year}:")
    for i, course in enumerate(courses, start=1):
        print(f"{i}. {course[0]} - {course[1]}")
    
    choice = int(input("Select the course number to remove: ")) - 1
    course_to_remove = courses[choice][0]

    cursor.execute("DELETE FROM schedules WHERE user_id = %s AND course_number = %s AND term = %s AND year = %s", (user_id, course_to_remove, term, year))
    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM schedules WHERE user_id = %s AND term = %s AND year = %s", (user_id, term, year))
    course_count = cursor.fetchone()[0]

    if course_count < 4:
        print("You must add another course immediately.")
        
    else:
        print(f"Course {course_to_remove} removed successfully.")

    cursor.close()
    connection.close()


def main_menu(user_id):
    while True:
        print("\n--- Main Menu ---")
        print("1. Create a new term")
        print("2. Add courses to existing term")
        print("3. View terms and schedules")
        print("4. Manage schedule")
        print("5. Log out")

        choice = input("Select an option: ")
        
        if choice == '1':
            term = input("Enter term (Fall, Winter, Spring, Summer, Maymester): ")
            year = int(input("Enter year (2024 - 2100): "))
            if create_term(user_id, term, year):
                while True:
                    course_number = input("Enter course number: ")
                    course_title = input("Enter course title: ")
                    credits = int(input("Enter course credits: "))
                    days = input("Enter course days (e.g., Monday-Friday): ")
                    add_course(user_id, term, year, course_number, course_title, credits, days)
                    if input("Add another course? (y/n): ").lower() != 'y':
                        break
        elif choice == '2':
            term = input("Enter term to add courses to: ")
            year = int(input("Enter year: "))
            while True:
                course_number = input("Enter course number: ")
                course_title = input("Enter course title: ")
                credits = int(input("Enter course credits: "))
                days = input("Enter course days (e.g., Monday-Friday): ")
                add_course(user_id, term, year, course_number, course_title, credits, days)
                if input("Add another course? (y/n): ").lower() != 'y':
                    break
        elif choice == '3':
            term = input("Enter term to view: ")
            year = int(input("Enter year: "))
            view_schedule(user_id, term, year)
        elif choice == '4':
            term = input("Enter term to manage: ")
            year = int(input("Enter year: "))
            manage_schedule(user_id, term, year)
        elif choice == '5':
            print("Logged out.")
            break
        else:
            print("Invalid option.")


def main():
    while True:
        print("\n--- Welcome to the Class Schedule Creator ---")
        print("1. Sign Up")
        print("2. Login")
        choice = input("Select an option: ")

        if choice == '1':
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            sign_up(first_name, last_name, email, password)
        elif choice == '2':
            email = input("Enter email: ")
            password = input("Enter password: ")
            user_id = login(email, password)
            if user_id:
                main_menu(user_id)
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
