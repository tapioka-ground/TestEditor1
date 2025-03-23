from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QApplication
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
from PIL import ImageQt
from src.canvas_view import CanvasView
from src.backlog_submit import BacklogSubmit
from datetime import datetime
import os
import tempfile


class EditorWindow(QMainWindow):
    def __init__(self, app_manager):
        super().__init__()

        self.app_manager = app_manager
        self.setWindowTitle("Editor")

        self.window_bg_color = "#444444"



        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        screen_width = screen_size.width()
        screen_height = screen_size.height()

        target_width = int(screen_width * 0.6)
        target_height = int(screen_height * 0.9)

        self.resize(target_width, target_height)










        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        self.central_widget.setStyleSheet(f"background-color: {self.window_bg_color};")
        self.setCentralWidget(self.central_widget)

        self.create_header()
        self.create_canvas()

        self.current_mode = "none"


    def create_header(self):
        self.header_widget = QWidget()
        self.header_layout = QHBoxLayout(self.header_widget)
        self.header_layout.setContentsMargins(10, 5, 10, 5)
        self.header_layout.setSpacing(10)
        self.header_widget.setStyleSheet("background-color: #212121;")

        self.left_widget = QWidget()
        self.left_layout = QHBoxLayout(self.left_widget)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(5)
        self.left_layout.setAlignment(Qt.AlignLeft)

        self.back_button = self.add_toolbar_button(self.left_layout, "back", self.test)
        self.edit_button = self.add_toolbar_button(self.left_layout, "edit", lambda: self.set_mode("edit"))

        self.center_widget = QWidget()
        self.center_layout = QHBoxLayout(self.center_widget)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(5)
        self.center_layout.setAlignment(Qt.AlignCenter)

        self.draw_button = self.add_toolbar_button(self.center_layout, "draw", lambda: self.set_mode("draw"))
        self.arrow_button = self.add_toolbar_button(self.center_layout, "arrow", lambda: self.set_mode("arrow"))
        self.text_button = self.add_toolbar_button(self.center_layout, "text", lambda: self.set_mode("text"))

        self.right_widget = QWidget()
        self.right_layout = QHBoxLayout(self.right_widget)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(5)
        self.right_layout.setAlignment(Qt.AlignRight)

        self.export_button = self.add_toolbar_button(self.right_layout, "export", self.export_canvas)
        self.backlog_button = self.add_toolbar_button(self.right_layout, "backlog", self.send_backlog)

        self.header_layout.addWidget(self.left_widget, 1)
        self.header_layout.addWidget(self.center_widget, 1)
        self.header_layout.addWidget(self.right_widget, 1)

        self.central_layout.addWidget(self.header_widget)


    def create_canvas(self):
        self.canvas_view = CanvasView(self, bg_color="#FFFFFF")
        self.central_layout.addWidget(self.canvas_view)

    def add_toolbar_button(self, layout, icon_name, callback):
        button = QPushButton()
        button.setFixedSize(28, 28)
        button.setIconSize(QSize(20, 20))

        icon = QIcon(f"src/svgt/{icon_name}.svg")
        button.setIcon(icon)

        button.setStyleSheet("""
            QPushButton {
                background-color: #272727;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        button.clicked.connect(callback)
        layout.addWidget(button)
        return button

    def set_mode(self, modename):
        self.current_mode = modename
        print(f"モード切り替え: {modename}")
        self.canvas_view.setcanvasmode(self.current_mode)

    def export_canvas(self):
        filename, _ = QFileDialog.getSaveFileName(self, "エクスポート", "", "PNG Files (*.png)")
        if filename:
            self.canvas_view.export_scene_to_image(filename)
            print(f"画像を保存しました: {filename}")


    def send_backlog(self):
        print("バックログに投稿")

        pixmap = self.canvas_view.export_scene_to_pixmap()

        self.backlog_window = BacklogSubmit(self.app_manager, pixmap)
        self.backlog_window.show()


    def test(self):
        print("戻る")

    def update_canvas(self, image_dict, padding):
        self.canvas_view.clear_canvas()

        x_offset = padding
        y_offset = padding
        self.block_width = 200
        max_row_height = 0
        max_total_width = 0

        for image_id, data in image_dict.items():
            if data == "":
                x_offset += self.block_width + padding
                continue

            elif data == "new":
                print("改行だよ！")
                x_offset = padding
                y_offset += max_row_height + padding
                max_row_height = 0
                continue

            qt_image = ImageQt.ImageQt(data)
            pixmap = QPixmap.fromImage(qt_image)
            if image_id == 0:
                self.block_width = pixmap.width()

            self.canvas_view.add_image(pixmap, position=(x_offset, y_offset))

            x_offset += pixmap.width() + padding
            max_row_height = max(max_row_height, pixmap.height())
            max_total_width = max(max_total_width, x_offset)

        total_width = max_total_width + padding
        total_height = y_offset + max_row_height + padding
        self.canvas_view.set_scene_rect(total_width, total_height)

        self.fit_canvas_to_window()

    def fit_canvas_to_window(self):
        if not hasattr(self, 'canvas_view') or self.canvas_view is None:
            return

        view = self.canvas_view
        scene_rect = view.scene.sceneRect()
        if not scene_rect.isNull():
            view.fitInView(scene_rect, Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_canvas_to_window()
