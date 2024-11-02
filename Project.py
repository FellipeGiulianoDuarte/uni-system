def main():
    while True:
        print("Please select one of the following:")
        print("1- Add a new student")
        print("2- Add a new course")
        print("3- Add a new grade")
        print("4- Print a student's transcript")
        print("5- Students who pass a subject")
        print("6- Exit")
        choice=int(input("Enter your choice: "))
        if choice == 1:
            addNewStudent()
        elif choice == 2:
            addNewCourse()
        elif choice == 3:
            addNewGrade()
        elif choice == 4:
            printStudentTranscript()
        elif choice == 5:
            studentsWhoPassSubject()
        elif choice == 6:
            print("Goodbye!")
            break
        else:
            print("Please insert a valid value")


def addNewStudent():
    student_id=int(input("Enter student ID: "))
    student_name=input("Enter student name: ")
    student_mobile=int(input("Enter student mobile: "))
    file=open('students.txt', 'a')
    file.write(f"{student_id},{student_name},{student_mobile},0.0\n")
    file.close()


def addNewCourse():
    course_no=input("Enter course No.: ")
    course_name=input("Enter course name: ")
    course_credits=int(input("Enter course credits: "))
    file=open('courses.txt', 'a')
    file.write(f"{course_no},{course_name},{course_credits}\n")
    file.close()


def addNewGrade():
    student_id=int(input("Enter student ID: "))
    file=open('students.txt', 'r')
    lines=file.readlines()
    file.close()
    student_exists=False
    for line in lines:
        if str(student_id) in line:
            student_exists=True
            break
    if not student_exists:
        print("There is no student with this ID")
        return
    student_course=input("Enter course No.: ")
    while True:
        student_grade=input("Enter student Grade: ")
        if student_grade not in ['A', 'B', 'C', 'D', 'F']:
            print("Invalid input!")
        else:
            file=open('grades.txt', 'a')
            file.write(f"{student_id},{student_course},{student_grade}\n")
            file.close()
            calculateAndUpdateGPA(student_id)
            return


def printStudentTranscript():
    student_id=int(input("Enter student ID: "))
    file=open('students.txt', 'r')
    lines=file.readlines()
    student_exists=False
    for line in lines:
        if str(student_id) in line:
            student_exists=True
            break
    file.close()
    if not student_exists:
        print("There is no student with this ID")
        return
    file=open('students.txt', 'r')
    lines=file.readlines()
    student=None
    for line in lines:
        if str(student_id) in line:
            student=line.split(',')
            break
    file.close()
    print(f"\nStudent Name: {student[1]}")
    print(f"Student GPA: {student[3].strip()}\n")


def studentsWhoPassSubject():
    student_course=input("Enter course No.: ")
    file=open('courses.txt', 'r')
    course_lines=file.readlines()
    file.close()
    course_exists=False
    for line in course_lines:
        if student_course in line:
            course_exists=True
            break
    if not course_exists:
        print("There is no course with this number")
        return
    file=open('grades.txt', 'r')
    lines=file.readlines()
    file.close()
    passed_students=[]
    for line in lines:
        split_line=line.split(',')
        if split_line[1] == student_course and split_line[2].strip() in ['A', 'B', 'C']:
            passed_students.append(split_line[0])
    if passed_students:
        print("Students who passed the course:")
        file=open('students.txt', 'r')
        lines=file.readlines()
        for student in passed_students:
            for line in lines:
                split_line=line.split(',')
                if split_line[0] == str(student):
                    print(f"Name: {split_line[1]}")
                    print(f"GPA: {split_line[3]}\n")
        file.close()
    else:
        print("No students passed the course")


def calculateAndUpdateGPA(student_id):
    file=open('students.txt', 'r')
    lines=file.readlines()
    file.close()
    student_exists=False
    for line in lines:
        if str(student_id) in line:
            student_exists=True
            break
    if not student_exists:
        print("There is no student with this ID")
        return
    total_credits=0
    weighted_sum=0
    grades_file=open('grades.txt', 'r')
    grade_lines=grades_file.readlines()
    grades_file.close()
    for line in grade_lines:
        data=line.split(',')
        if int(data[0]) == student_id:
            course_no=data[1]
            course_file=open('courses.txt', 'r')
            course_lines=course_file.readlines()
            course_file.close()
            credits=None
            for course_line in course_lines:
                if course_no in course_line:
                    credits=int(course_line.split(',')[2])
                    break
            total_credits += credits
            grade_value=data[2].strip()
            if grade_value == 'A':
                weighted_sum += 4 * credits
            elif grade_value == 'B':
                weighted_sum += 3 * credits
            elif grade_value == 'C':
                weighted_sum += 2 * credits
            elif grade_value == 'D':
                weighted_sum += 1 * credits
            elif grade_value == 'F':
                weighted_sum += 0 * credits
    if total_credits == 0:
        print("No grades available for this student.")
        return
    gpa=weighted_sum / total_credits
    student_file=open('students.txt', 'r')
    lines=student_file.readlines()
    student_file.close()
    students=[]
    for line in lines:
        student_data=line.rstrip("\n").split(',')
        students.append(student_data)
    for student in students:
        if int(student[0]) == student_id:
            student[3]=str(gpa)
    student_file=open('students.txt', 'w')
    for student in students:
        student_file.write(f"{student[0]},{student[1]},{student[2]},{student[3]}\n")
    student_file.close()


main()
