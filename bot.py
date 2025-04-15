import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import schedule
import time
import threading

# 設定日誌
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 定義 /start 指令的處理函式
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("你好，我是你的 Telegram Bot！")

# 定時發送訊息
async def send_scheduled_message(application):
    chat_id = '你的聊天 ID'  # ← 等等請填上你自己的 Telegram chat_id
    await application.bot.send_message(chat_id=chat_id, text="這是定時發送的訊息。")

# 執行排程任務
def run_schedule(application):
    schedule.every().day.at("08:30").do(lambda: application.create_task(send_scheduled_message(application)))
    schedule.every().day.at("09:30").do(lambda: application.create_task(send_scheduled_message(application)))
    schedule.every().day.at("10:30").do(lambda: application.create_task(send_scheduled_message(application)))
    schedule.every().day.at("11:30").do(lambda: application.create_task(send_scheduled_message(application)))
    while True:
        schedule.run_pending()
        time.sleep(1)

# 主程式啟動點
if __name__ == '__main__':
    application = ApplicationBuilder().token("你的 Bot Token").build()  # ← 請填入你自己的 Token
    application.add_handler(CommandHandler("start", start))

    threading.Thread(target=run_schedule, args=(application,), daemon=True).start()
    application.run_polling()