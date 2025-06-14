from aiogram import Router, types
from database import is_admin, add_admin
from keyboards.inline import main_menu
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start(msg: types.Message):
    if not is_admin(msg.chat.id):
        return await msg.answer("❌ У вас нет доступа.")
    await msg.answer("🛠 <b>Управление серверами:</b>", parse_mode="HTML", reply_markup=main_menu())


@router.message(Command("addadmin"))
async def addadmin(msg: types.Message):
    if not is_admin(msg.chat.id):
        return await msg.answer("❌ Нет прав.")
    try:
        uid = int(msg.text.split()[1])
        add_admin(uid)
        await msg.answer(f"✅ Админ добавлен: {uid}")
    except:
        await msg.answer("❌ Использование: /addadmin <ID>")
