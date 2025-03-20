import subprocess
import io
from PIL import Image
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QImage

class AndroidCaptureArea(QWidget):
    def __init__(self):
        super().__init__()

        # Android画面表示用
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: black; border: 5px solid gray;")

        # レイアウトとラベル
        self.layout = QVBoxLayout(self)
        self.image_label = QLabel("接続中...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_android_screen)
        self.setGeometry(200, 200, 1000, 400)  # 初期サイズ（あとで調整）

    def update_android_screen(self):
        """ADBで実機のスクリーンショットを取得して表示"""
        try:
            # adbでスクショ取得（PNGバイナリ）
            result = subprocess.run(
                ["adb", "exec-out", "screencap", "-p"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )

            if result.returncode != 0:#接続失敗
                print("ADB接続エラー:", result.stderr.decode())
                self.image_label.setText("接続中...")
                return

            # 画像データをPILで読み込み
            image_data = result.stdout
            pil_image = Image.open(io.BytesIO(image_data))
            width, height = pil_image.size
            self.setFixedSize(width, height)

            qt_image = self.pil_to_qimage(pil_image)
            pixmap = QPixmap.fromImage(qt_image)
            self.image_label.setPixmap(pixmap)
            self.image_label.setFixedSize(width, height)
            print("表示ループなう")

        except Exception as e:
            print("スクリーン取得エラー:", e)

    def pil_to_qimage(self, pil_image):
        """PIL.Image → QImage 変換"""
        pil_image = pil_image.convert("RGB")
        width, height = pil_image.size
        data = pil_image.tobytes("raw", "RGB")
        return QImage(data, width, height, QImage.Format_RGB888)

    def get_image(self):
        """ADBから直接スクリーンショットを取得して返す"""
        try:
            result = subprocess.run(
                ["adb", "exec-out", "screencap", "-p"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )
            if result.returncode != 0:
                print("ADB接続エラー:", result.stderr.decode())
                return None
            image_data = result.stdout
            pil_image = Image.open(io.BytesIO(image_data))

            return pil_image
        except Exception as e:
            print("スクリーン取得エラー:", e)
            return None


    def start_androidmode(self,):
        self.timer.start(1000)
        print("start")

    def stop_androidmode(self,):
        self.timer.stop()
        print("stop")
