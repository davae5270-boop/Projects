#!/usr/bin/env python3
# BOT TELEGRAM DAVAOFC - MINIMAL VERSION

import telebot
import sqlite3
import time
import threading

BOT_TOKEN = "8699257728:AAHYiE8d5iG75qfXN7xMtv2k3AFWhAQPzco"
OWNER_ID = 8737366854

bot = telebot.TeleBot(BOT_TOKEN)

# ===================== START =====================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or 'Tidak ada'
    full_name = message.from_user.first_name or 'User'
    
    welcome_text = f"""
🚀 *SELAMAT DATANG DI DAVAOFC!* 🚀

👤 Nama: {full_name}
🆔 ID: {user_id}
📝 Username: @{username}

━━━━━━━━━━━━━━━━━━━━
📌 *Fitur Tersedia:*
✅ Convert Crypto ke IDR
✅ Deposit & Withdraw
✅ Slot Games (Classic, Astronot, Gaple)
✅ Arisan
✅ Investasi
✅ Referral

━━━━━━━━━━━━━━━━━━━━
💡 *Cara Mulai:*
1. Buka web: http://localhost:5700
2. Login pake ID Telegram ini
3. Mulai transaksi!

👑 Owner: @davaofc4
"""
    
    bot.reply_to(message, welcome_text, parse_mode='Markdown')
    
    # Notifikasi ke owner
    bot.send_message(
        OWNER_ID,
        f"📝 *USER BARU START BOT!*\n\n"
        f"👤 @{username} ({full_name})\n"
        f"🆔 ID: {user_id}"
    )

# ===================== ID =====================
@bot.message_handler(commands=['id'])
def get_id(message):
    bot.reply_to(
        message,
        f"🆔 *ID Anda:* `{message.from_user.id}`\n"
        f"📝 Username: @{message.from_user.username or 'Tidak ada'}",
        parse_mode='Markdown'
    )

# ===================== PING =====================
@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "🏓 *Pong!* Bot aktif!", parse_mode='Markdown')

# ===================== OWNER ONLY =====================
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Hanya owner!", parse_mode='Markdown')
        return
    
    text = message.text.replace('/broadcast', '').strip()
    if not text:
        bot.reply_to(message, "❌ Kirim pesan setelah /broadcast", parse_mode='Markdown')
        return
    
    # Ambil semua user dari database
    conn = sqlite3.connect('exchange_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT telegram_id FROM users')
    users = cursor.fetchall()
    conn.close()
    
    success = 0
    for user in users:
        try:
            bot.send_message(user[0], f"📢 *BROADCAST*\n\n{text}", parse_mode='Markdown')
            success += 1
            time.sleep(0.1)
        except:
            pass
    
    bot.reply_to(message, f"✅ Broadcast terkirim ke {success} user!", parse_mode='Markdown')

# ===================== RUN =====================
if __name__ == '__main__':
    print("🤖 BOT TELEGRAM DAVAOFC STARTED!")
    print(f"📱 Bot: @Newotpdava2bot")
    print(f"👤 Owner ID: {OWNER_ID}")
    print("=" * 40)
    
    # Polling dengan auto-restart
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=30)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("🔄 Restart dalam 5 detik...")
            time.sleep(5)
