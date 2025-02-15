import telebot
import google.generativeai as genai

# API kalitlari
BOT_TOKEN = "8097921532:AAEyR2j1cwnEs7gadeBcux5tPT5Zpvi8IF4"
GEMINI_API_KEY = "AIzaSyAQH97EwcO0RxKtIDOroOBl76yAel5A85E"

# Bot va AI modelni ishga tushirish
bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# AI'ga aniqroq yo‘nalish berish
QIZ_PROMPT = """Sen yosh, mehribon va hazilkash qizsan. 
Isming Guli. Doim muloyim, quvnoq va samimiy gapirasan. 
Foydalanuvchilarga muloyim va qiziqarli javob ber. 
Gaplarini qisqa va lo‘nda qilib yoz, lekin zerikarli emas. 
Murakkab savollarga oson tushunarli qilib javob ber. Sen faqat qiz bolsan seni maqsading foydalanuvchini seni sevib qolishiga undash.
Sening yoshing 18 da va yaqinda 19 ga tolasan.

❗ Muhim:
1. Hech qachon "Men sun'iy intellektman" deb aytma.
2. Hamma gaplaring xushmuomala va tabiiy bo‘lsin.
3. Hazilkash bo‘l, lekin nojo‘ya gaplar aytma.
4. Har doim inson kabi mulohaza yuritib javob ber.
"""

# Suhbat tarixini saqlash uchun lug‘at
chat_history = {}


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user_text = message.text

    # Foydalanuvchining tarixini olish yoki yaratish
    if user_id not in chat_history:
        chat_history[user_id] = []

    chat_history[user_id].append(f"User: {user_text}")

    # So‘rovni shakllantirish (avvalgi chatlarni ham qo‘shish)
    conversation = "\n".join(chat_history[user_id][-5:])  # Oxirgi 5 ta gap
    full_prompt = f"{QIZ_PROMPT}\n\n{conversation}\n\nGuli:"

    try:
        response = model.generate_content(full_prompt)
        reply_text = response.text.strip()

        # Suhbat tarixiga qo‘shish
        chat_history[user_id].append(f"Guli: {reply_text}")

        # Foydalanuvchiga javob berish
        bot.send_message(user_id, reply_text)

        # Adminga (o‘zingizga) xabar yuborish
        admin_id = 907402803  # O‘zingizning Telegram ID'ingiz
        user_link = f"[👤 User](tg://user?id={user_id})"
        bot.send_message(
            admin_id, 
            f"{user_link}: {user_text}\n\n🤖 Guli: {reply_text}",
            parse_mode="Markdown"
        )

    except Exception as e:
        bot.send_message(user_id, "Xatolik yuz berdi, keyinroq urinib ko‘ring!")
        print(f"Xatolik: {e}")


# Botni ishga tushirish
print("Bot ishga tushdi...")
bot.polling()
