import sqlite3

def collect_student_data():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Fetch all students and their phone numbers
    query = '''
        SELECT students.name, students.father_phone, students.mother_phone
        FROM students
    '''
    cursor.execute(query)
    students = cursor.fetchall()

    student_data = {}
    for student_name, father_phone, mother_phone in students:
        phones = []
        if father_phone:
            phones.append(father_phone)
        if mother_phone:
            phones.append(mother_phone)
        if phones:
            student_data[student_name] = ",".join(phones)

    conn.close()

    # Save student data to a file
    with open('student_data.txt', 'w', encoding='utf-8') as file:
        for name, phone in student_data.items():
            file.write(f"{name}: {phone}\n")

    print("Student data collected and saved to student_data.txt")

if __name__ == "__main__":
    collect_student_data()