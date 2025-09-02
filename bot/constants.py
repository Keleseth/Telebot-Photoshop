BG_COLOR_CHOICES = [
        ("Без фона", "NONE"),
        ("Белый", "#ffffff"),
        ("Чёрный", "#000000"),
        ("Красный", "#ff0000"),
        ("Синий", "#007bff"),
        ("Зелёный", "#00cc66"),
    ]
ALLOWED_COLORS = [val for _, val in BG_COLOR_CHOICES]
NETIFY_PALLETE_URL = 'https://glittering-sfogliatella-0a9950.netlify.app'
LIMIT_PER_DAY = 6


# Сообщения бота - тексты кнопок
ADMIN_ZONE = '🛠 Админ-зона'
WHITELIST_BUTTON_TEXT = 'VIP список'
FIND_USER_BUTTON_TEXT = 'Найти пользователя по id'
ADD_USER_BUTTON_TEXT = 'Добавить пользователя в vip список'
REMOVE_USER_BUTTON_TEXT = 'Удалить пользователя из vip списка'
ASK_ID_TO_SEARH_BUTTON_TEXT = 'Введите Telegram ID для поиска пользователя:'
ASK_ID_TO_ADD_BUTTON_TEXT = 'Введите Telegram ID для добавления пользователя:'
ASK_ID_TO_REMOVE_BUTTON_TEXT = 'Введите Telegram ID для удаления пользователя:'
CANCEL_BUTTON = '🔄 Отмена'

# Сообщения бота - инструкция
CHOOSE_COLOR = "🎨 Откройте WebApp для выбора цвета фона."
CHOSEN_OPTION_RM_BG = 'Опция выбрана: убрать фон'
CHOOSE_OPTION = 'Выбери опциию из списка'


# Сообщения бота - тексты ошибок
NO_COLOR = 'Цвет не выбран. Повторите выбор в палитре.'
SERVER_ERROR = 'Ошибка при обработке, повторите попытку.'
INCORRECT_COLOR = 'Не удалось обработать цвет из палитры : Выберите другой цвет.'
NO_PHOTO  = 'Нет фото — пришли заново'
LIMIT_EXCEEDED = f"📛 Превышен лимит: {LIMIT_PER_DAY} фото в сутки. Попробуйте завтра."


# Redis ключи
REDIS_ADMINS_KEY = 'admins'
REDIS_WHITELIST_KEY = 'whitelist'