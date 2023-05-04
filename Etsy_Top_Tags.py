import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window properties
        self.setWindowTitle("Etsy Top Tags")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(500, 500)
        self.setStyleSheet("background-color: #1E1E1E; color: #FFFFFF;")

        # Set the palette for the dark mode
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(50, 50, 50))
        palette.setColor(QPalette.AlternateBase, QColor(30, 30, 30))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(50, 50, 50))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

        # Create the widgets
        self.title_label = QLabel("Etsy Top Tags")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.number_label = QLabel("Number of tags wanted:")
        self.number_label.setFont(QFont("calibri", 12))
        self.number_edit = QLineEdit()
        self.number_edit.setFont(QFont("calibri", 8))
        self.file_label = QLabel("Select a text file:")
        self.file_label.setFont(QFont("calibri", 12))
        self.file_edit = QLineEdit()
        self.file_edit.setFont(QFont("calibri", 8))
        self.file_edit.setReadOnly(True)
        self.file_button = QPushButton("Browse")
        self.file_button.setFont(QFont("calibri", 12))
        self.generate_button = QPushButton("Generate")
        self.generate_button.setFont(QFont("calibri", 12))
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("calibri", 10))
        self.text_edit.setReadOnly(True)

        # Set the style for the widgets
        self.title_label.setStyleSheet("color: #FFFFFF;")
        self.number_edit.setStyleSheet("background-color: #FFFFFF; color: #000000; border-radius: 5px;")
        self.file_edit.setStyleSheet("background-color: #FFFFFF; color: #000000; border-radius: 5px;")
        self.file_button.setStyleSheet("background-color: #4CAF50; color: #000000; border-radius: 9px;")
        self.generate_button.setStyleSheet("background-color: #4CAF50; color: #000000; border-radius: 9px;")
        self.text_edit.setStyleSheet("background-color: #FFFFFF; color: #000000; border-radius: 5px;")

        # Set the layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addSpacing(20)
        self.number_layout = QHBoxLayout()
        self.number_layout.addWidget(self.number_label)
        self.number_layout.addWidget(self.number_edit)
        self.main_layout.addLayout(self.number_layout)
        self.main_layout.addSpacing(20)
        self.file_layout = QHBoxLayout()
        self.file_layout.addWidget(self.file_label)
        self.file_layout.addWidget(self.file_edit)
        self.file_layout.addWidget(self.file_button)
        self.main_layout.addLayout(self.file_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(self.generate_button)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(self.text_edit)
        self.setLayout(self.main_layout)

        # Connect the buttons to their respective functions
        self.file_button.clicked.connect(self.select_file)
        self.generate_button.clicked.connect(self.generate)

        # Set the default file path
        self.file_path = 'words.txt'

    def select_file(self):
        # Open a file dialog to allow the user to select a text file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"Select a text file", "","Text Files (*.txt)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    lines = f.readlines()
                    lst = [line.strip() for line in lines if line.strip()]
                self.file_path = file_name
                self.file_edit.setText(self.file_path)
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                QMessageBox.critical(self, "Error", error_msg, QMessageBox.Ok)

    def generate(self):
        xx = int(self.number_edit.text())
        try:
            with open(self.file_path, 'r') as f:
                lines = f.readlines()
                lst = [line.strip() for line in lines if line.strip()]
            word_combinations = []
            for i in range(0, len(lst), 2):
                name = lst[i]
                value = lst[i+1].strip("()")
                word_combinations.append(f"{name} ({value})")
            word_count = {}
            word_value = {}
            for phrase in word_combinations:
                if '(' in phrase and ')' in phrase:
                    value_str = phrase.split('(')[1].split(')')[0]
                    value = float(value_str[:-1]) * 1e6 if value_str.endswith('M') else float(value_str[:-1]) * 1e3 if value_str.endswith('K') else float(value_str)
                    words = phrase.split('(')[0].strip()
                else:
                    value = 0
                    words = phrase
                for word in words.split():
                    if word not in word_count:
                        word_count[word] = 1
                        word_value[word] = value if value else 0
                    else:
                        word_count[word] += 1
                        word_value[word] += value if value else 0

            best_phrases = []
            for phrase in word_combinations:
                words = phrase.split('(')[0].strip()
                value_str = phrase.split('(')[1].split(')')[0] if '(' in phrase and ')' in phrase else '0'
                value = float(value_str[:-1]) * 1e6 if value_str.endswith('M') else float(value_str[:-1]) * 1e3 if value_str.endswith('K') else float(value_str)
                score = sum(word_count[word] for word in words.split()) * word_value[words.split()[0]]
                best_phrases.append((phrase, score))

            best_phrases = sorted(best_phrases, key=lambda x: x[1], reverse=True)

            # Display the top phrases in the text edit widget
            self.text_edit.clear()

            for i in range(xx):
                self.text_edit.append("{}\n".format(best_phrases[i][0]))
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            QMessageBox.critical(self, "Error", error_msg, QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
