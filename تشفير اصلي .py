import telebot
import base64
import marshal
import zlib
import os

# حط توكن بوتك هنا
bot = telebot.TeleBot("7072174969:AAG1OZijM09vBtXAZRhApiLOQIlFANXFWJw")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 أهلاً بك في بوت تشفير @Xisjs\nارسل لي ملف .py لأشفره لك 🔐")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        file_name = message.document.file_name
        downloaded_file = bot.download_file(file_info.file_path)

        # حفظ الملف المؤقت
        with open(file_name, 'wb') as f:
            f.write(downloaded_file)

        # قراءة كود السكربت الأصلي
        with open(file_name, 'r', encoding='utf-8') as f:
            code = f.read()

        # تشفير السكربت (compile > marshal > zlib > base64)
        compiled_code = compile(code, "<memory>", "exec")
        marshaled = marshal.dumps(compiled_code)
        compressed = zlib.compress(marshaled)
        encoded = base64.b64encode(compressed).decode()

        # السكربت النهائي المشفر (يفك التشفير ويشغل من الذاكرة فقط)
        encrypted_code = f'''# — Encrypted by @Xisjs | Memory Safe
import base64, zlib, marshal

encoded = "{encoded}"
try:
    b64 = base64.b64decode(encoded)
    raw = zlib.decompress(b64)
    code = marshal.loads(raw)
    exec(code)
except Exception as e:
    print("❌ خطأ في فك التشفير:", e)
'''

        output_file = f"Xisjs_Encrypted_{file_name}"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encrypted_code)

        # إرسال الملف المشفر للمستخدم
        with open(output_file, 'rb') as f:
            bot.send_document(message.chat.id, f, caption="✅ تم التشفير بنجاح بواسطة @Xisjs")

        # حذف الملفات المؤقتة
        os.remove(file_name)
        os.remove(output_file)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ حدث خطأ أثناء التشفير:\n{e}")

bot.polling()