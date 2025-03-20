from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QLineEdit
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt
from PIL import ImageGrab
from src.overlay_area import OverlayCaptureArea
from src.android_area import AndroidCaptureArea

class CaptureWindow(QMainWindow):
    def __init__(self, app_manager):
        super().__init__()

        self.app_manager = app_manager

        # ウィンドウの基本設定
        self.setWindowTitle("キャプチャウィンドウ")
        self.setGeometry(100, 100, 600, 400)

        # メインレイアウト
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)

        # ヘッダー（共通ボタンエリア）
        self.header_widget = QWidget()
        self.header_layout = QHBoxLayout(self.header_widget)

        #数字ボックスです
        self.padding_input = QLineEdit()
        self.padding_input.setValidator(QIntValidator(0,500))
        self.padding_input.setText(str(self.app_manager.block_padding))
        self.padding_input.editingFinished.connect(self.padding_edit)






        # モード切り替えボタン
        self.mode_button = QPushButton("切り替え（現在: Web）")
        self.mode_button.clicked.connect(self.toggle_mode)
        
        self.capture_button = QPushButton("撮影")
        self.capture_button.clicked.connect(self.capture)

        self.white_button = QPushButton("白紙")
        self.white_button.clicked.connect(self.spacer)

        self.newline_button = QPushButton("改行")
        self.newline_button.clicked.connect(self.newline)

        self.back_button = QPushButton("戻る")
        self.back_button.clicked.connect(self.remove)

        self.delete_button = QPushButton("削除")
        self.delete_button.clicked.connect(self.delete)

        self.video_button = QPushButton("録画")
        self.video_button.clicked.connect(self.movie)

        self.header_layout.addWidget(self.mode_button)
        self.header_layout.addWidget(self.capture_button)
        self.header_layout.addWidget(self.white_button)
        self.header_layout.addWidget(self.newline_button)
        self.header_layout.addWidget(self.back_button)
        self.header_layout.addWidget(self.delete_button)
        self.header_layout.addWidget(self.video_button)
        self.header_layout.addWidget(self.padding_input)

        self.main_layout.addWidget(self.header_widget)

        # **モード切り替えのための QStackedWidget**
        self.mode_container = QStackedWidget()
        self.overlay_capture = OverlayCaptureArea()
        self.android_capture = AndroidCaptureArea()

        self.mode_container.addWidget(self.overlay_capture)
        self.mode_container.addWidget(self.android_capture)

        self.main_layout.addWidget(self.mode_container)

        # **デフォルトは Web モード**
        self.current_mode = "web"
        self.mode_container.setCurrentWidget(self.overlay_capture)

    def toggle_mode(self):
        if self.app_manager.tap_checker() == True:

            if self.current_mode == "web":
                self.current_mode = "android"
                self.mode_container.setCurrentWidget(self.android_capture)
                self.mode_button.setText("切り替え（現在: Android）")
                self.android_capture.start_androidmode()
            else:
                self.current_mode = "web"
                self.mode_container.setCurrentWidget(self.overlay_capture)
                self.mode_button.setText("切り替え（現在: Web）")
                self.android_capture.stop_androidmode()

    def capture(self):  # 写真取得して投げる
        if self.current_mode == "web":
            # オーバーレイ範囲でPC画面をキャプチャ
            x, y, w, h = self.overlay_capture.get_area()
            screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        else:  # Androidモード
            screenshot = self.android_capture.get_image()
        if screenshot is not None:
            self.app_manager.add_capture_image(screenshot)
        else:
            print("スクリーンショット取得失敗！")

    def spacer(self,):
        self.app_manager.add_spacer_image()

    def newline(self,):
        self.app_manager.add_newline()

    def remove(self,):
        self.app_manager.remove_image()

    def delete(self,):
        self.app_manager.delete_image()





    def padding_edit(self):
        # 入力値を取得して、パディングを更新
        value = int(self.padding_input.text())
        self.app_manager.block_padding = value
        print(f"パディングを {value} に更新！")

    def movie(self,):#テスト用
        print("testevent")

