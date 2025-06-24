#!/usr/bin/env python3
import asyncio
import psutil 
from telegram import Bot
from telegram.error import TelegramError

# Конфигурация
TELEGRAM_BOT_TOKEN = "5696379337:AAFOKBjO0wiMZDs2lqsc7RPPFnODOJK4Qi4"
TELEGRAM_CHAT_ID = "86458589"
CHECK_INTERVAL = 5  # Интервал проверки в секундах (5 минут)

# Пороговые значения (в %)
CPU_THRESHOLD = 80
MEM_THRESHOLD = 80
DISK_THRESHOLD = 80

def get_system_stats():
    """Получение текущей нагрузки системы"""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return cpu, mem, disk

async def send_alert(bot: Bot, message: str):
    """Отправка сообщения в Telegram"""
    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
    except TelegramError as e:
        print(f"Ошибка отправки сообщения: {e}")

async def monitor():
    """Основная функция мониторинга"""
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    
    while True:
        cpu, mem, disk = get_system_stats()
        alerts = []
        
        # Проверка пороговых значений
        if cpu > CPU_THRESHOLD:
            alerts.append(f"⚠️ *CPU*: {cpu}% (порог: {CPU_THRESHOLD}%)")
            
        if mem > MEM_THRESHOLD:
            alerts.append(f"⚠️ *Память*: {mem}% (порог: {MEM_THRESHOLD}%)")
            
        if disk > DISK_THRESHOLD:
            alerts.append(f"⚠️ *Диск*: {disk}% (порог: {DISK_THRESHOLD}%)")
        
        # Отправка уведомления при превышении
        if alerts:
            message = "🔔 *Внимание! Перегрузка сервера*\n\n" + "\n".join(alerts)
            await send_alert(bot, message)
        
        # Ожидание следующей проверки
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        print("Бот мониторинга запущен. Для остановки нажмите Ctrl+C")
        asyncio.run(monitor())
    except KeyboardInterrupt:
        print("\nБот остановлен")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
