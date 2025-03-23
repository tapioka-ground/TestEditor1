from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QPixmap, QImage
from src.capture_thread import Capture_Thread

class AndroidCaptureArea(QWidget):
    def __init__(self, parent_window=None):
        super().__init__()

        self.parent_window = parent_window

        self.original_width = 1000
        self.original_height = 400

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel("接続中...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.last_capture_image = None

        self.thread = QThread()    #ADB用スレっど
        self.worker = Capture_Thread()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.start_loop)
        self.worker.image_ready.connect(self.update_android_screen)
        self.worker.error.connect(self.show_error)

        self.worker.device_name_set.connect(self.path_device_name)

    def path_device_name(self,name):
        print(name + "が接続されました")
        self.parent_window.change_device_name(name)


    def get_image(self,):
        return self.last_capture_image




    def start_androidmode(self):
        print("キャプチャ開始")
        self.thread.start()

    def stop_androidmode(self):
        print("キャプチャ終わり")
        self.worker.stop_loop()
        self.thread.quit()
        self.thread.wait()

    def update_android_screen(self, pil_image):
        self.last_capture_image = pil_image
        qt_image = self.pil_to_qimage(pil_image)

        self.original_width, self.original_height = pil_image.size

        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap)

        #検討中まだいらん
        self.parentWidget().parentWidget()
        self.parent_window.resize_android_capture()
        width, height = pil_image.size
        self.setFixedSize(width, height)
        self.image_label.setPixmap(pixmap)
        self.image_label.setFixedSize(width, height)

    def show_error(self, message):
        print("エラー:", message)
        self.image_label.setText("接続中...")

    def pil_to_qimage(self, pil_image):
        pil_image = pil_image.convert("RGB")
        width, height = pil_image.size
        data = pil_image.tobytes("raw", "RGB")
        return QImage(data, width, height, QImage.Format_RGB888)




    def create_DB(self,):

        self.worker.get_db_signal.emit()

