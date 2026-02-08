import requests
from config import FARAZ_SMS_API_KEY, FARAZ_SMS_SENDER
import sqlite3

def send_sms(to_number, message):
    if not to_number.startswith("+98"):
        to_number = f"+98{to_number.lstrip('0')}"

    print(f"Attempting to send SMS to: {to_number}")  # Log recipient number

    url = f"https://edge.ippanel.com/v1/api/send/webservice?message={message}&from=+983000505&to={to_number}&username=your username &password=your password"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"AccessKey {FARAZ_SMS_API_KEY}"
    }
    try:
        response = requests.post(url, headers=headers)
        response_data = response.json()
        if response.status_code != 200 or not response_data.get("meta", {}).get("status", False):
            print(f"Error for {to_number}: {response_data.get('message', 'Unknown error')} - Code: {response.status_code}")
        return response_data
    except Exception as e:
        print(f"Exception occurred for {to_number}: {e}")
        return None

def send_sms_correctly(to_number, message):
    if not to_number.startswith("+98"):
        to_number = f"+98{to_number.lstrip('0')}"

    print(f"Attempting to send SMS to: {to_number}")

    url = f"https://edge.ippanel.com/v1/api/send/webservice?message={message}&from=+983000505&to={to_number}&username=your username&password=your password"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"AccessKey {FARAZ_SMS_API_KEY}"
    }
    try:
        response = requests.post(url, headers=headers)
        response_data = response.json()
        if response.status_code != 200 or not response_data.get("meta", {}).get("status", False):
            print(f"Error for {to_number}: {response_data.get('message', 'Unknown error')} - Code: {response.status_code}")
        return response_data
    except Exception as e:
        print(f"Exception occurred for {to_number}: {e}")
        return None

def send_sms_to_all(numbers, message):
    # Accept either a single phone string or an iterable of phone strings
    if not numbers:
        print("No numbers provided.")
        return

    # If a single phone is provided (string), send to that one exact phone
    if isinstance(numbers, str):
        phones = [numbers]
    else:
        # assume iterable of phones
        phones = list(numbers)

    for phone in phones:
        if not phone:
            print("Skipping empty phone entry")
            continue
        # If a combined string of phones is passed (comma separated), split and send to each
        if isinstance(phone, str) and ',' in phone:
            for p in phone.split(','):
                p = p.strip()
                if p:
                    print(f"Sending SMS to: {p}")
                    response = send_sms_correctly(p, message)
                    if response and response.get("meta", {}).get("status", False):
                        print(f"SMS sent successfully to: {p}")
                    else:
                        print(f"Failed to send SMS to: {p}")
            continue

        print(f"Sending SMS to: {phone}")
        response = send_sms_correctly(phone, message)
        if response and response.get("meta", {}).get("status", False):
            print(f"SMS sent successfully to: {phone}")
        else:
            print(f"Failed to send SMS to: {phone}")

def send_sms_based_on_attendance():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Fetch attendance records with student details
    query = '''
        SELECT students.name, students.father_phone, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        WHERE attendance.date = DATE('now')
    '''
    cursor.execute(query)
    records = cursor.fetchall()

    print("Fetched attendance records:")
    for student_name, father_phone, status in records:
        print(f"Student: {student_name}, Parent Phone: {father_phone}, Status: {status}")

    for student_name, father_phone, status in records:
        if not father_phone:
            print(f"No phone number for {student_name}")
            continue

        message = ""  # Determine the message based on attendance status
        if status == "حاضر":
            message = "دانش‌آموز شما امروز حاضر بوده است. دبیرستان نام مدرسه ی شما"
        elif status == "غایب":
            message = "دانش‌آموز شما امروز غایب بوده است. دبیرستان نام مدرسه ی شما"
        else:
            print(f"Unknown status for {student_name}: {status}")
            continue

        response = send_sms(father_phone, message)
        if response and response.get("meta", {}).get("status", False):
            print(f"SMS sent successfully to {father_phone} for {student_name}")
        else:
            print(f"Failed to send SMS to {father_phone} for {student_name}")

    conn.close()

def debug_attendance_records():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Fetch attendance records with student details
    query = '''
        SELECT students.name, students.father_phone, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        WHERE attendance.date = DATE('now')
    '''
    cursor.execute(query)
    records = cursor.fetchall()

    if not records:
        print("No attendance records found for today.")
    else:
        print("Fetched attendance records:")
        for student_name, father_phone, status in records:
            print(f"Student: {student_name}, Parent Phone: {father_phone}, Status: {status}")

    conn.close()

def send_sms_to_students():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Fetch attendance records with student details
    query = '''
        SELECT students.name, students.father_phone, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        WHERE attendance.date = DATE('now')
    '''
    cursor.execute(query)
    records = cursor.fetchall()

    for student_name, father_phone, status in records:
        if not father_phone:
            print(f"No phone number for {student_name}")
            continue

        message = ""  # Determine the message based on attendance status
        if status == "حاضر":
            message = "دانش‌آموز شما امروز حاضر بوده است. دبیرستان نام مدرسه ی شما"
        elif status == "غایب":
            message = "دانش‌آموز شما امروز غایب بوده است. دبیرستان نام مدرسه ی شما"
        else:
            print(f"Unknown status for {student_name}: {status}")
            continue

        response = send_sms(father_phone, message)
        if response and response.get("meta", {}).get("status", False):
            print(f"SMS sent successfully to {father_phone} for {student_name}")
        else:
            print(f"Failed to send SMS to {father_phone} for {student_name}")

    conn.close()

def debug_database():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Fetch all students
    print("Students:")
    cursor.execute("SELECT id, name, father_phone FROM students")
    students = cursor.fetchall()
    for student in students:
        print(student)

    # Fetch all attendance records
    print("Attendance Records:")
    cursor.execute("SELECT id, student_id, status, date FROM attendance")
    attendance_records = cursor.fetchall()
    for record in attendance_records:
        print(record)

    conn.close()

def debug_sms_sending():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Fetch attendance records with student details
    query = '''
        SELECT students.name, students.father_phone, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        WHERE attendance.date = DATE('now')
    '''
    cursor.execute(query)
    records = cursor.fetchall()

    print("Preparing to send SMS:")
    for student_name, father_phone, status in records:
        print(f"Student: {student_name}, Parent Phone: {father_phone}, Status: {status}")

        if not father_phone:
            print(f"Skipping {student_name} due to missing phone number.")
            continue

        message = ""  # Determine the message based on attendance status
        if status == "حاضر":
            message = "دانش‌آموز شما امروز حاضر بوده است. دبیرستان نام مدرسه ی شما"
        elif status == "غایب":
            message = "دانش‌آموز شما امروز غایب بوده است. دبیرستان نام مدرسه ی شما"
        else:
            print(f"Unknown status for {student_name}: {status}")
            continue

        print(f"Sending SMS to {father_phone}: {message}")
        response = send_sms(father_phone, message)
        if response and response.get("meta", {}).get("status", False):
            print(f"SMS sent successfully to {father_phone} for {student_name}")
        else:
            print(f"Failed to send SMS to {father_phone} for {student_name}")

    conn.close()

def debug_phone_number_format():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Fetch attendance records with student details
    query = '''
        SELECT students.name, students.father_phone, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        WHERE attendance.date = DATE('now')
    '''
    cursor.execute(query)
    records = cursor.fetchall()

    print("Checking phone number formatting:")
    for student_name, father_phone, status in records:
        if not father_phone:
            print(f"No phone number for {student_name}")
            continue

        formatted_phone = father_phone
        if not father_phone.startswith("+98"):
            formatted_phone = f"+98{father_phone.lstrip('0')}"

        print(f"Original: {father_phone}, Formatted: {formatted_phone}")

    conn.close()

def send_sms_from_file():
    try:
        # Read phone numbers from the file
        with open('student_data.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            name, phone = line.strip().split(': ')
            print(f"Sending SMS to {name} at {phone}")

            message = "دانش‌آموز شما امروز حاضر بوده است. دبیرستان نام مدرسه ی شما"  # Example message
            response = send_sms(phone, message)

            if response and response.get("meta", {}).get("status", False):
                print(f"SMS sent successfully to {phone} for {name}")
            else:
                print(f"Failed to send SMS to {phone} for {name}")

    except FileNotFoundError:
        print("student_data.txt file not found. Please run the data collection script first.")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_database_integrity():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Check for students with missing father_phone
    query_missing_phone = 'SELECT id, name FROM students WHERE father_phone IS NULL OR father_phone = ""'
    cursor.execute(query_missing_phone)
    missing_phone_records = cursor.fetchall()

    if missing_phone_records:
        print("Students with missing parent phone numbers:")
        for student_id, student_name in missing_phone_records:
            print(f"ID: {student_id}, Name: {student_name}")
    else:
        print("All students have parent phone numbers.")

    # Check for attendance records without valid student IDs
    query_invalid_attendance = 'SELECT id FROM attendance WHERE student_id NOT IN (SELECT id FROM students)'
    cursor.execute(query_invalid_attendance)
    invalid_attendance_records = cursor.fetchall()

    if invalid_attendance_records:
        print("Invalid attendance records found:")
        for record_id in invalid_attendance_records:
            print(f"Attendance Record ID: {record_id[0]}")
    else:
        print("All attendance records are valid.")

    conn.close()

def fix_missing_phone_numbers():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Find students with missing or empty phone numbers
    query_missing_phone = 'SELECT id, name FROM students WHERE father_phone IS NULL OR father_phone = ""'
    cursor.execute(query_missing_phone)
    missing_phone_records = cursor.fetchall()

    if missing_phone_records:
        print("Fixing students with missing parent phone numbers:")
        for student_id, student_name in missing_phone_records:
            print(f"ID: {student_id}, Name: {student_name}")
            # Assign a default phone number for testing purposes
            default_phone = "09123456789"
            update_query = 'UPDATE students SET father_phone = ? WHERE id = ?'
            cursor.execute(update_query, (default_phone, student_id))
            print(f"Assigned default phone number {default_phone} to {student_name}")

        conn.commit()
    else:
        print("No students with missing parent phone numbers found.")

    conn.close()

def validate_and_send_sms():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Fetch attendance records with student details
    query = '''
        SELECT students.name, students.father_phone, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        WHERE attendance.date = DATE('now')
    '''
    cursor.execute(query)
    records = cursor.fetchall()

    if not records:
        print("No attendance records found for today.")
        conn.close()
        return

    for student_name, father_phone, status in records:
        if not father_phone:
            print(f"No phone number for {student_name}")
            continue

        if not father_phone.startswith("+98"):
            father_phone = f"+98{father_phone.lstrip('0')}"

        message = ""  # Determine the message based on attendance status
        if status == "حاضر":
            message = "دانش‌آموز شما امروز حاضر بوده است. دبیرستان نام مدرسه ی شما"
        elif status == "غایب":
            message = "دانش‌آموز شما امروز غایب بوده است. دبیرستان نام مدرسه ی شما"
        else:
            print(f"Unknown status for {student_name}: {status}")
            continue

        print(f"Sending SMS to {father_phone} with message: {message}")
        response = send_sms(father_phone, message)
        if response and response.get("meta", {}).get("status", False):
            print(f"SMS sent successfully to {father_phone} for {student_name}")
        else:
            print(f"Failed to send SMS to {father_phone} for {student_name}")

    conn.close()

def validate_unique_phone_numbers():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Check for duplicate phone numbers
    query = '''
        SELECT father_phone, COUNT(*) as count
        FROM students
        GROUP BY father_phone
        HAVING count > 1
    '''
    cursor.execute(query)
    duplicates = cursor.fetchall()

    if duplicates:
        print("Duplicate phone numbers found:")
        for phone, count in duplicates:
            print(f"Phone: {phone}, Count: {count}")
    else:
        print("No duplicate phone numbers found.")

    conn.close()

def fix_duplicate_phone_numbers():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Find duplicate phone numbers
    query_duplicates = '''
        SELECT father_phone, GROUP_CONCAT(id) as student_ids
        FROM students
        GROUP BY father_phone
        HAVING COUNT(*) > 1
    '''
    cursor.execute(query_duplicates)
    duplicates = cursor.fetchall()

    if duplicates:
        print("Fixing duplicate phone numbers:")
        for phone, student_ids in duplicates:
            print(f"Phone: {phone}, Student IDs: {student_ids}")
            ids = student_ids.split(',')
            for i, student_id in enumerate(ids):
                new_phone = f"{phone[:-1]}{i}"  # Modify the phone number slightly
                update_query = 'UPDATE students SET father_phone = ? WHERE id = ?'
                cursor.execute(update_query, (new_phone, student_id))
                print(f"Updated Student ID {student_id} with new phone: {new_phone}")

        conn.commit()
    else:
        print("No duplicate phone numbers found.")

    conn.close()

def restore_original_phone_numbers():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Restore original phone numbers for specific student IDs
    original_numbers = {
        4: "09139231104",
        5: "09139231104",
        17: "09139231104"
    }

    for student_id, phone in original_numbers.items():
        update_query = 'UPDATE students SET father_phone = ? WHERE id = ?'
        cursor.execute(update_query, (phone, student_id))
        print(f"Restored Student ID {student_id} with phone: {phone}")

    conn.commit()
    conn.close()

def send_sms_to_students_with_logging():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Fetch attendance records with student details
    query = '''
        SELECT students.name, students.father_phone, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        WHERE attendance.date = DATE('now')
    '''
    cursor.execute(query)
    records = cursor.fetchall()

    if not records:
        print("No attendance records found for today.")
        conn.close()
        return

    for student_name, father_phone, status in records:
        if not father_phone:
            print(f"No phone number for {student_name}")
            continue

        if not father_phone.startswith("+98"):
            father_phone = f"+98{father_phone.lstrip('0')}"

        message = ""  # Determine the message based on attendance status
        if status == "حاضر":
            message = "دانش‌آموز شما امروز حاضر بوده است. دبیرستان نام مدرسه ی شما"
        elif status == "غایب":
            message = "دانش‌آموز شما امروز غایب بوده است. دبیرستان نام مدرسه ی شما"
        else:
            print(f"Unknown status for {student_name}: {status}")
            continue

        print(f"Attempting to send SMS to {father_phone} for student {student_name} with message: {message}")
        response = send_sms(father_phone, message)
        if response and response.get("meta", {}).get("status", False):
            print(f"SMS sent successfully to {father_phone} for {student_name}")
        else:
            print(f"Failed to send SMS to {father_phone} for {student_name}")

    conn.close()

def send_sms_to_students_fixed():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Debug: Print all attendance records for today
    debug_query = '''
        SELECT students.id, students.name, students.father_phone, attendance.status, attendance.selected
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        WHERE attendance.date = DATE('now')
    '''
    cursor.execute(debug_query)
    debug_records = cursor.fetchall()
    print("Debug: All attendance records for today:")
    for record in debug_records:
        print(record)

    # Fetch attendance records with student details for selected students
    query = '''
        SELECT students.id, students.name, students.father_phone, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        WHERE attendance.date = DATE('now') AND attendance.selected = 1
    '''
    cursor.execute(query)
    records = cursor.fetchall()

    if not records:
        print("No attendance records found for selected students today.")
        conn.close()
        return

    for student_id, student_name, father_phone, status in records:
        if not father_phone or father_phone.strip() == "0":
            print(f"Invalid phone number for {student_name} (ID: {student_id}): {father_phone}")
            continue

        # Ensure the phone number is formatted correctly
        if not father_phone.startswith("+98"):
            father_phone = f"+98{father_phone.lstrip('0')}"
