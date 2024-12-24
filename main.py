import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal, QObject
from ui.MainUI import MainUI
from usbmonitor import USBMonitor
from usbmonitor.attributes import ID_VENDOR_ID

BS_VENDOR_ID = "20A0"
class VoidSignal(QObject):
    void_signal = pyqtSignal()
    def emit(self):
        self.void_signal.emit()
def device_connect_event(device_id, device_info):
    if device_info[ID_VENDOR_ID] == BS_VENDOR_ID:
        connect_signal.emit()

monitor = USBMonitor()
app = QApplication(sys.argv)
win = MainUI()
connect_signal = VoidSignal(void_signal=win.scan_devices)
win.show()
monitor.start_monitoring(on_connect=device_connect_event, on_disconnect=device_connect_event)
sys.exit(app.exec())

