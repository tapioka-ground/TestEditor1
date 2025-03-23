from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,QApplication,
    QPushButton, QLineEdit, QStackedWidget, QToolBar
)
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtCore import Qt, QSize
from PIL import ImageGrab
from src.overlay_area import OverlayCaptureArea
from src.android_area import AndroidCaptureArea

class CaptureWindow(QMainWindow):
    def __init__(self, app_manager):
        super().__init__()

        self.app_manager = app_manager
        self.bar_title = "--capture(PCmode)--"
        self.connect_name = "Display"
        self.setWindowTitle(self.bar_title)


        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        screen_width = screen_size.width()
        screen_height = screen_size.height()

        target_width = int(screen_width * 0.38)
        target_height = int(screen_height * 0.9)

        self.resize(target_width, target_height)











        self.toolbar = QWidget()
        self.toolbar_layout = QHBoxLayout(self.toolbar)
        self.toolbar_layout.setContentsMargins(10, 5, 10, 5)
        self.toolbar_layout.setSpacing(10)
        self.toolbar.setStyleSheet("""
            background-color: #212121;
        """)

        self.left_widget = QWidget()
        self.left_layout = QHBoxLayout(self.left_widget)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(5)
        self.left_layout.setAlignment(Qt.AlignLeft)

        self.mode_button = self.add_toolbar_button(self.left_layout, "web", self.toggle_mode)

        self.connect_name_field = QLabel(self.connect_name)
        self.connect_name_field.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 14px;
                padding: 4px;
                padding-left: 20px;
            }
        """)
        self.left_layout.addWidget(self.connect_name_field)


        self.center_widget = QWidget()
        self.center_layout = QHBoxLayout(self.center_widget)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(5)
        self.center_layout.setAlignment(Qt.AlignCenter)

        for name in ["remove","capture", "spacer", "newline"]:
            self.add_toolbar_button(self.center_layout, name, getattr(self, name))
#こいつパディング欄
        self.padding_input = QLineEdit()
        self.padding_input.setFixedHeight(28)
        self.padding_input.setFixedWidth(44)
        self.padding_input.setValidator(QIntValidator(0, 500))
        self.padding_input.setText(str(self.app_manager.block_padding))
        self.padding_input.setAlignment(Qt.AlignCenter)
        self.padding_input.setPlaceholderText("Pad")
        self.padding_input.setStyleSheet("""
            QLineEdit {
                background-color: #2e2e2e;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #00aaff;
                background-color: #3a3a3a;
            }
        """)
        self.padding_input.editingFinished.connect(self.padding_edit)
        self.center_layout.addWidget(self.padding_input)


        self.right_widget = QWidget()
        self.right_layout = QHBoxLayout(self.right_widget)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(5)
        self.right_layout.setAlignment(Qt.AlignRight)

        for name in ["saveas_DB", "movie", "delete"]:
            self.add_toolbar_button(self.right_layout, name, getattr(self, name))

        self.toolbar_layout.addWidget(self.left_widget, 1)
        self.toolbar_layout.addWidget(self.center_widget, 1)
        self.toolbar_layout.addWidget(self.right_widget, 1)

        self.central_widget = QWidget()#メインレイアウト
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        self.central_widget.setStyleSheet("""
            background-color: #282828
            """)

        self.central_layout.addWidget(self.toolbar)
        self.setCentralWidget(self.central_widget)

        self.overlay_capture = OverlayCaptureArea()
        self.android_capture = AndroidCaptureArea(parent_window=self)

        self.android_container = QWidget()
        self.android_layout = QHBoxLayout(self.android_container)
        self.android_layout.setAlignment(Qt.AlignCenter)
        self.android_layout.setContentsMargins(0, 0, 0, 0)
        self.android_layout.addWidget(self.android_capture)


        self.mode_container = QStackedWidget()
        self.mode_container.addWidget(self.overlay_capture)
        self.mode_container.addWidget(self.android_container)

        self.central_layout.addWidget(self.mode_container)

        self.current_mode = "web"
        self.mode_container.setCurrentWidget(self.overlay_capture)

        self.padding_input.clearFocus()

    def showEvent(self, event):  #Awakeみたいな感じ
        super().showEvent(event)
        self.padding_input.clearFocus()
        self.central_widget.setFocus()



    def add_toolbar_button(self, layout, name, callback):
        button = QPushButton()
        button.setFixedSize(28, 28)
        button.setIconSize(QSize(20, 20))

        icon = QIcon(f"src/svg/{name}.svg")
        button.setIcon(icon)

        button.setStyleSheet(f"""
            QPushButton {{
                background-color: #272727;
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #444444;
            }}
        """)
        button.clicked.connect(callback)
        layout.addWidget(button)
        return button


    def toggle_mode(self):#ボタン系
        if not self.app_manager.tap_checker():
            return

        if self.current_mode == "web":
            self.current_mode = "android"
            self.mode_container.setCurrentWidget(self.android_container)
            self.android_capture.start_androidmode()
            self.bar_title = "--capture(Androidmode)--"
            self.setWindowTitle(self.bar_title)
            self.mode_button.setIcon(QIcon("src/svg/android.svg"))
        else:
            self.current_mode = "web"
            self.mode_container.setCurrentWidget(self.overlay_capture)
            self.android_capture.stop_androidmode()
            self.bar_title = "--capture(PCmode)--"
            self.setWindowTitle(self.bar_title)
            self.connect_name_field.setText("Display")
            self.mode_button.setIcon(QIcon("src/svg/web.svg"))

    def change_device_name(self, name):
        self.connect_name = name
        text = f'<span style="font-size:8px;color: #00ff00;">●</span>  {self.connect_name}'
        self.connect_name_field.setText(text)


    def capture(self):
        if self.current_mode == "web":
            x, y, w, h = self.overlay_capture.get_area()
            screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        else:
            screenshot = self.android_capture.get_image()

        if screenshot:
            self.app_manager.add_capture_image(screenshot)
        else:
            print("スクリーンショット取得失敗！")

    def spacer(self):
        self.app_manager.add_spacer_image()

    def newline(self):
        self.app_manager.add_newline()

    def remove(self):
        self.app_manager.remove_image()

    def delete(self):
        self.app_manager.delete_image()

    def saveas_DB(self):
        self.android_capture.create_DB()

    def movie(self):
        print("testevent")

    def padding_edit(self):
        value = int(self.padding_input.text())
        self.app_manager.block_padding = value
        print(f"パディングを {value} に更新！")
        self.padding_input.clearFocus()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.current_mode == "android":
            self.resize_android_capture()

    def resize_android_capture(self):#検討中の遣唐使の剣闘士の健闘した。
        self.android_layout.setContentsMargins(0, 20, 0, 20)


