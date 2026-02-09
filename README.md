# School--and-university-attendance
# سامانه مدیریت حضور و غیاب مدرسه

[English](#english) | [فارسی](#فارسی)

---

## English

### Overview
A comprehensive school attendance management system developed with Python, PyQt5, SQLite, and Pandas. This application provides an intuitive interface for managing student attendance records and automating SMS notifications to parents using the Faraz SMS API.

### Features
- 🎨 **Modern GUI** - Built with PyQt5 for a user-friendly interface
- 📚 **Student Management** - Store and manage student information including:
  - Full name and father's name
  - Student ID/Code
  - Grade level (10, 11, 12)
  - Major/Field of study
  - Parent contact information (father and mother phone numbers)
- 📊 **Attendance Tracking** - Record daily attendance with status (present/absent)
- 📥 **Excel Import** - Bulk import student data from Excel files
- 💬 **SMS Notifications** - Automated SMS to parents via Faraz SMS API
- 💾 **Data Persistence** - SQLite database for reliable data storage
- 🔍 **Filtering** - Filter students by grade and major

### Requirements
- Python 3.8+
- PyQt5
- SQLite3 (included with Python)
- Pandas
- Requests (for SMS API)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mahangh8512/School--and-university-attendance.git
cd kardanesh
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
cd src
python main.py
```

### Project Structure
```
kardanesh/
├── src/
│   ├── main.py           # Main application entry point
│   ├── db.py             # Database initialization and management
│   ├── student_data.py   # Student data handling
│   ├── sms.py            # SMS API integration
│   ├── config.py         # Configuration settings
│   ├── school.db         # SQLite database
│   └── __pycache__/
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### Configuration

#### SMS API Setup
To enable SMS notifications, you need to configure your Faraz SMS API credentials:

1. Sign up at [Faraz SMS](https://farazsms.com) and get your API key
2. Update `src/config.py` with your credentials:
```python
SMS_API_KEY = "your_api_key_here"
SMS_API_USERNAME = "your_username"
```

### Usage

1. **Adding Students**: Import from Excel file with student information
2. **Recording Attendance**: Select students and mark them as present/absent
3. **Sending SMS**: Automatically send notifications to parents of absent students
4. **Viewing Records**: Filter and view attendance history by grade and major

### Database Schema

**Students Table**
- ID, Name, Father's Name, Student Code
- Grade, Major, Parent Phone Numbers

**Attendance Table**
- Student ID, Date, Status (Present/Absent)

**Grade Table**
- Grades 10, 11, 12

**Major Table**
- Various academic majors/fields

### License
GPL-3.0 license

### Contributing
Contributions are welcome! Feel free to submit issues and pull requests.

### Contact
For questions and support, please open an issue in the repository.

---

## فارسی

### نمای کلی
یک سامانه جامع مدیریت حضور و غیاب مدرسه که با Python، PyQt5، SQLite و Pandas توسعه داده شده است. این برنامه رابط کاربری سهل‌الاستفاده‌ای برای مدیریت رکوردهای حضور و غیاب دانش‌آموزان و خودکارسازی اطلاع‌رسانی پیامکی به والدین از طریق API فراز اس‌ام‌اس فراهم می‌کند.

### ویژگی‌ها
- 🎨 **رابط کاربری مدرن** - توسعه‌یافته با PyQt5 برای تجربه‌ای کاربری بهتر
- 📚 **مدیریت دانش‌آموزان** - ذخیره و مدیریت اطلاعات دانش‌آموزان شامل:
  - نام و نام پدر
  - کد دانش‌آموزی
  - پایه تحصیلی (10، 11، 12)
  - رشته تحصیلی
  - شماره تماس والدین (پدر و مادر)
- 📊 **پیگیری حضور و غیاب** - ثبت روزانه وضعیت حضور/غیاب
- 📥 **درون‌ریزی از اکسل** - واردکردن دسته‌ای اطلاعات دانش‌آموزان از فایل‌های اکسل
- 💬 **اطلاع‌رسانی پیامکی** - ارسال خودکار پیامک به والدین از طریق API فراز
- 💾 **ذخیره‌سازی داده‌ها** - پایگاه داده SQLite برای ذخیره قابل‌اعتماد اطلاعات
- 🔍 **فیلتر کردن** - جستجو و فیلتر دانش‌آموزان بر اساس پایه و رشته

### نیازمندی‌ها
- Python 3.8+
- PyQt5
- SQLite3 (شامل در Python)
- Pandas
- Requests (برای API پیامک)

### نحوه نصب

1. مخزن را کلون کنید:
```bash
git clone https://github.com/mahangh8512/School--and-university-attendance.git
cd kardanesh
```

2. وابستگی‌ها را نصب کنید:
```bash
pip install -r requirements.txt
```

3. برنامه را اجرا کنید:
```bash
cd src
python main.py
```

### ساختار پروژه
```
kardanesh/
├── src/
│   ├── main.py           # نقطه ورودی برنامه
│   ├── db.py             # مدیریت پایگاه داده
│   ├── student_data.py   # مدیریت اطلاعات دانش‌آموزان
│   ├── sms.py            # یکپارچگی API پیامک
│   ├── config.py         # تنظیمات برنامه
│   ├── school.db         # پایگاه داده SQLite
│   └── __pycache__/
├── requirements.txt      # وابستگی‌های Python
└── README.md            # این فایل
```

### تنظیمات

#### راه‌اندازی API فراز
برای فعال‌کردن اطلاع‌رسانی پیامکی، باید اطلاعات API فراز را تنظیم کنید:

1. در [فراز اس‌ام‌اس](https://farazsms.com) ثبت‌نام کنید و API Key خود را دریافت کنید
2. فایل `src/config.py` را با اطلاعات خود به‌روزرسانی کنید:
```python
SMS_API_KEY = "api_key_شما"
SMS_API_USERNAME = "نام‌کاربری_شما"
```

### نحوه استفاده

1. **افزودن دانش‌آموزان**: درون‌ریزی از فایل اکسل شامل اطلاعات دانش‌آموزان
2. **ثبت حضور و غیاب**: انتخاب دانش‌آموزان و علامت‌زدن وضعیت حضور/غیاب
3. **ارسال پیامک**: ارسال خودکار اطلاعیه به والدین دانش‌آموزان غایب
4. **مشاهده رکوردها**: نمایش و فیلتر کردن تاریخچه حضور و غیاب بر اساس پایه و رشته

### طراحی پایگاه داده

**جدول دانش‌آموزان**
- شناسه، نام، نام پدر، کد دانش‌آموزی
- پایه، رشته، شماره تماس والدین

**جدول حضور و غیاب**
- شناسه دانش‌آموز، تاریخ، وضعیت (حاضر/غایب)

**جدول پایه‌ها**
- پایه‌های 10، 11، 12

**جدول رشته‌ها**
- رشته‌های تحصیلی مختلف

### مجوز
GPL-3.0 license
### مشارکت
مشارکات استقبال می‌شوند! لطفاً مشکلات و درخواست‌های Pull خود را ارائه دهید.

### تماس
برای سؤالات و پشتیبانی، لطفاً یک Issue در مخزن باز کنید.
