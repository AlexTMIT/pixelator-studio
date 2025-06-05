
import sys
from PySide6.QtWidgets import QApplication
from model.model import AppModel
from controller.controller import AppController
from view.main_window import MainWindow

app = QApplication(sys.argv)

model = AppModel()
view = MainWindow()
controller = AppController(model, view)

view.show()
app.exec()