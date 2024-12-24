from PyQt6.uic.load_ui import loadUi
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import pyqtSignal
from ui.strings import *
import pickle
class Device(QWidget):
    onNameChanged = pyqtSignal(str, str)
    def __init__(self):
        super(Device, self).__init__()
        loadUi("ui/QDevice.ui", self)
        self.__init_ui()
    def __init_ui(self):
        self.fr_cube.setStyleSheet('border-image: url(ui/blinkcube.png) 0 0 0 0 stretch stretch;\n')
        self.le_name.setText(str_device_default_name)
        self.last_name = str_device_default_name
        self.le_name.onLostFocus.connect(self.__bringDefault)
        self.le_name.onMousePressed.connect(self.__clearDefault)
        # self.le_name = MyLineEdit(self.__bringDefault, self.__clearDefault)
        # self.verticalLayout.addWidget(ConsciousLineEdit(self.__bringDefault, self.__clearDefault, str_device_default_name))
    
    def __clearDefault(self):
        self.le_name.setReadOnly(False)
        if self.le_name.text() == str_device_default_name:
            self.le_name.clear()

    def __bringDefault(self):
        self.le_name.setReadOnly(True)
        if self.le_name.text() == "":
            self.le_name.setText(str_device_default_name)
        if(self.le_name.text() != self.last_name):
            self.onNameChanged.emit(self.le_name.text(), self.lbl_sn.text())
        self.last_name = self.le_name.text()
        


class ConsciousLineEdit(QLineEdit):
    onLostFocus = pyqtSignal()
    onMousePressed = pyqtSignal()
    def __init__(self, defaultText="", *args, **kwargs):
        super(ConsciousLineEdit, self).__init__(*args, **kwargs)
        self.setText(defaultText)
    def focusOutEvent(self, event):
        self.onLostFocus.emit()
        super(ConsciousLineEdit, self).focusInEvent(event)
    def mousePressEvent(self, event):
        self.onMousePressed.emit()
        super( ConsciousLineEdit, self).mousePressEvent(event)

