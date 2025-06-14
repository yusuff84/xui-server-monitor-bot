from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить сервер", callback_data="add_server")],
        [InlineKeyboardButton(text="📋 Список серверов", callback_data="list_servers")],
        [InlineKeyboardButton(text="📈 Общая статистика", callback_data="show_all_stats")]
    ])


def servers_keyboard(servers):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🗑 Удалить {url}", callback_data=f"del_{sid}")]
        for sid, url in servers
    ])


def back_to_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")]
        ]
    )
