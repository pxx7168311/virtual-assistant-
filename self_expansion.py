import subprocess
import importlib
import sys
import os
from config import AUTO_EXPANSION, OWNER_ID

class SelfExpansionManager:
    def __init__(self):
        self.log_path = "expansion_log.txt"

    def log(self, message):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(message + "\n")

    def install_package(self, package: str, triggered_by: int) -> str:
        if not self._is_authorized(triggered_by):
            return "❌ الصلاحيات المطلقة للتوسعة محفوظة للقائد فقط."
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            self.log(f"تم تثبيت الحزمة: {package}")
            return f"✅ تم تثبيت الحزمة بنجاح: {package}"
        except Exception as e:
            self.log(f"❌ فشل تثبيت الحزمة: {package} | {e}")
            return f"❌ فشل تثبيت الحزمة: {package} | {e}"

    def load_module(self, module_path: str, triggered_by: int) -> str:
        if not self._is_authorized(triggered_by):
            return "❌ الصلاحيات المطلقة للتوسعة محفوظة للقائد فقط."
        try:
            module_name = os.path.splitext(os.path.basename(module_path))[0]
            if module_path not in sys.path:
                sys.path.append(os.path.dirname(module_path))
            importlib.invalidate_caches()
            importlib.import_module(module_name)
            self.log(f"تم تحميل الوحدة بنجاح: {module_path}")
            return f"✅ تم تحميل الوحدة بنجاح: {module_path}"
        except Exception as e:
            self.log(f"❌ فشل تحميل الوحدة: {module_path} | {e}")
            return f"❌ فشل تحميل الوحدة: {module_path} | {e}"

    def update_code(self, git_repo_url: str, triggered_by: int) -> str:
        if not self._is_authorized(triggered_by):
            return "❌ الصلاحيات المطلقة للتوسعة محفوظة للقائد فقط."
        try:
            out = subprocess.check_output(f"git pull {git_repo_url}", shell=True, text=True)
            self.log(f"تم تحديث الكود من: {git_repo_url} | {out}")
            return f"✅ تم تحديث النظام من المستودع:\n{out}"
        except Exception as e:
            self.log(f"❌ فشل تحديث الكود: {git_repo_url} | {e}")
            return f"❌ فشل تحديث الكود: {git_repo_url} | {e}"

    def auto_expand_if_needed(self, current_state, triggered_by: int):
        if not AUTO_EXPANSION:
            return "❕ التوسعة التلقائية غير مفعّلة."
        if not self._is_authorized(triggered_by):
            return "❌ الصلاحيات للتوسعة التلقائية محفوظة للقائد فقط."
        if "cv2" not in sys.modules:
            return self.install_package("opencv-python", triggered_by)
        return "لا حاجة للتوسعة الآن."

    def log_status(self):
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                return f.read()[-2000:]
        except FileNotFoundError:
            return "لا يوجد سجل توسعة بعد."

    def _is_authorized(self, user_id: int) -> bool:
        return user_id == OWNER_ID
