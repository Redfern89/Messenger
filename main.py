#!/usr/bin/env python3

import sys
import asyncio

from qasync import QEventLoop
from PyQt5.QtWidgets import QApplication
from core.controller import AppController
from core.session import SessionManager
from ui.manager import UIManager

if __name__ == "__main__":
	app_qt = QApplication(sys.argv)

	loop = QEventLoop(app_qt)
	asyncio.set_event_loop(loop)

	session_manager = SessionManager()
	controller = AppController(session_manager)
	ui = UIManager()

	ui.show_login()
	ui.login_dialog.login_requested.connect(controller.handle_login)
	controller.login_success.connect(ui.show_chat)
	controller.login_success.connect(ui.login_dialog.on_login_success)
	controller.login_failed.connect(ui.login_dialog.on_login_failed)

	app_qt.aboutToQuit.connect(
		lambda: asyncio.create_task(session_manager.close())
	)

	with loop:
		loop.run_forever()