import sys
import json
from random import choice, randint, shuffle
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import pyperclip

class PasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Manager")
        self.setFixedSize(600, 300)

        self.central_Widget = QWidget()
        self.setCentralWidget(self.central_Widget)

        self.layout = QVBoxLayout()
        self.central_Widget.setLayout(self.layout)

        self.logo_label = QLabel()
        self.logo_label.setPixmap(QIcon("security.png").pixmap(150, 150))
        self.layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.website_layout = QHBoxLayout()
        self.layout.addLayout(self.website_layout)

        self.website_label = QLabel("Website: ")
        self.website_entry = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.find_password)

        self.website_layout.addWidget(self.website_label)
        self.website_layout.addWidget(self.website_entry)
        self.website_layout.addWidget(self.search_button)

        self.eu_layout = QHBoxLayout()
        self.layout.addLayout(self.eu_layout)

        self.eu_label = QLabel("Email/Username: ")
        self.eu_entry = QLineEdit()
        self.eu_entry.setText("hoodstar417@gmail.com")

        self.eu_layout.addWidget(self.eu_label)
        self.eu_layout.addWidget(self.eu_entry)

        # Password
        self.password_layout = QHBoxLayout()
        self.layout.addLayout(self.password_layout)

        self.password_label = QLabel("Password: ")
        self.password_entry = QLineEdit()
        self.generate_password_button = QPushButton("Generate password")
        self.generate_password_button.clicked.connect(self.generate_password)

        self.password_layout.addWidget(self.password_label)
        self.password_layout.addWidget(self.password_entry)
        self.password_layout.addWidget(self.generate_password_button)

        # Add Button
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_info)
        self.layout.addWidget(self.add_button)

        self.setStyleSheet("background-color: deepskyblue")

    def find_password(self):
        search_query = self.website_entry.text()
        try:
            with open("data.json", mode="r") as df:
                pass_data = json.load(df)
                result_e = pass_data[search_query]["email"]
                result_p = pass_data[search_query]["password"]
        except KeyError:
            QMessageBox.warning(self, "Error", "There is no entry under that name")
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No entries have been added yet.")
        except:
            QMessageBox.warning(self, "Error", "No entries have been added yet.")
        else:
            if search_query in pass_data:
                QMessageBox.information(self, search_query, f"email: {result_e}\npassword: {result_p}")

    def generate_password(self):
        letters = [chr(i) for i in range(ord('a'), ord('z') + 1)] + [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        numbers = [str(i) for i in range(10)]
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        password_letters = [choice(letters) for _ in range(randint(8, 10))]
        password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
        password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
        password_list = password_letters + password_numbers + password_symbols

        shuffle(password_list)

        password = "".join(password_list)

        self.password_entry.setText(password)
        pyperclip.copy(password)

    def add_info(self):
        website = self.website_entry.text()
        eu = self.eu_entry.text()
        password = self.password_entry.text()
        new_data = {
            website: {
                "email": eu,
                "password": password
            }
        }

        if len(website) < 1 or len(password) < 1:
            QMessageBox.warning(self, "Error", "Please don't leave any fields empty!")
        else:
            try:
                with open("data.json", mode="r") as df:
                    data = json.load(df)
            except FileNotFoundError:
                with open("data.json", mode="w") as df:
                    json.dump(new_data, df, indent=4)
            else:
                data.update(new_data)
                with open("data.json", mode="w") as df:
                    json.dump(data, df, indent=4)

            finally:
                self.website_entry.clear()
                self.password_entry.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = PasswordManager()
    window.show()
    sys.exit(app.exec())
