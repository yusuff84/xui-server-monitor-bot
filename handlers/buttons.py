# from aiogram import Router, types
# from database import is_admin, set_waiting, get_servers, delete_server
# from services.xui_api import get_server_stats
# from keyboards.inline import servers_keyboard, back_to_menu_keyboard
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#
# import asyncio
#
# router = Router()
#
# @router.callback_query()
# async def button_handler(query: types.CallbackQuery):
#     chat_id = query.message.chat.id
#     await query.answer()
#
#     if not is_admin(chat_id):
#         return await query.answer("❌ Нет доступа", show_alert=True)
#
#     if query.data == "add_server":
#         set_waiting(chat_id, 1)
#         await query.message.edit_text("Введите адреса серверов через запятую:\n<code>http://1.2.3.4:54321,http://2.2.2.2:1111</code>", parse_mode="HTML")
#
#     elif query.data == "list_servers":
#         servers = get_servers(chat_id)
#         if not servers:
#             return await query.message.edit_text("❌ Серверов нет.")
#         keyboard = servers_keyboard(servers)
#         keyboard.inline_keyboard.append([
#             InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")
#         ])
#         await query.message.edit_text(
#             "📋 <b>Ваши сервера:</b>",
#             parse_mode="HTML",
#             reply_markup=keyboard
#         )
#
#     elif query.data.startswith("del_"):
#             sid = int(query.data.split("_")[1])
#             delete_server(chat_id, sid)
#             await query.message.edit_text(
#                 "🗑 Сервер удалён.",
#                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
#
#                     [InlineKeyboardButton("🔙 Назад в меню", callback_data="main_menu")]]))
#
#     elif query.data == "main_menu":
#         await query.message.edit_text(
#             "🔧 Главное меню:",
#             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
#                 [InlineKeyboardButton(text="➕ Добавить сервер", callback_data="add_server")],
#                 [InlineKeyboardButton(text="📋 Список серверов", callback_data="list_servers")],
#                 [InlineKeyboardButton(text="📊 Статистика", callback_data="show_all_stats")],
#             ])
#         )
#
#     # elif query.data == "show_all_stats":
#     #     servers = get_servers(chat_id)
#     #     if not servers:
#     #         return await query.message.edit_text("❌ Нет добавленных серверов.")
#     #     await query.message.edit_text("⏳ Сбор статистики...")
#     #     results = [await get_server_stats(url) for _, url in servers]
#     #     await query.message.edit_text("\n".join(results), parse_mode="HTML")
#
#
#     elif query.data == "show_all_stats":
#         servers = get_servers(chat_id)
#         if not servers:
#             return await query.message.edit_text("❌ Нет добавленных серверов.")
#         await query.message.edit_text("⏳ Сбор статистики...")
#
#         tasks = [get_server_stats(url) for _, url in servers]
#         results = await asyncio.gather(*tasks)
#
#         await query.message.edit_text(
#             "\n".join(results),
#             parse_mode="HTML",
#             reply_markup=back_to_menu_keyboard()
#         )


from aiogram import Router, types
from database import is_admin, set_waiting, get_servers, delete_server
from services.xui_api import get_server_stats
from keyboards.inline import servers_keyboard, back_to_menu_keyboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import asyncio

router = Router()


@router.callback_query()
async def button_handler(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    await query.answer()

    if not is_admin(chat_id):
        return await query.answer("❌ Нет доступа", show_alert=True)

    if query.data == "add_server":
        set_waiting(chat_id, 1)
        await query.message.edit_text(
            "Введите адреса серверов через запятую:\n<code>http://1.2.3.4:54321,http://2.2.2.2:1111</code>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")]
                ]
            )
        )


    elif query.data == "list_servers":
        servers = get_servers(chat_id)
        if not servers:
            return await query.message.edit_text("❌ Серверов нет.")

        keyboard = servers_keyboard(servers)
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")
        ])

        await query.message.edit_text(
            "📋 <b>Ваши сервера:</b>",
            parse_mode="HTML",
            reply_markup=keyboard
        )

    elif query.data.startswith("del_"):
        sid = int(query.data.split("_")[1])
        delete_server(chat_id, sid)
        await query.message.edit_text(
            "🗑 Сервер удалён.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")]
                ]
            )
        )

    elif query.data == "main_menu":
        await query.message.edit_text(
            "🔧 Главное меню:",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="➕ Добавить сервер", callback_data="add_server")],
                    [InlineKeyboardButton(text="📋 Список серверов", callback_data="list_servers")],
                    [InlineKeyboardButton(text="📊 Статистика", callback_data="show_all_stats")]
                ]
            )
        )

    elif query.data == "show_all_stats":
        servers = get_servers(chat_id)
        if not servers:
            return await query.message.edit_text("❌ Нет добавленных серверов.")

        await query.message.edit_text("⏳ Сбор статистики...")
        tasks = [get_server_stats(url) for _, url in servers]
        results = await asyncio.gather(*tasks)

        await query.message.edit_text(
            "\n".join(results),
            parse_mode="HTML",
            reply_markup=back_to_menu_keyboard()
        )
