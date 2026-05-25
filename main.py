import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import aiogram.types as am

# Твой рабочий токен
TOKEN = "8915256349:AAHWC5jN4e6wEtHIYAQBnquLLfubgg52BHo"

bot = Bot(token=TOKEN)
dp = Dispatcher()

PHOTO_MAIN = "https://cdn.phototourl.com/free/2026-05-24-19c12646-ee43-4ef9-8b7f-ee4898def442.jpg"
PHOTO_STARS = "https://cdn.phototourl.com/free/2026-05-24-d76c777f-f309-49fc-ae7f-f320a8039c78.jpg"
PHOTO_PREMIUM = "https://cdn.phototourl.com/free/2026-05-24-d76c777f-f309-49fc-ae7f-f320a8039c78.jpg"

CARD_NUMBER = "5375 4115 9128 3481"
TON_WALLET = "UQA-T10RmY8GJGMlE4CBIgttdSYGaPO3rLPw3uelUAp7fZ-O"

ANTI_SCAM_TEXT = (
    "🛡️ *Почему нам можно доверять?*\n"
    "Мы используем одну и ту же постоянную карту. Она полностью личная, а не арендованный дроп. "
    "Нам важна наша репутация и долгосрочная работа, а скрывать нам нечего!"
)

# Словарь для автоматического определения цен при выводе реквизитов
PRICES_DICT = {
    "50": "40 грн", "75": "60 грн", "100": "79 грн", "150": "119 грн",
    "250": "198 грн", "350": "278 грн", "500": "397 грн", "750": "595 грн", "1000": "794 грн",
    "1y": "1385 грн", "6m": "765 грн", "3m": "575 грн"
}

# --- Клавиатуры ---

def get_main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ Купить Звезды", callback_data="buy_stars")],
        [InlineKeyboardButton(text="💎 Купить Премиум", callback_data="buy_premium")],
        [InlineKeyboardButton(text="🎮 Арендовать игры (Steam)", callback_data="rent_games")],
        [InlineKeyboardButton(text="👨‍💻 Поддержка", callback_data="support")]
    ])

def get_stars_prices_kb():
    prices = [
        ("50 ⭐ — 40 грн", "stars_50"), ("75 ⭐ — 60 грн", "stars_75"),
        ("100 ⭐ — 79 грн", "stars_100"), ("150 ⭐ — 119 грн", "stars_150"),
        ("250 ⭐ — 198 грн", "stars_250"), ("350 ⭐ — 278 грн", "stars_350"),
        ("500 ⭐ — 397 грн", "stars_500"), ("750 ⭐ — 595 грн", "stars_750"),
        ("1000 ⭐ — 794 грн", "stars_1000")
    ]
    keyboard = []
    for i in range(0, len(prices), 2):
        row = [InlineKeyboardButton(text=prices[i][0], callback_data=prices[i][1])]
        if i + 1 < len(prices):
            row.append(InlineKeyboardButton(text=prices[i+1][0], callback_data=prices[i+1][1]))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="to_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_premium_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚡ 1 год — 1385 грн ⚡", callback_data="prem_1y")],
        [InlineKeyboardButton(text="⚡ 6 месяцев — 765 грн ⚡", callback_data="prem_6m")],
        [InlineKeyboardButton(text="⚡ 3 месяца — 575 грн ⚡", callback_data="prem_3m")],
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="to_main")]
    ])

def get_payment_method_kb(stars_count):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Украинская карта", callback_data=f"pay_card_{stars_count}")],
        [InlineKeyboardButton(text="🤖 CryptoBot (TON)", callback_data=f"pay_crypto_{stars_count}")],
        [InlineKeyboardButton(text="⬅️ Назад к выбору звёзд", callback_data="buy_stars")]
    ])

def get_confirm_payment_kb(back_target="buy_stars"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Я оплатил(а)", callback_data="payment_done")],
        [InlineKeyboardButton(text="⬅️ Отмена и назад", callback_data=back_target)]
    ])

def get_back_to_main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="to_main")]
    ])

# --- Хэндлеры ---

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    welcome_text = (
        "👋 *Приветствуем в нашем магазине цифровых товаров!*\n\n"
        "⚡ Выбирай интересующий раздел ниже 👇"
    )
    await message.answer_photo(
        photo=PHOTO_MAIN,
        caption=welcome_text,
        reply_markup=get_main_kb(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_media(
        media=am.InputMediaPhoto(media=PHOTO_MAIN, caption="👋 *Приветствуем!*\n⚡ Выбирай раздел:", parse_mode="Markdown"),
        reply_markup=get_main_kb()
    )
    await callback.answer()

@dp.callback_query(F.data == "buy_stars")
async def section_stars(callback: CallbackQuery):
    text = "🌟 *Покупка Telegram Stars*\n\nВыбери пакет:"
    await callback.message.edit_media(
        media=am.InputMediaPhoto(media=PHOTO_STARS, caption=text, parse_mode="Markdown"),
        reply_markup=get_stars_prices_kb()
    )
    await callback.answer()

@dp.callback_query(F.data == "buy_premium")
async def section_premium(callback: CallbackQuery):
    text = "💎 *Покупка Telegram Premium*\n\nВыбери период подписки:"
    await callback.message.edit_media(
        media=am.InputMediaPhoto(media=PHOTO_PREMIUM, caption=text, parse_mode="Markdown"),
        reply_markup=get_premium_kb()
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("stars_"))
async def choose_payment_method(callback: CallbackQuery):
    stars_count = callback.data.split("_")[1]
    text = f"💳 *Вы выбрали:* {stars_count} ⭐\nВыбери способ оплаты:"
    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_payment_method_kb(stars_count),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("prem_"))
async def choose_premium_payment_method(callback: CallbackQuery):
    period = callback.data.split("_")[1]
    
    # Красивое отображение выбранного периода
    period_labels = {"1y": "1 год", "6m": "6 месяцев", "3m": "3 месяца"}
    display_period = period_labels.get(period, period)
    
    text = f"💎 *Вы выбрали Premium:* {display_period}\nВыбери способ оплаты:"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Украинская карта", callback_data=f"pay_card_{period}")],
        [InlineKeyboardButton(text="🤖 CryptoBot (TON)", callback_data=f"pay_crypto_{period}")],
        [InlineKeyboardButton(text="⬅️ Назад к выбору подписки", callback_data="buy_premium")]
    ])
    
    await callback.message.edit_caption(
        caption=text,
        reply_markup=kb,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data.in_(["rent_games", "support"]))
async def other_sections(callback: CallbackQuery):
    text = "⚠️ *Раздел временно недоступен.*" if callback.data != "support" else "👨‍💻 *Поддержка: @Ratnikstarsbot*"
    await callback.message.edit_caption(caption=text, reply_markup=get_back_to_main_kb(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data.startswith("pay_"))
async def pay_action(callback: CallbackQuery):
    parts = callback.data.split("_")
    pay_method = parts[1]  # card или crypto
    item_id = parts[2]     # например, 50 (звезды) или 1y (премиум)
    
    # Определяем, что покупают для красивого текста
    if item_id in ["1y", "6m", "3m"]:
        period_names = {"1y": "на 1 год", "6m": "на 6 месяцев", "3m": "на 3 месяца"}
        label = f"Telegram Premium {period_names.get(item_id)}"
        back_target = "buy_premium"
    else:
        label = f"{item_id} ⭐"
        back_target = "buy_stars"
        
    price = PRICES_DICT.get(item_id, "По запросу")
    
    if pay_method == "card":
        text = (
            f"🛒 *Оплата товара: {label}*\n"
            f"💰 *Сумма к оплате:* `{price}`\n\n"
            f"📌 Переведи указанную сумму на карту:\n`{CARD_NUMBER}`\n\n"
            f"{ANTI_SCAM_TEXT}"
        )
    else:
        text = (
            f"🛒 *Оплата товара: {label}*\n"
            f"💰 *Сумма к оплате:* `{price}`\n\n"
            f"🤖 *Инструкция для оплаты через CryptoBot (TON):*\n"
            f"1. Вбей в поиске Google актуальный курс: `TON к UAH` или используй калькулятор валют.\n"
            f"2. Посчитайте, сколько TON составляет сумма `{price}` по текущему курсу.\n"
            f"3. Отправь полученное количество TON на наш кошелек:\n`{TON_WALLET}`\n\n"
            f"{ANTI_SCAM_TEXT}"
        )
        
    await callback.message.edit_caption(caption=text, reply_markup=get_confirm_payment_kb(back_target), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "payment_done")
async def payment_confirmation(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption="📥 *Заявка отправлена!*\nПришли скриншот оплаты.",
        reply_markup=get_back_to_main_kb(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.message(F.photo | F.document)
async def handle_receipt(message: Message):
    await message.reply("⏳ *Чек принят на проверку!*", parse_mode="Markdown")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))
