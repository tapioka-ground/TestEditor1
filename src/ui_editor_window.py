from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFileDialog)
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPixmap, QColor, QPainter
from PIL import ImageQt
from src.canvas_view import CanvasView
from src.android_area import AndroidCaptureArea

class EditorWindow(QMainWindow):
    def __init__(self, app_manager):
        super().__init__()

        self.app_manager = app_manager
        self.setWindowTitle("Editor")

        self.window_sizeX = 1000
        self.window_sizeY = 600
        self.setGeometry(600, 100, self.window_sizeX, self.window_sizeY)

        # 背景カラー（外側のウィンドウ）
        self.window_bg_color = "#444444"

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)

        self.main_widget.setStyleSheet(f"background-color: {self.window_bg_color};")
        self.canvas_bg_color = "#FFFFFF"#canvasvueをせってい
        self.canvas_view = CanvasView(self, bg_color=self.canvas_bg_color)
        self.main_layout.addWidget(self.canvas_view)

        self.current_mode = "none" # これedit,draw,arrow,textに分かれるよ

        # ヘッダーWidget
        self.header_widget = QWidget()
        self.header_layout = QHBoxLayout(self.header_widget)

        # 編集モード切り替え
        self.edit_button = QPushButton("編集モード")
        self.edit_button.clicked.connect(lambda: self.set_mode("edit"))

        # 戻る
        self.back_button = QPushButton("戻る")
        self.back_button.clicked.connect(lambda: self.test())

        # 鉛筆
        self.draw_button = QPushButton("お絵描き")
        self.draw_button.clicked.connect(lambda: self.set_mode("draw"))

        # 矢印
        self.arrow_button = QPushButton("矢印挿入")
        self.arrow_button.clicked.connect(lambda: self.set_mode("arrow"))

        # テキスト
        self.text_button = QPushButton("テキスト挿入")
        self.text_button.clicked.connect(lambda: self.set_mode("text"))

        # エクスポート
        self.export_button = QPushButton("エクスポート")
        self.export_button.clicked.connect(lambda: self.export_canvas())

        # 投稿
        self.backlog_button = QPushButton("バックログ投稿")
        self.backlog_button.clicked.connect(lambda: self.test())



        self.header_layout.addWidget(self.edit_button)
        self.header_layout.addWidget(self.back_button)
        self.header_layout.addWidget(self.draw_button)
        self.header_layout.addWidget(self.arrow_button)
        self.header_layout.addWidget(self.text_button)
        self.header_layout.addWidget(self.export_button)
        self.header_layout.addWidget(self.backlog_button)

        self.main_layout.insertWidget(0, self.header_widget)

    def set_mode(self, modename):
        self.current_mode = modename
        print(self.current_mode)
        self.canvas_view.setcanvasmode(self.current_mode)










    def export_canvas(self):
        filename, _ = QFileDialog.getSaveFileName(self, "エクスポート", "", "PNG Files (*.png)")
        if filename:
            self.canvas_view.export_scene_to_image(filename)
            print(f"画像を保存しました: {filename}")



















    def update_canvas(self, image_dict, padding): #ここからした全部キャプチャ系。構成ミスってるだろ
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
        view = self.canvas_view
        scene_rect = view.scene.sceneRect()
        if not scene_rect.isNull():
            view.fitInView(scene_rect, Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_canvas_to_window()


