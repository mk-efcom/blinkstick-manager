from PyQt6.QtCore import QThread, QObject, pyqtSignal, QDir
from PyQt6.QtWidgets import QMainWindow, QGraphicsBlurEffect, QListWidgetItem
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap, QIcon
from blinkstick import blinkstick
from blinkstick.blinkstick import BlinkStick
from typing import List
import utils
from ui.Device import Device


class Worker(QObject):
    finished = pyqtSignal(object)
    def __init__(self, funcref, *args):
        super().__init__()
        self.__funcToRunArgs = args
        self.funcToRun = funcref

    def run(self):
        res = self.funcToRun(*self.__funcToRunArgs)
        if self.finished is not None:
            self.finished.emit(res)

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        self.thread = None
        self.selected_device = None
        QDir.addSearchPath("background", '/')
        loadUi('ui/main.ui', self)
        self.__setup_ui()

    def __setup_ui(self):
        self.setStyleSheet("background-image: url(ui/background.jpg)")
        px_cube = QPixmap('ui/blinkcube.png')
        self.lbl_cube.setPixmap(px_cube)
        ic_search = QIcon('ui/search.ico')
        self.btn_search.setIcon(ic_search)
        self.btn_search.clicked.connect(self.scan_devices)
        # blur = QGraphicsBlurEffect()
        # blur.setBlurRadius(10)
        # self.lst_devices.setGraphicsEffect(blur)
        self.scan_devices()

    def __exec_threaded(self, func, callback, *args):
        self.thread = QThread()
        self.worker = Worker(func, *args)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        if callback is not None:
            self.worker.finished.connect(callback)
        self.thread.start()

    def scan_devices(self):
        self.__exec_threaded(blinkstick.find_all, self.__load_devices)

    def __save_device_name(self, name, snr):
        self.__exec_threaded(utils.save_device_data, None, name, snr)
        

    def __load_devices(self, results: List[BlinkStick]):
        print(results)
        if results is None or len(results) == 0:
            self.lbl_info.setText("No compatible devices found.")
        else:
            self.lbl_info.setText(f"Found {len(results)} compatible devices.")
            children = [self.lst_devices.itemWidget(self.lst_devices.item(i)) for i in range(self.lst_devices.count())]
            serials = []
            for stick in results:
                sn = stick.get_serial()
                serials.append(sn)
                if not any(isinstance(device, Device) and device.lbl_sn.text() == sn for device in children):
                    deviceWidget = Device()
                    deviceWidget.onNameChanged.connect(self.__save_device_name)
                    name = utils.get_device_data(sn)
                    if name is not None:
                        deviceWidget.le_name.setText(name)
                    deviceWidget.lbl_sn.setText(sn)
                    deviceWidget.fr_cube.clicked.connect(self.__onDeviceSelected)
                    item = QListWidgetItem(self.lst_devices)
                    item.setSizeHint(deviceWidget.sizeHint())
                    self.lst_devices.addItem(item)
                    self.lst_devices.setItemWidget(item, deviceWidget)
            for child in children:
                if isinstance(child, Device) and child.lbl_sn.text() not in serials:
                    self.lst_devices.removeWidget(child)
    def __onDeviceSelected(self):
        if self.selected_device is not None:
            self.selected_device.parent().setStyleSheet('')
        self.selected_device = self.sender()
        self.selected_device.parent().setStyleSheet('background: rgba(100,240,220,25)')
            