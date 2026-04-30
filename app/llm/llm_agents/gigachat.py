from langchain_gigachat.chat_models import GigaChat
from app.core.settings import AUTH_KEY_GIGACHAT




def get_gigachat() -> GigaChat:
    """
     Возвращаем ИИ агента

    """
    return GigaChat(
        credentials=AUTH_KEY_GIGACHAT,
        verify_ssl_certs=False,
    )