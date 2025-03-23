import subprocess
import io
import time
from PIL import Image
from PySide6.QtCore import QObject, Signal, Slot

class Capture_Thread(QObject):
    image_ready = Signal(Image.Image)
    device_name_set = Signal(str)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.device_name = ""


        self._running = False
        self.database_root = ""
        self.db_name = ""




#-----------------------------------一旦保留
    @Slot()
    def get_database(self):
        """ADBから指定ディレクトリの中身を全部抜き取る"""
        print("▶ DB取得開始！")

        package_name = "com.example.app"  # パッケージ名（外からも渡せるようにするとなお良し）
        app_root = self.database_root      # 例: "com.example.app/databases"
        tmp_remote_tar = f"/sdcard/db_backup.tar"
        local_save_dir = "./backup"
        local_tar_path = f"{local_save_dir}/db_backup.tar"

        try:
            # ディレクトリをtarで固める
            # -C でchdir（作業ディレクトリ変更）、その下のフォルダ名を指定（相対パスになる）
            cmd = f"run-as {package_name} tar -cf {tmp_remote_tar} -C /data/data/{package_name} {app_root.split('/')[-1]}"
            print(f"adb shell {cmd}")
            subprocess.run(["adb", "shell", cmd], check=True)

            # pullしてPCに持ってくる
            print(f"adb pull {tmp_remote_tar} {local_tar_path}")
            subprocess.run(["adb", "pull", tmp_remote_tar, local_tar_path], check=True)

            # sdcardから削除
            print(f"adb shell rm {tmp_remote_tar}")
            subprocess.run(["adb", "shell", "rm", tmp_remote_tar], check=True)

            print(f"✅ DBディレクトリ取得完了！: {local_tar_path}")

            # オプション：ローカルで解凍（tarfile使うと便利）
            import tarfile, os
            with tarfile.open(local_tar_path) as tar:
                extract_path = os.path.join(local_save_dir, "extracted")
                os.makedirs(extract_path, exist_ok=True)
                tar.extractall(path=extract_path)
            print(f"✅ 解凍完了！ → {extract_path}")

        except subprocess.CalledProcessError as e:
            print("ADBエラー:", e)
            self.error.emit(str(e))


#-----------------------------------一旦保留








    def start_loop(self):
        self.get_device()
        self._running = True
        self.loop()


    def stop_loop(self):
        self._running = False

    def loop(self):
        print("ループ開始する")
        while self._running:
            try:
                result = subprocess.run(
                    ["adb", "exec-out", "screencap", "-p"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5
                )

                if result.returncode != 0:
                    error_msg = result.stderr.decode()
                    print("ADBコマンドしっぱい", error_msg)
                    self.error.emit(error_msg)
                    continue

                image_data = result.stdout
                pil_image = Image.open(io.BytesIO(image_data))
                self.image_ready.emit(pil_image)

                time.sleep(1/30)

            except Exception as e:
                print("スクリーンしっぱい", e)
                self.error.emit(str(e))
                time.sleep(1)
                self.get_device()

    def get_device(self):#デバイス名取得
        try:
            result = subprocess.run(
                ["adb", "shell", "getprop", "ro.product.model"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )
            self.device_name = result.stdout.decode().strip()
            self.device_name_set.emit(self.device_name)


        except Exception as e:
            print(e)
            self.device_name = ""
            self.device_name_set.emit(self.device_name)

