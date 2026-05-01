from langchain_gigachat.chat_models import GigaChat

from app.core.settings import settings


def get_gigachat() -> GigaChat:
    """
    Возвращаем ИИ агента

    """
    return GigaChat(
        credentials=settings.AUTH_KEY_GIGACHAT,
        verify_ssl_certs=False,
    )
