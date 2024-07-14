from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aiosmtplib import SMTP
import asyncio
from telethon import TelegramClient, events
import logging

# Настройки Telegram
api_id = ''
api_hash = ''
bot_token = ''
channel_username = ''

# Настройки email
email_from = ''
email_to = ''
email_to2 = ''
email_password = ''
smtp_server = 'smtp.yandex.ru'
smtp_port = 465

# Создание клиента Telegram
logging.basicConfig(level=logging.INFO)
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def send_email(subject, body):
    message = MIMEMultipart()
    message['From'] = email_from
    message['To'] = email_to
    message['Subject'] = subject
    message.attach(MIMEText(f"<html><body>{body}</body></html>", "html", "utf-8"))

    smtp_client = SMTP(hostname=smtp_server, port=smtp_port, use_tls=True)
    async with smtp_client:
        print("smtp login, please wait...")
        await smtp_client.login(email_from, email_password)
        await smtp_client.send_message(message)
        await smtp_client.send_message(message2)
        print("message sent")
        await smtp_client.quit()
        print("connection closed")

@client.on(events.NewMessage(chats=channel_username))
async def handle_new_message(event):
    message = event.message.message
    print(f"new message in channel: {message}")
    try:
        await send_email('New Message from Channel', message)
    except Exception as e:
        print(f"failed to send email: {e}")

async def main():
    try:
        await client.start()
        print("bot has started. listening for new messages in the channel...")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()