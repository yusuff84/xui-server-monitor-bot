from aiogram import Router, types
from database import is_admin, is_waiting, set_waiting, save_server

router = Router()

@router.message()
async def text_handler(msg: types.Message):
    chat_id = msg.chat.id
    if not is_admin(chat_id): return
    if is_waiting(chat_id):
        set_waiting(chat_id, 0)
        urls = [u.strip() for u in msg.text.strip().split(",") if u.strip().startswith("http")]
        if not urls:
            return await msg.answer("❌ Не найдено корректных URL.")
        for url in urls:
            save_server(chat_id, url)
        await msg.answer(f"✅ Добавлено серверов: {len(urls)}")