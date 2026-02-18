# We create an empty dictionary to store all student records
students = {}

def add_student(student_id, first_name, last_name):
# We use student ID as our main key to identify students
    if student_id in students:
        print("Student ID record already exists")
        return

    # Create a dictioanry of our student record
    students[student_id] = {
        "first_name" : first_name,
        "last_name" : last_name,
        "attendance" : {},
        "evaluation" : "No record"
    }

    print("\n-> Student record added")

def add_attendance(student_id, date, attendance):
    # Check if ID exists
    if student_id not in students:
        print("\nStudent not found")
        return
    
    # Check if correct attendance is entered
    if attendance not in ["P", "A"]:
        print("\nPlease use 'P' - Present and 'A' - Absent")
        return
    
    # Check if attendance alreaddy entered for a date
    if date in students[student_id]["attendance"]:
        print("\nAttendance already exists for this date")
        return
    
    # Add the attendance
    students[student_id]["attendance"][date] = attendance
    update_evaluation(student_id)
    print("\n-> Attendance has been recorded")

def calc_atten_perc(student_id):
    attendance = students[student_id]["attendance"]
    total_no_of_days = len(attendance)

    if total_no_of_days == 0:
        return 0
    
    present_days = list(attendance.values()).count("P")
    percentage = (present_days/total_no_of_days) * 100
    return round(percentage, 2)

def update_evaluation(student_id):
    percentage = calc_atten_perc(student_id)

    if percentage >=85:
        evaluation = "Excellent"
    elif percentage >=75:
        evaluation = "Good"
    elif percentage >=60:
        evaluation = "Needs Improvement"
    else:
        evaluation = "At Risk"
    
    students[student_id]["evaluation"] = evaluation

def view_student(student_id):

    # Check if student exists based on student_id
    if student_id not in students:
        print("\nStudent record has not been found")
        return
    
    student = students[student_id]

    print("\n----Student details----\n")
    print("ID: ", student_id)
    print("Name: ", student["first_name"], student["last_name"])

    attendance_percentage = calc_atten_perc(student_id)
    print(f"Attendance percentage: {attendance_percentage}%")
    print(f"Evaluation: {student['evaluation']}")

    print("\nAttendance records:")
    if not student["attendance"]:
        print("No attendance records yet")
    else:
        for date, attendance in student["attendance"].items():
            print(f"{date} : {attendance}")


def delete_student(student_id):
    if student_id not in students:
        print("\nNo student record found")
        return
    
    del students[student_id]
    print("\n-> Student record has been deleted")


def display_menu():
    print("\n----Mini Student Management System----")
    print("1. Add Student")
    print("2. Mark Attendance")
    print("3. View Student")
    print("4. Delete Student")
    print("5. Exit")


def main():
    while True:
        display_menu()    
        user_input = input("\nSelect the task you want to perform: ")

        if user_input == "1":
            student_id = int(input("Enter Student ID: "))
            first_name = input("Enter First Name: ")
            last_name = input("Enter last name: ")

            add_student(student_id, first_name, last_name)

        elif user_input == "2":
            student_id = int(input("Enter Student ID: "))
            date = input("Enter date in YYYY-MM-DD format: ")
            attendance = input("Enter attendance [P/A]: ").upper()

            add_attendance(student_id, date, attendance)

        elif user_input == "3":
            student_id = int(input("Enter Student ID: "))

            view_student(student_id)

        elif user_input == "4":
            student_id = int(input("Enter Student ID: "))

            delete_student(student_id)

        elif user_input == "5":
            print("Exiting records")
            break

        else:
            print("\nPlease select from the following tasks only")


if __name__ == "__main__":
    main()