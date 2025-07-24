import os
import zipfile
import datetime
from telegram import Bot
import asyncio

# 👇 تنظیمات اصلی
TELEGRAM_BOT_TOKEN = '7255674500:AAHw1lN7oheFvZ3W-12MpGxkdzfbJ2pWsfM'
CHAT_ID = '-1002795263743'
FOLDER_TO_BACKUP = 'Baygani'  # باید این پوشه کنار همین فایل داخل ریپو باشه

def create_zip_archive():
    print("🔄 در حال ساخت فایل زیپ...")
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f'backup_{timestamp}.zip'

    if not os.path.exists(FOLDER_TO_BACKUP):
        print(f"❌ پوشه '{FOLDER_TO_BACKUP}' پیدا نشد. عملیات متوقف شد.")
        return None

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(FOLDER_TO_BACKUP):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, FOLDER_TO_BACKUP)
                zipf.write(file_path, arcname)
                print(f"✅ اضافه شد: {file_path}")
    print(f"📦 فایل زیپ ساخته شد: {zip_filename}")
    return zip_filename

async def send_to_telegram(zip_filename):
    if not zip_filename:
        print("⚠️ فایلی برای ارسال وجود ندارد.")
        return
    print("📤 در حال ارسال فایل به تلگرام...")
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        with open(zip_filename, 'rb') as zip_file:
            await bot.send_document(chat_id=CHAT_ID, document=zip_file, caption=f'Backup created at {datetime.datetime.now()}')
        print("✅ فایل با موفقیت ارسال شد!")
    except Exception as e:
        print(f"❌ خطا هنگام ارسال به تلگرام: {e}")
    os.remove(zip_filename)
    print("🧹 فایل زیپ موقت حذف شد.")

async def main():
    zip_filename = create_zip_archive()
    await send_to_telegram(zip_filename)

if __name__ == '__main__':
    asyncio.run(main())
