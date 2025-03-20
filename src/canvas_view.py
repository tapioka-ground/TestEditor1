from PySide6.QtWidgets import QGraphicsTextItem ,QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsPathItem ,QGraphicsRectItem
from PySide6.QtCore import Qt,QLineF, QPointF, QRectF
from PySide6.QtGui import QPixmap, QColor, QPainter,QPen,QImage, QPainterPath
import sys

from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PySide6.QtCore import QRectF
import sys

#-----------------------------------------------------------------------------------
class CanvasView(QGraphicsView):
    def __init__(self, parent=None, bg_color="#FFFFFF"):
        super().__init__(parent)

        # シーンを作成してビューにアタッチ
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # 背景色を QColor で渡す！
        self.setBackgroundBrush(QColor(bg_color))

        # アンチエイリアスやスムース描画を有効に
        self.setRenderHints(self.renderHints() | QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

                # --- お絵描きモード用 ---
        self.edit_mode = False  # 編集モードON/OFF
        self.drawing = False  # 線を描いている最中か
        self.current_path = None  # 現在の線データ
        self.current_item = None  # シーンに追加した描画オブジェクト
        self.pen_color = QColor("red")  # 線の色（自由に変えられる！）
        self.pen_width = 3  # 線の太さ




        # スクロールハンド有効に（ドラッグで動く）
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.edit_mode = False
        self.current_tool = None  # None, 'arrow', 'text'

    def clear_canvas(self):
        """シーン内をクリア"""
        self.scene.clear()

    def add_image(self, pixmap: QPixmap, position=(0, 0)):
        """画像をシーンに追加"""
        item = QGraphicsPixmapItem(pixmap)
        item.setPos(*position)
        self.scene.addItem(item)

    def add_spacer(self, width, position=(0, 0)):
        """スペーサーの代わりに透明な矩形でも追加できる"""
        # 透明な矩形は後で考えてOK。とりあえずXオフセットだけ動かせばよい
        pass

    def set_scene_rect(self, width, height):
        """シーンのサイズを設定"""
        self.scene.setSceneRect(0, 0, width, height)

    def setcanvasmode(self, mode_name):
        self.current_tool = mode_name
        print(f"モード変更: {self.current_tool}")

        is_edit = (self.current_tool == "edit")
        is_text = (self.current_tool == "text")
        for item in self.scene.items():
            # 画像アイテムはそのまま（今までの処理）
            if isinstance(item, QGraphicsPixmapItem):
                item.setFlag(QGraphicsPixmapItem.ItemIsSelectable, is_edit)
                item.setFlag(QGraphicsPixmapItem.ItemIsMovable, is_edit)

            # テキストアイテムの場合
            if isinstance(item, QGraphicsTextItem):
                # editモード → 選択/移動はOK、編集はNG
                if is_edit:
                    item.setTextInteractionFlags(Qt.NoTextInteraction)
                    item.setFlag(QGraphicsTextItem.ItemIsSelectable, True)
                    item.setFlag(QGraphicsTextItem.ItemIsMovable, True)
                # textモード → 編集OK、選択/移動OK
                elif is_text:
                    item.setTextInteractionFlags(Qt.TextEditorInteraction)
                    item.setFlag(QGraphicsTextItem.ItemIsSelectable, True)
                    item.setFlag(QGraphicsTextItem.ItemIsMovable, True)
                # それ以外 → 編集も選択も禁止（必要なら）
                else:
                    item.setTextInteractionFlags(Qt.NoTextInteraction)
                    item.setFlag(QGraphicsTextItem.ItemIsSelectable, False)
                    item.setFlag(QGraphicsTextItem.ItemIsMovable, False)

    def clear_canvas(self):
        self.scene.clear()

    def add_image(self, pixmap: QPixmap, position=(0, 0)):
        item = QGraphicsPixmapItem(pixmap)
        item.setPos(*position)
        self.scene.addItem(item)





#ここまで平和ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

    def mousePressEvent(self, event):
        scene_pos = self.mapToScene(event.pos())

        # 描画モード
        if self.current_tool == "draw" and event.button() == Qt.LeftButton:
            self.start_drawing(scene_pos)

        # テキストモード - 矩形選択開始
        elif self.current_tool == "text" and event.button() == Qt.LeftButton:
            self.text_start_point = scene_pos
            self.temp_rect_item = QGraphicsRectItem()
            pen = QPen(Qt.black, 1, Qt.DashLine)
            self.temp_rect_item.setPen(pen)
            self.scene.addItem(self.temp_rect_item)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        scene_pos = self.mapToScene(event.pos())

        # ドロー中の線
        if self.current_tool == "draw" and self.drawing:
            self.update_drawing(scene_pos)

        # テキスト範囲を選択中（ガイド枠を更新）
        elif self.current_tool == "text" and self.text_start_point:
            rect = QRectF(self.text_start_point, scene_pos).normalized()
            if self.temp_rect_item:
                self.temp_rect_item.setRect(rect)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        scene_pos = self.mapToScene(event.pos())

        # 描画終了
        if self.current_tool == "draw" and event.button() == Qt.LeftButton and self.drawing:
            self.finish_drawing()

        # テキストボックス確定
        elif self.current_tool == "text" and event.button() == Qt.LeftButton and self.text_start_point:
            self.add_text_box(self.text_start_point, scene_pos)

        super().mouseReleaseEvent(event)

    def start_drawing(self, pos):
        self.current_path = QPainterPath(pos)
        self.current_item = QGraphicsPathItem()
        pen = QPen(self.pen_color, self.pen_width)
        self.current_item.setPen(pen)
        self.scene.addItem(self.current_item)
        self.drawing = True

    def update_drawing(self, pos):
        self.current_path.lineTo(pos)
        self.current_item.setPath(self.current_path)

    def finish_drawing(self):
        self.drawing = False
        print("描画完了！")


#未完成------------------------------------
    def add_arrow(self, start_point=QPointF(100, 100), end_point=QPointF(300, 300)):#未完成です
        if self.current_tool != "arrow":
            print("矢印モードじゃない")
            return
        pen = QPen(Qt.black, 3)
        self.scene.addLine(QLineF(start_point, end_point), pen)
#未完成------------------------------------



    def add_text_box(self, start_point, end_point):
            if not self.temp_rect_item:
                return

            rect = QRectF(start_point, end_point).normalized()
            print(rect)

            # ガイド削除
            self.scene.removeItem(self.temp_rect_item)
            self.temp_rect_item = None
            self.text_start_point = None

            if rect.width() < 10 or rect.height() < 10:
                print("小さすぎるので無視！")
                return

            # テキストアイテム作成
            text_item = QGraphicsTextItem("テキストを入力")
            from PySide6.QtGui import QFont
            font = QFont("Meiryo", 40)  # フォント名とサイズ（例: メイリオ）
            font.setBold(True)
            text_item.setFont(font)
            text_item.setTextInteractionFlags(Qt.TextEditorInteraction)  # ダブルクリックで編集
            text_item.setPos(rect.topLeft())
            text_item.setTextWidth(rect.width())
            text_item.setDefaultTextColor(QColor("blue"))#フォントカラー

            text_item.setFlag(QGraphicsTextItem.ItemIsSelectable, True)
            text_item.setFlag(QGraphicsTextItem.ItemIsMovable, True)
            text_item.setFocus()  # フォーカスを与えるとカーソル(Iビーム)が出る！


            self.scene.addItem(text_item)

            print(f"テキストボックス追加: {rect}")




    def export_scene_to_image(self, filename):
        rect = self.scene.sceneRect()
        image = QImage(int(rect.width()), int(rect.height()), QImage.Format_ARGB32)
        image.fill(Qt.white)

        painter = QPainter(image)
        self.scene.render(painter)
        painter.end()

        image.save(filename)