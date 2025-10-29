import aiohttp
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

API_URL = "http://host.docker.internal:8000/products"
BOT_TOKEN = "8269018717:AAFET4JgFzjAz099wk20agw5JfF69tVNNZw"



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для управления товарами.\n"
        "Команды:\n"
        "/list - список товаров\n"
        "/add - добавить товар\n"
        "/update - обновить товар\n"
        "/delete - удалить товар"
    )

async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as r:
            if r.status == 200:
                products = await r.json()
                if not products:
                    await update.message.reply_text("Список пуст.")
                    return
                text = "\n".join([f"ID: {p['id']}, Название: {p['name']}, Цена: {p['price']}" for p in products])
                await update.message.reply_text(text)
            else:
                await update.message.reply_text("Ошибка получения списка.")

async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите данные через запятую: имя, цена")
    context.user_data["action"] = "add"

async def update_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите данные через запятую: id, имя, цена")
    context.user_data["action"] = "update"

async def delete_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите ID товара для удаления")
    context.user_data["action"] = "delete"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    action = context.user_data.get("action")
    if not action:
        await update.message.reply_text("Используйте одну из команд: /list /add /update /delete")
        return

    text = update.message.text.strip()
    async with aiohttp.ClientSession() as session:
        if action == "add":
            try:
                name, price = map(str.strip, text.split(","))
                price = float(price)
                async with session.post(API_URL, json={"name": name, "price": price}) as r:
                    if r.status in (200, 201):
                        await update.message.reply_text("Товар добавлен.")
                    else:
                        await update.message.reply_text("Ошибка добавления.")
            except:
                await update.message.reply_text("Неверный формат. Пример: Товар, 123.45")
        elif action == "update":
            try:
                id_, name, price = map(str.strip, text.split(","))
                async with session.put(f"{API_URL}/{id_}", json={"name": name, "price": float(price)}) as r:
                    if r.status == 200:
                        await update.message.reply_text("Товар обновлен.")
                    else:
                        await update.message.reply_text("Ошибка обновления.")
            except:
                await update.message.reply_text("Неверный формат. Пример: 1, Товар, 123.45")
        elif action == "delete":
            try:
                id_ = text
                async with session.delete(f"{API_URL}/{id_}") as r:
                    if r.status == 200:
                        await update.message.reply_text("Товар удален.")
                    else:
                        await update.message.reply_text("Ошибка удаления.")
            except:
                await update.message.reply_text("Неверный ID.")
    context.user_data["action"] = None

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_products))
    app.add_handler(CommandHandler("add", add_product))
    app.add_handler(CommandHandler("update", update_product))
    app.add_handler(CommandHandler("delete", delete_product))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
