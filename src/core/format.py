import telegramify_markdown # ubah markdown dari gemini jadi markdown yg dikenali telegram

def to_telegram_markdown(text: str) -> str:
    """
    Ubah markdown standar (output dari LLM) menjadi Telegram MarkdownV2 yang valid
    """
    return telegramify_markdown.convert(text)
