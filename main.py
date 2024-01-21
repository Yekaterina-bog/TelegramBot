import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

TELEGRAM_BOT_TOKEN = "6606111041:AAFotzKGqbCgEwAfZ1pxwTpTQBD41uCI0OY"

GOOGLE_BOOKS_API_KEY = "AIzaSyA8N0aAvz0N5kAb_vFJJBF_nCxFsmeMlow"

SEARCH_BOOK_TITLE = 1

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Привет! Я BooksUniverse бот - ваш проводник в мир книг. Введите /bookinfo для начала поиска книги, а затем название интересующей вас литературы.")
    return SEARCH_BOOK_TITLE

def book_info(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Введите название книги:")
    return SEARCH_BOOK_TITLE

def get_book_info(update: Update, context: CallbackContext) -> None:
    book_title = update.message.text
    book_info_text = get_book_info_from_api(book_title)
    update.message.reply_text(book_info_text)

def get_book_info_from_api(book_title: str) -> str:
    url = f"https://www.googleapis.com/books/v1/volumes?q={book_title}&key={GOOGLE_BOOKS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "items" in data and len(data["items"]) > 0:
        book = data["items"][0]["volumeInfo"]
        title = book.get("title", "Название не найдено")
        authors = ", ".join(book.get("authors", ["Автор не найден"]))
        description = book.get("description", "Описание не найдено")
        year = book.get("publishedDate", "Год выпуска не найден")
        genre = ", ".join(book.get("categories", ["Жанр не найден"]))
        page_count = book.get("pageCount", "Количество страниц не найдено")

        return f"Название: {title}\nАвторы: {authors}\nОписание: {description}\nГод выпуска: {year}\nЖанр: {genre}\nКоличество страниц: {page_count}"
    else:
        return "Книга не найдена."

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Поиск завершен. Был рад помочь!")
    return ConversationHandler.END

def main() -> None:
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SEARCH_BOOK_TITLE: [MessageHandler(Filters.text & ~Filters.command, get_book_info)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
