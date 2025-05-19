import subprocess
import pandas as pd
import cv2

class ExecutionUnits:
    def shell_command(self, command: str) -> str:
        try:
            output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT, timeout=30)
            return output[:2000]
        except subprocess.CalledProcessError as e:
            return f"❌ خطأ في التنفيذ:\n{e.output}"
        except Exception as e:
            return f"❌ استثناء أثناء التنفيذ: {str(e)}"

    def analyze_data(self, csv_path: str, column: str) -> str:
        try:
            df = pd.read_csv(csv_path)
            desc = df[column].describe()
            return str(desc)
        except Exception as e:
            return f"خطأ في تحليل البيانات: {e}"

    def process_image(self, image_path: str) -> str:
        try:
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            mean_intensity = gray.mean()
            return f"متوسط شدة الإضاءة للصورة: {mean_intensity:.2f}"
        except Exception as e:
            return f"خطأ في معالجة الصورة: {e}"
