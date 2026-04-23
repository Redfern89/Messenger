from ui.main_window import ChatWindow
from ui.connect_form import LoginDialog

class UIManager:
	def __init__(self):
		self.login_dialog = None
		self.chat_window = None

	def show_login(self):
		self.login_dialog = LoginDialog()
		self.login_dialog.show()

	def show_chat(self):
		if self.chat_window is None:
			self.chat_window = ChatWindow()
		self.chat_window.show()

	def close_login(self):
		if self.login_dialog:
			self.login_dialog.close()
