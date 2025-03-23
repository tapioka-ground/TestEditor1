from src.ui_capture_window import CaptureWindow
from src.ui_editor_window import EditorWindow
from PySide6.QtWidgets import QMessageBox ,QApplication
import time


class AppManager:
    _instance = None#シングルトンにしてます
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.capture_window = None
        self.editor_window = None
        self.canvas_image_list = {}
        self.image_index = 0
        self.block_padding = 100
        self.tapcheak = True
        self.last_tap = 0
        self.tap_interval = 0.4#ここで連打感覚調整して

    def set_padding(self,input_padding):
        self.block_padding = input_padding

    def get_padding(self,):
        return self.block_padding

    def tap_checker(self,):
        current_time = time.time()
        if current_time - self.last_tap < self.tap_interval:
            print("連打防止中")
            return False

        self.last_tap = current_time
        return True


    def add_capture_image(self,screenshot):#画像追加
        if self.tap_checker() == True:
            image_id = self.image_index
            self.canvas_image_list[image_id] = screenshot
            self.image_index += 1

            self.editor_window.update_canvas(self.canvas_image_list,self.block_padding)

    def add_spacer_image(self,):
        if self.tap_checker() == True:
            image_id = self.image_index
            self.canvas_image_list[image_id] = ""
            self.image_index += 1

            self.editor_window.update_canvas(self.canvas_image_list,self.block_padding)

    def add_newline(self,):
        if self.tap_checker() == True:
            image_id = self.image_index
            self.canvas_image_list[image_id] = "new"
            self.image_index += 1

            self.editor_window.update_canvas(self.canvas_image_list,self.block_padding)

    def remove_image(self):
        if self.tap_checker() == True:
            if self.image_index == 0:
                print("削除する画像がない！")
                return
            last_image_id = self.image_index - 1

            if last_image_id in self.canvas_image_list:
                del self.canvas_image_list[last_image_id]
                print(f"image_id {last_image_id} を削除したよ！")
            self.image_index -= 1

            self.editor_window.update_canvas(self.canvas_image_list, self.block_padding)

    def delete_image(self,):
        if self.tap_checker() == True:
            if not self.cheak_message("確認","全てのキャプチャを削除しますか？"):
                return
            if self.image_index == 0:
                print("ダメです")
                return
            else:
                self.canvas_image_list = {}
                self.image_index = 0
                self.editor_window.update_canvas({0:""}, self.block_padding)
                print("削除完了")







    def capture_window_start(self):
        self.capture_window = CaptureWindow(self)
        self.capture_window.move(0, 0)
        self.capture_window.show()


    def editor_window_start(self):
        self.editor_window = EditorWindow(self)
        screen = QApplication.primaryScreen()
        screen_width = screen.size().width()

        window_width = self.editor_window.width()
        self.editor_window.move(screen_width - window_width, 0)
        self.editor_window.show()



    def cheak_message(self,title,messege):
        msg_box = QMessageBox(self.capture_window)
        msg_box.setWindowTitle(title)
        msg_box.setText(messege)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec()

        if result == QMessageBox.Yes:
            print("はい")
            return True
        else:
            print("いいえ")
            return False

    def start_app(self):
        self.capture_window_start()
        self.editor_window_start()
