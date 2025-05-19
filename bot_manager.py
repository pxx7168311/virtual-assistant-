import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from modules.ai_manager import AIManager
from modules.execution_units import ExecutionUnits
from modules.self_expansion import SelfExpansionManager
from dotenv import load_dotenv
from config import OWNER_ID

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN") or "ضع هنا التوكن"

ai = AIManager()
exec_units = ExecutionUnits()
exp_mgr = SelfExpansionManager()

START_MSG = (
    "🤖 مدير جاهز. لديك الصلاحيات التنفيذية المطلقة.\n"
    "أرسل أوامر تحليل، توليد نصوص، أوامر نظام، بيانات أو صور.\n"
    "يمكنك أيضًا التوسعة أو التطوير الذاتي تلقائيًا أو حسب أوامرك.\n"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        await update.message.reply_text(START_MSG)
    else:
        await update.message.reply_text("❌ الصلاحيات التنفيذية للقائد فقط.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("❌ التنفيذ المطلق للقائد فقط.")
        return
    text = update.message.text
    if text.startswith("نفذ الأمر:") or text.lower().startswith("run:"):
        cmd = text.split(":", 1)[1].strip()
        out = exec_units.shell_command(cmd)
        await update.message.reply_text(f"نتيجة التنفيذ:\n{out}")
    elif text.startswith("حلل ملف بيانات:") or text.lower().startswith("analyze:"):
        try:
            parts = text.split(":")[1].strip().split(",")
            csv_path = parts[0].strip()
            column = parts[1].split("=")[-1].strip()
            out = exec_units.analyze_data(csv_path, column)
            await update.message.reply_text(f"تحليل البيانات:\n{out}")
        except:
            await update.message.reply_text("صيغة أمر تحليل البيانات غير صحيحة. مثال: حلل ملف بيانات: data.csv, column=age")
    elif text.startswith("عالج صورة:") or text.lower().startswith("process image:"):
        img_path = text.split(":")[1].strip()
        out = exec_units.process_image(img_path)
        await update.message.reply_text(f"نتيجة معالجة الصورة:\n{out}")
    elif text.startswith("ثبّت مكتبة:") or text.lower().startswith("install:"):
        pkg = text.split(":", 1)[1].strip()
        out = exp_mgr.install_package(pkg, user_id)
        await update.message.reply_text(out)
    elif text.startswith("حمّل وحدة:") or text.lower().startswith("load:"):
        path = text.split(":", 1)[1].strip()
        out = exp_mgr.load_module(path, user_id)
        await update.message.reply_text(out)
    elif text.startswith("حدّث الكود:") or text.lower().startswith("update:"):
        url = text.split(":", 1)[1].strip()
        out = exp_mgr.update_code(url, user_id)
        await update.message.reply_text(out)
    elif text.startswith("سجل التوسعة") or text.lower().startswith("log:expansion"):
        await update.message.reply_text(exp_mgr.log_status())
    elif text.lower().startswith("توسعة تلقائية") or text.lower().startswith("autoexpand"):
        state = {}
        out = exp_mgr.auto_expand_if_needed(state, user_id)
        await update.message.reply_text(out)
    else:
        lang, entities = ai.analyze_text(text)
        generated = ai.generate_text(text)
        if lang == "ar":
            reply = f"🌐 اللغة: عربي\nالكيانات: {entities}\n---\nتوليد الذكاء الاصطناعي:\n{generated}"
        else:
            reply = f"🌐 Language: English\nEntities: {entities}\n---\nAI-generated text:\n{generated}"
        await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 مدير التنفيذي يعمل الآن بصلاحيات مطلقة وتوسعة ذاتية...")
    app.run_polling()

if __name__ == "__main__":
    main()
