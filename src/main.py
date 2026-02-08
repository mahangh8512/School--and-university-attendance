import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox,
    QComboBox, QLabel, QLineEdit, QVBoxLayout, QWidget, QListWidget, QHBoxLayout, QListWidgetItem)
import pandas as pd
from db import init_db
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def load_students(self):
        try:
            self.students_list.clear()
            import sqlite3
            conn = sqlite3.connect('school.db')
            try:
                c = conn.cursor()
                grade = self.grade_combo.currentText()
                major = self.major_combo.currentText()

                # دریافت id پایه و رشته انتخاب‌شده
                c.execute("SELECT id FROM grade WHERE name=?", (grade,))
                grade_row = c.fetchone()
                grade_id = grade_row[0] if grade_row else None
                c.execute("SELECT id FROM major WHERE name=? AND grade_id=?", (major, grade_id))
                major_row = c.fetchone()
                major_id = major_row[0] if major_row else None

                # بررسی وجود پایه و رشته در پایگاه داده
                if grade_id and major_id:
                    c.execute("SELECT name, father_name, student_code, father_phone, mother_phone FROM students WHERE grade_id=? AND major_id=?", (grade_id, major_id))
                    students = c.fetchall()

                    # افزودن دانش‌آموزان به لیست با چک‌باکس
                    for s in students:
                        item = QListWidgetItem(f"نام: {s[0]} | نام پدر: {s[1]} | کد دانش‌آموز: {s[2]} | شماره پدر: {s[3]} | شماره مادر: {s[4]}")
                        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                        item.setCheckState(Qt.Unchecked)
                        self.students_list.addItem(item)

                    # راست‌چین کردن متن‌ها
                    self.students_list.setLayoutDirection(Qt.RightToLeft)
                else:
                    self.students_list.clear()  # پاک کردن لیست در صورت عدم وجود داده
                    QMessageBox.warning(self, "توجه", "هیچ دانش‌آموزی برای این پایه و رشته یافت نشد.")
            finally:
                conn.close()
        except Exception as e:
            QMessageBox.critical(self, "خطا", str(e))

    def add_student_dialog(self):
        from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox
        dialog = QDialog(self)
        dialog.setWindowTitle("افزودن دانش‌آموز جدید")
        layout = QFormLayout(dialog)

        name_edit = QLineEdit()
        father_name_edit = QLineEdit()
        father_phone_edit = QLineEdit()
        mother_phone_edit = QLineEdit()
        student_code_edit = QLineEdit()
        grade_combo = QComboBox()
        # load grades from DB (fallback to 10/11/12)
        import sqlite3
        try:
            conn = sqlite3.connect('school.db')
            c = conn.cursor()
            c.execute("SELECT name FROM grade ORDER BY name")
            grade_rows = c.fetchall()
            grades = [r[0] for r in grade_rows] if grade_rows else ["10", "11", "12"]
        except Exception:
            grades = ["10", "11", "12"]
        finally:
            try:
                conn.close()
            except Exception:
                pass
        grade_combo.addItems(grades)
        major_combo = QComboBox()

        def update_major_combo():
            selected_grade = grade_combo.currentText()
            major_combo.clear()
            try:
                conn = sqlite3.connect('school.db')
                c = conn.cursor()
                c.execute("SELECT id FROM grade WHERE name=?", (selected_grade,))
                gid = c.fetchone()
                if gid:
                    c.execute("SELECT name FROM major WHERE grade_id=? ORDER BY name", (gid[0],))
                    rows = c.fetchall()
                    major_combo.addItems([r[0] for r in rows])
            finally:
                try:
                    conn.close()
                except Exception:
                    pass

        grade_combo.currentTextChanged.connect(update_major_combo)
        update_major_combo()

        layout.addRow("نام:", name_edit)
        layout.addRow("نام پدر:", father_name_edit)
        layout.addRow("شماره پدر:", father_phone_edit)
        layout.addRow("شماره مادر:", mother_phone_edit)
        layout.addRow("کد دانش‌آموز:", student_code_edit)
        layout.addRow("پایه:", grade_combo)
        layout.addRow("رشته:", major_combo)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addRow(button_box)

        def on_accept():
            name = name_edit.text()
            father_name = father_name_edit.text()
            mother_phone = mother_phone_edit.text()
            father_phone = father_phone_edit.text()
            student_code = student_code_edit.text()
            grade = grade_combo.currentText()
            major = major_combo.currentText()

            if not all([name, father_name, father_phone, student_code, grade, major]):
                QMessageBox.warning(self, "خطا", "لطفاً تمام فیلدها را پر کنید.")
                return

            import sqlite3
            try:
                conn = sqlite3.connect('school.db')
                c = conn.cursor()
                c.execute("INSERT OR IGNORE INTO grade (name) VALUES (?)", (grade,))
                conn.commit()
                c.execute("SELECT id FROM grade WHERE name=?", (grade,))
                gr = c.fetchone()
                if not gr:
                    QMessageBox.critical(self, "خطا", "پایه یافت نشد.")
                    return
                grade_id = gr[0]
                c.execute("INSERT OR IGNORE INTO major (name, grade_id) VALUES (?, ?)", (major, grade_id))
                conn.commit()
                c.execute("SELECT id FROM major WHERE name=? AND grade_id=?", (major, grade_id))
                mr = c.fetchone()
                if not mr:
                    QMessageBox.critical(self, "خطا", "رشته یافت نشد.")
                    return
                major_id = mr[0]
                c.execute(
                    "INSERT INTO students (name, father_name, mother_phone, father_phone, student_code, grade_id, major_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (name, father_name, mother_phone, father_phone, student_code, grade_id, major_id)
                )
                conn.commit()

                # بارگذاری مجدد دانش‌آموزان برای رشته و پایه فعلی
                self.load_students()

                QMessageBox.information(self, "موفق", "دانش‌آموز جدید اضافه شد.")
                dialog.accept()
            except Exception as e:
                QMessageBox.critical(self, "خطا", str(e))
            finally:
                conn.close()

        button_box.accepted.connect(on_accept)
        button_box.rejected.connect(dialog.reject)

        dialog.exec_()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("سامانه حضور و غیاب دبیرستان نام مدرسه ی شما")
        self.setGeometry(100, 100, 600, 400)
        init_db()
        self.init_ui()
        self.load_students()  # بارگذاری لیست دانش‌آموزان هنگام باز کردن برنامه

    def init_ui(self):
        self.btn_delete_student = QPushButton("حذف دانش‌آموز")
        self.btn_delete_student.clicked.connect(self.delete_student)
        # تعریف همه ویجت‌های کلیدی
        self.grade_label = QLabel("پایه:")
        self.grade_combo = QComboBox()
        self.grade_combo.addItems(["10", "11", "12"])
        # majors are stored in DB per grade; UI will load them dynamically
        self.major_label = QLabel("رشته:")
        self.major_combo = QComboBox()
        self.students_list = QListWidget()
        self.btn_add_student = QPushButton("افزودن دانش‌آموز جدید")
        self.btn_import = QPushButton("ورود اطلاعات از اکسل")
        self.btn_attendance = QPushButton("ثبت حضور/غیاب")

        # چیدمان
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.grade_label)
        top_layout.addWidget(self.grade_combo)
        top_layout.addWidget(self.major_label)
        top_layout.addWidget(self.major_combo)
        # buttons to manage majors
        self.btn_add_major = QPushButton("افزودن رشته")
        self.btn_remove_major = QPushButton("حذف رشته")
        top_layout.addWidget(self.btn_add_major)
        top_layout.addWidget(self.btn_remove_major)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.btn_import)
        main_layout.addWidget(self.btn_add_student)
        main_layout.addWidget(self.students_list)
        main_layout.addWidget(self.btn_delete_student)
        main_layout.addWidget(self.btn_attendance)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # اتصال سیگنال‌ها
        self.grade_combo.currentTextChanged.connect(self.update_major_combo)
        self.btn_add_student.clicked.connect(self.add_student_dialog)
        self.btn_import.clicked.connect(self.import_excel)
        self.btn_attendance.clicked.connect(self.mark_attendance)
        self.btn_add_major.clicked.connect(self.add_major)
        self.btn_remove_major.clicked.connect(self.remove_major)
        self.update_major_combo()
        self.grade_combo.currentTextChanged.connect(self.load_students)
        self.major_combo.currentTextChanged.connect(self.load_students)

    def delete_student(self):
        try:
            # Collect items that are either checked (checkbox) or selected (highlighted)
            items_to_delete = []
            for i in range(self.students_list.count()):
                item = self.students_list.item(i)
                if item.checkState() == Qt.Checked or item.isSelected():
                    items_to_delete.append(item)

            if not items_to_delete:
                QMessageBox.warning(self, "توجه", "لطفاً دانش‌آموز را انتخاب یا تیک بزنید.")
                return

            reply = QMessageBox.question(self, "حذف دانش‌آموز", "آیا از حذف دانش‌آموز(ها) انتخاب‌شده مطمئن هستید؟", QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes:
                return

            import sqlite3
            grade = self.grade_combo.currentText()
            major = self.major_combo.currentText()

            conn = sqlite3.connect('school.db')
            try:
                c = conn.cursor()
                c.execute("SELECT id FROM grade WHERE name=?", (grade,))
                gid = c.fetchone()
                c.execute("SELECT id FROM major WHERE name=? AND grade_id=?", (major, gid[0] if gid else None))
                mid = c.fetchone()
                if not gid or not mid:
                    QMessageBox.warning(self, "خطا", "پایه یا رشته یافت نشد.")
                    return
                grade_id = gid[0]
                major_id = mid[0]

                for item in items_to_delete:
                    text = item.text()
                    # Expected format: "نام: {name} | نام پدر: {father} | ..."
                    if '|' in text:
                        student_name = text.split('|')[0].split(':', 1)[1].strip()
                    else:
                        # Fallback: try old separator or use whole text
                        student_name = text.split(' - ')[0].strip()

                    c.execute("DELETE FROM students WHERE name=? AND grade_id=? AND major_id=?", (student_name, grade_id, major_id))

                conn.commit()
                self.load_students()
                QMessageBox.information(self, "حذف شد", "دانش‌آموز(ها) انتخاب‌شده حذف شدند.")
            except Exception as e:
                QMessageBox.critical(self, "خطا", str(e))
            finally:
                conn.close()
        except Exception as e:
            QMessageBox.critical(self, "خطای غیرمنتظره", str(e))

    def update_major_combo(self):
        grade = self.grade_combo.currentText()
        self.major_combo.clear()
        import sqlite3
        try:
            conn = sqlite3.connect('school.db')
            c = conn.cursor()
            c.execute("SELECT id FROM grade WHERE name=?", (grade,))
            gid = c.fetchone()
            if gid:
                c.execute("SELECT name FROM major WHERE grade_id=? ORDER BY name", (gid[0],))
                rows = c.fetchall()
                self.major_combo.addItems([r[0] for r in rows])
        except Exception:
            pass
        finally:
            try:
                conn.close()
            except Exception:
                pass
        self.load_students()  # بارگذاری لیست دانش‌آموزان هنگام تغییر رشته

    def add_major(self):
        from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox
        dialog = QDialog(self)
        dialog.setWindowTitle("افزودن رشته جدید")
        layout = QFormLayout(dialog)
        grade_sel = QComboBox()
        name_edit = QLineEdit()
        # load grades
        import sqlite3
        try:
            conn = sqlite3.connect('school.db')
            c = conn.cursor()
            c.execute("SELECT name FROM grade ORDER BY name")
            rows = c.fetchall()
            grade_sel.addItems([r[0] for r in rows])
        finally:
            try:
                conn.close()
            except Exception:
                pass

        layout.addRow("پایه:", grade_sel)
        layout.addRow("نام رشته:", name_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addRow(buttons)

        def on_accept():
            g = grade_sel.currentText()
            name = name_edit.text().strip()
            if not name:
                QMessageBox.warning(self, "خطا", "نام رشته را وارد کنید.")
                return
            try:
                conn = sqlite3.connect('school.db')
                c = conn.cursor()
                c.execute("SELECT id FROM grade WHERE name=?", (g,))
                gr = c.fetchone()
                if not gr:
                    QMessageBox.critical(self, "خطا", "پایه یافت نشد.")
                    return
                gid = gr[0]
                c.execute("INSERT OR IGNORE INTO major (name, grade_id) VALUES (?, ?)", (name, gid))
                conn.commit()
                QMessageBox.information(self, "موفق", "رشته اضافه شد.")
                dialog.accept()
                self.update_major_combo()
            except Exception as e:
                QMessageBox.critical(self, "خطا", str(e))
            finally:
                try:
                    conn.close()
                except Exception:
                    pass

        buttons.accepted.connect(on_accept)
        buttons.rejected.connect(dialog.reject)
        dialog.exec_()

    def remove_major(self):
        # remove currently selected major (if no students attached)
        maj = self.major_combo.currentText()
        if not maj:
            QMessageBox.warning(self, "توجه", "ابتدا یک رشته انتخاب کنید.")
            return
        grade = self.grade_combo.currentText()
        import sqlite3
        try:
            conn = sqlite3.connect('school.db')
            c = conn.cursor()
            c.execute("SELECT id FROM grade WHERE name=?", (grade,))
            gr = c.fetchone()
            if not gr:
                QMessageBox.warning(self, "خطا", "پایه یافت نشد.")
                return
            gid = gr[0]
            c.execute("SELECT id FROM major WHERE name=? AND grade_id=?", (maj, gid))
            mr = c.fetchone()
            if not mr:
                QMessageBox.warning(self, "خطا", "رشته یافت نشد.")
                return
            mid = mr[0]
            c.execute("SELECT COUNT(*) FROM students WHERE major_id=?", (mid,))
            cnt = c.fetchone()[0]
            if cnt > 0:
                QMessageBox.warning(self, "خطا", "نمی‌توان رشته‌ای را حذف کرد که دانش‌آموز دارد.")
                return
            reply = QMessageBox.question(self, "حذف رشته", f"آیا از حذف رشته '{maj}' مطمئن هستید؟", QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes:
                return
            c.execute("DELETE FROM major WHERE id=?", (mid,))
            conn.commit()
            QMessageBox.information(self, "حذف شد", "رشته حذف شد.")
            self.update_major_combo()
        except Exception as e:
            QMessageBox.critical(self, "خطا", str(e))
        finally:
            try:
                conn.close()
            except Exception:
                pass
    def import_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "انتخاب فایل اکسل", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            try:
                # read with pandas and try to handle files with extra header/footer rows
                df = pd.read_excel(file_path, dtype=str)
                # drop completely empty rows
                df = df.dropna(how='all')
                # normalize columns to lowercase ascii/persian-less keys for flexible matching
                original_columns = list(df.columns)
                norm_map = {}
                import re
                def norm(s):
                    if s is None:
                        return ''
                    s = str(s).strip().lower()
                    # remove punctuation and spaces so headers like 'نام:' or 'name ' match
                    # use Arabic/Persian Unicode block \u0600-\u06FF
                    try:
                        s = re.sub(r"[^0-9A-Za-z\u0600-\u06FF]+", "", s)
                    except re.error:
                        # fallback: remove non-alphanumeric
                        s = re.sub(r"[^0-9A-Za-z]+", "", s)
                    return s
                for col in original_columns:
                    norm_map[norm(col)] = col

                # helper to find column by several possible keys
                def find_col(*candidates):
                    for cand in candidates:
                        nc = norm(cand)
                        if nc in norm_map:
                            return norm_map[nc]
                    return None

                # possible names in Persian and English
                name_col = find_col('name', 'نام')
                last_name_col = find_col('last_name', 'نام خانوادگی', 'نامخانوادگی', 'lastname', 'family')
                father_name_col = find_col('father_name', 'نام پدر', 'نام_پدر', 'father', 'والد', 'پدر')
                # common phone column names (Persian/English): موبایل پدر, شماره پدر, father_phone
                father_phone_col = find_col('father_phone', 'شماره پدر', 'fatherphone', 'father_phone_number', 'موبایل پدر', 'موبایلفدر', 'پدرموبایل')
                # common mother column names
                mother_phone_col = find_col('mother_phone', 'شماره مادر', 'mother', 'mother_phone_number', 'موبایل مادر', 'مادرموبایل')
                # student's own mobile / home phone
                student_phone_col = find_col('mobile', 'موبایل', 'تلفن', 'phone', 'موبایل ', 'تلفن منزل')
                # prefer national id if present
                student_code_col = find_col('student_code', 'کد دانش‌آموز', 'studentcode')
                national_id_col = find_col('national_id', 'کد ملی', 'melli', 'nationalid')
                if national_id_col:
                    student_code_col = national_id_col

                # if no name column found, abort with a helpful message
                if not name_col:
                    QMessageBox.critical(self, "خطا", "ستون نام در فایل اکسل پیدا نشد. لطفاً فایل را بررسی کنید (header row).")
                    return

                # keep only rows which have at least a name
                df = df[df[name_col].notna()]
                # debug: print detected columns mapping
                try:
                    print('Excel columns:', original_columns)
                    print('Normalized map:', norm_map)
                except Exception:
                    pass
                import sqlite3
                conn = sqlite3.connect('school.db')
                c = conn.cursor()
                # افزودن پایه و رشته اگر وجود ندارند
                grade = self.grade_combo.currentText()
                major = self.major_combo.currentText()
                c.execute("INSERT OR IGNORE INTO grade (name) VALUES (?)", (grade,))
                conn.commit()
                c.execute("SELECT id FROM grade WHERE name=?", (grade,))
                grade_id = c.fetchone()[0]
                c.execute("INSERT OR IGNORE INTO major (name, grade_id) VALUES (?, ?)", (major, grade_id))
                conn.commit()
                c.execute("SELECT id FROM major WHERE name=? AND grade_id=?", (major, grade_id))
                major_id = c.fetchone()[0]
                inserted = 0
                for _, row in df.iterrows():
                    # build full name from first and last name columns if available
                    first_part = row.get(name_col, '') if name_col and name_col in row.index else ''
                    last_part = row.get(last_name_col, '') if last_name_col and last_name_col in row.index else ''
                    first_part = str(first_part).strip()
                    last_part = str(last_part).strip()
                    if last_part:
                        name = f"{first_part} {last_part}".strip()
                    else:
                        name = first_part
                    if not name:
                        continue
                    father_name = row.get(father_name_col, '') if father_name_col and father_name_col in row.index else ''
                    father_phone = row.get(father_phone_col, '') if father_phone_col and father_phone_col in row.index else ''
                    mother_phone = row.get(mother_phone_col, '') if mother_phone_col and mother_phone_col in row.index else ''
                    student_code = row.get(student_code_col, '') if student_code_col and student_code_col in row.index else ''

                    # basic strip and normalization
                    # name already constructed and stripped above
                    father_name = str(father_name).strip()
                    father_phone = str(father_phone).strip()
                    mother_phone = str(mother_phone).strip()
                    student_code = str(student_code).strip()

                    # insert
                    c.execute(
                        "INSERT INTO students (name, father_name, mother_phone, father_phone, student_code, grade_id, major_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (name, father_name, mother_phone, father_phone, student_code, grade_id, major_id)
                    )
                    inserted += 1
                conn.commit()
                conn.close()
                self.load_students()
                QMessageBox.information(self, "موفق", f"{inserted} دانش‌آموز وارد شد (از {len(df)} ردیف).")
            except Exception as e:
                QMessageBox.critical(self, "خطا", str(e))
        try:
            self.students_list.clear()
            import sqlite3
            conn = sqlite3.connect('school.db')
            try:
                c = conn.cursor()
                grade = self.grade_combo.currentText()
                major = self.major_combo.currentText()

                # دریافت id پایه و رشته انتخاب‌شده
                c.execute("SELECT id FROM grade WHERE name=?", (grade,))
                grade_id = c.fetchone()
                c.execute("SELECT id FROM major WHERE name=? AND grade_id=?", (major, grade_id[0] if grade_id else None))
                major_id = c.fetchone()

                # بررسی وجود پایه و رشته در پایگاه داده
                if grade_id and major_id:
                    c.execute("SELECT name, father_name, student_code, father_phone, mother_phone FROM students WHERE grade_id=? AND major_id=?", (grade_id[0], major_id[0]))
                    students = c.fetchall()

                    # افزودن دانش‌آموزان به لیست با چک‌باکس
                    for s in students:
                        # s => (name, father_name, student_code, father_phone, mother_phone)
                        item = QListWidgetItem(f"نام: {s[0]} | نام پدر: {s[1]} | کد دانش‌آموز: {s[2]} | شماره پدر: {s[3]} | شماره مادر: {s[4] if len(s) > 4 else ''}")
                        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                        item.setCheckState(Qt.Unchecked)
                        self.students_list.addItem(item)

                    # راست‌چین کردن متن‌ها
                    self.students_list.setLayoutDirection(Qt.RightToLeft)
                else:
                    self.students_list.clear()  # پاک کردن لیست در صورت عدم وجود داده
                    QMessageBox.warning(self, "توجه", "هیچ دانش‌آموزی برای این پایه و رشته یافت نشد.")
            finally:
                conn.close()
        except Exception as e:
            QMessageBox.critical(self, "خطا", str(e))

    def mark_attendance(self):
        try:
            import sqlite3
            from datetime import date
            from sms import send_sms_to_all

            conn = sqlite3.connect('school.db', timeout=10)
            try:
                c = conn.cursor()
                grade = self.grade_combo.currentText()
                major = self.major_combo.currentText()
                c.execute("SELECT id FROM grade WHERE name=?", (grade,))
                gr = c.fetchone()
                if not gr:
                    QMessageBox.warning(self, "خطا", "پایه یافت نشد.")
                    return
                grade_id = gr[0]
                c.execute("SELECT id FROM major WHERE name=? AND grade_id=?", (major, grade_id))
                mr = c.fetchone()
                if not mr:
                    QMessageBox.warning(self, "خطا", "رشته یافت نشد.")
                    return
                major_id = mr[0]

                # جمع‌آوری آیتم‌های انتخاب‌شده
                selected_items = []
                for index in range(self.students_list.count()):
                    item = self.students_list.item(index)
                    if item.checkState() == Qt.Checked:
                        selected_items.append(item)

                if not selected_items:
                    QMessageBox.warning(self, "توجه", "لطفاً حداقل یک دانش‌آموز را انتخاب کنید.")
                    return

                # یک بار پرسش برای همه‌ی دانش‌آموزان انتخاب‌شده
                count = len(selected_items)
                status = QMessageBox.question(
                    self,
                    "ثبت وضعیت",
                    f"{count} دانش‌آموز انتخاب شده‌اند. آیا همه‌ی آنها حاضر هستند؟ (بله=حاضر، خیر=غایب)",
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                )
                if status == QMessageBox.Cancel:
                    return

                # پرسش برای ارسال پیامک: برای همه‌ی انتخاب‌شده یک بار پرسیده می‌شود
                from PyQt5.QtWidgets import QInputDialog
                notify_options = ["پدر", "مادر", "هر دو", "هیچ‌کدام"]
                notify_choice, notify_ok = QInputDialog.getItem(self, "ارسال پیامک", "کدام والد پیامک دریافت کند؟", notify_options, 0, False)
                if not notify_ok:
                    # اگر کاربر پنجره را بست، فرض می‌کنیم هیچ کدام
                    notify_choice = "هیچ‌کدام"

                # اعمال وضعیت انتخاب‌شده برای همه‌ی آیتم‌ها
                for item in selected_items:
                    # پاک کردن احتمالی آیکون قبلی از متن آیتم
                    text = item.text()
                    if text.startswith('✅ ') or text.startswith('❌ '):
                        text = text[2:]
                    student_name = text.split('|')[0].split(':')[1].strip()
                    c.execute("SELECT id, father_phone, mother_phone FROM students WHERE name=? AND grade_id=? AND major_id=?", (student_name, grade_id, major_id))
                    student_row = c.fetchone()
                    if not student_row:
                        continue
                    student_id, father_phone, mother_phone = student_row

                    if status == QMessageBox.Yes:
                        c.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)", (student_id, date.today().isoformat(), 'حاضر'))
                        message = f"دانش‌آموز {student_name} امروز در مدرسه حاضر بود.دبیرستان نام مدرسه ی شما "
                        item.setText(f"✅ {text}")
                    else:
                        c.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)", (student_id, date.today().isoformat(), 'غایب'))
                        message = f"دانش‌آموز {student_name} امروز در مدرسه غایب بود. دبیرستان نام مدرسه ی شما"
                        item.setText(f"❌ {text}")

                    # تعیین گیرنده(گان) پیامک بر اساس انتخاب کاربر
                    targets = []
                    if notify_choice == "پدر":
                        if father_phone:
                            targets.append(father_phone)
                    elif notify_choice == "مادر":
                        if mother_phone:
                            targets.append(mother_phone)
                    elif notify_choice == "هر دو":
                        if father_phone:
                            targets.append(father_phone)
                        if mother_phone:
                            targets.append(mother_phone)
                    # "هیچ‌کدام" -> targets stays empty

                    if targets:
                        send_sms_to_all(targets, message)

                conn.commit()
                QMessageBox.information(self, "ثبت شد", "وضعیت حضور/غیاب برای دانش‌آموزان انتخاب‌شده ثبت شد.")
            finally:
                conn.close()
        except Exception as e:
            QMessageBox.critical(self, "خطا", str(e))

    # بارگذاری لیست دانش‌آموزان هنگام تغییر پایه یا رشته
    def showEvent(self, event):
        self.load_students()
        super().showEvent(event)

    def changeEvent(self, event):
        if event.type() == 105:  # QEvent.ActivationChange
            self.load_students()
        super().changeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
