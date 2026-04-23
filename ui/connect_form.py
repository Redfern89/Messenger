import sys
from PyQt5.QtWidgets import (
	QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
	QLineEdit, QPushButton, QFormLayout, QMessageBox
)

from PyQt5.QtCore import Qt, pyqtSignal

class LoginDialog(QDialog):
	login_requested = pyqtSignal(str, str, str, str)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle('Подключение к серверу')
		self.setFixedSize(520, 250)

		# Основной контейнер
		layout = QVBoxLayout(self)
		
		# Сетка формы для меток и полей
		self.form = QFormLayout()
		
		# Поля ввода
		self.ip_input = QLineEdit(self)
		self.ip_input.setPlaceholderText('127.0.0.1')
		self.ip_input.setText("127.0.0.1")
		
		self.port_input = QLineEdit(self)
		self.port_input.setPlaceholderText('8000')
		self.port_input.setText("8000")
		
		self.login_input = QLineEdit(self)
		self.login_input.setText("Redfern89")
		
		self.password_input = QLineEdit(self)
		self.password_input.setText("password000")
		self.password_input.setEchoMode(QLineEdit.Password) # Скрываем пароль звездочками

		self.form.addRow('IP адрес:', self.ip_input)
		self.form.addRow('Порт:', self.port_input)
		self.form.addRow('Логин:', self.login_input)
		self.form.addRow('Пароль:', self.password_input)
		
		layout.addLayout(self.form)

		# Кнопки управления
		btn_layout = QHBoxLayout()
		self.btn_login = QPushButton('Войти')
		self.btn_cancel = QPushButton('Отмена')
		
		btn_layout.addWidget(self.btn_login)
		btn_layout.addWidget(self.btn_cancel)
		layout.addLayout(btn_layout)

		# Обработка нажатий
		self.btn_login.clicked.connect(self.request_login)  # Закрывает с кодом 1
		self.btn_cancel.clicked.connect(self.reject) # Закрывает с кодом 0

	def request_login(self):
		self.btn_login.setEnabled(False)
		QApplication.setOverrideCursor(Qt.WaitCursor)

		host = self.ip_input.text()
		port = self.port_input.text()
		login = self.login_input.text()
		password = self.password_input.text()

		self.login_requested.emit(host, port, login, password)
		
	def on_login_success(self):
		self.btn_login.setEnabled(True)
		QApplication.restoreOverrideCursor()		
		self.accept()

	def on_login_failed(self, message):
		self.btn_login.setEnabled(True)
		QApplication.restoreOverrideCursor()
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Icon.Critical)

		msg.setWindowTitle("Error")
		msg.setText(message)
		msg.setStandardButtons(QMessageBox.StandardButton.Ok)
		msg.exec()