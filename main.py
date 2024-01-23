import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ChatActions
import openai

# Замените на ваш токен Telegram бота
TELEGRAM_TOKEN = '6787450167:AAGByC55w7mBxObi0hK7XWh29NOqgBMTqEs' # Здесь вы должны указать токен вашего Telegram бота.

# Замените на ваш API ключ от OpenAI
OPENAI_API_KEY = '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'
# Здесь вы должны указать свой API ключ от OpenAI.

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN) # Создание экземпляра бота с указанным токеном.
dp = Dispatcher(bot) # Создание диспетчера для управления обработчиками сообщений.

# Глобальный объект для хранения сессий чата
chat_sessions = {} # Словарь для хранения истории сообщений каждого пользователя.

# Функция для создания запроса
def create_prompt(user_id):
    messages = chat_sessions[user_id]['messages'] # Получение списка сообщений пользователя.
    prompt = [
        {"role": "system", "content": "Я менеджер компании, Моя главная задача помогать людям"}
    ] # Создание системного сообщения для установки контекста диалога.
    prompt.extend(messages) # Добавление всех предыдущих сообщений пользователя в запрос.
    return prompt # Возврат сформированного запроса.

# Функция обработки чата с GPT
async def handle_chat_with_gpt(user_id, message):
    if user_id not in chat_sessions:
        chat_sessions[user_id] = {'messages': []} # Если пользователя нет в сессиях, создается новая сессия.

    chat_sessions[user_id]['messages'].append({'role': 'user', 'content': message}) # Добавление сообщения пользователя в историю.

    # Имитация набора текста
    await bot.send_chat_action(user_id, ChatActions.TYPING) # Отправка действия "печатает" пользователю.

    prompt = create_prompt(user_id) # Создание запроса для модели.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        api_key=OPENAI_API_KEY,
        messages=prompt
    ) # Отправка запроса в модель ChatGPT и получение ответа.

    chat_sessions[user_id]['messages'].append(
        {'role': 'assistant', 'content': response['choices'][0]['message']['content']}) # Добавление ответа модели в историю чата.

    await bot.send_message(user_id, response['choices'][0]['message']['content']) # Отправка ответа пользователю.

# Обработчик текстовых сообщений
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text_handler(message: types.Message):
    await handle_chat_with_gpt(message.from_user.id, message.text) # Обработка текстовых сообщений от пользователя.

# Запуск бота
if __name__ == '__main__':
    openai.api_key = OPENAI_API_KEY # Установка API ключа OpenAI.
    executor.start_polling(dp, skip_updates=True) # Запуск бота для прослушивания входящих сообщений.
