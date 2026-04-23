import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton)
from PyQt5.QtCore import Qt

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Chat UI")
        self.resize(1200, 500)

        # Основной виджет и слой
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 1. Поле истории чата (только для чтения)
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.layout.addWidget(self.chat_history)

        # 2. Нижняя панель (ввод сообщения + кнопка)
        self.input_layout = QHBoxLayout()
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Напиши сообщение...")
        # Отправка по нажатию Enter
        self.message_input.returnPressed.connect(self.send_message)
        
        self.send_button = QPushButton("Отправить")
        self.send_button.clicked.connect(self.send_message)

        self.input_layout.addWidget(self.message_input)
        self.input_layout.addWidget(self.send_button)
        
        self.layout.addLayout(self.input_layout)

    def send_message(self):
        text = self.message_input.text().strip()
        if text:
            # Добавляем текст в историю
            self.chat_history.append(f"<b>Вы:</b> {text}")
            # Очищаем поле ввода
            self.message_input.clear()
            # Прокрутка вниз
            self.chat_history.verticalScrollBar().setValue(
                self.chat_history.verticalScrollBar().maximum()
            )