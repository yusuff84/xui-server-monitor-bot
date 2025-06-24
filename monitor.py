import asyncio
import html

# import logging
from urllib.parse import urlparse

# настрой логгирование (глобально, можно один раз в начале файла)
# logging.basicConfig(level=logging.INFO)


# async def monitor_servers(bot):
#     await asyncio.sleep(10)
#
#     while True:
#         try:
#             import sqlite3
#             from database import get_servers
#             from services.xui_api import get_server_stats_raw
#
#             with sqlite3.connect("servers.db") as conn:
#                 cur = conn.execute("SELECT DISTINCT chat_id FROM servers")
#                 chat_ids = [row[0] for row in cur.fetchall()]
#
#             for chat_id in chat_ids:
#                 servers = get_servers(chat_id)
#                 for _, url in servers:
#                     try:
#                         stats = await get_server_stats_raw(url)
#
#                         alert_reasons = []
#                         if stats["online"] < 10:
#                             alert_reasons.append("🟥 Онлайн < 10")
#                         if stats["expired"] > 10:
#                             alert_reasons.append("🟨 Истекших ключей > 10")
#
#                         if alert_reasons:
#                             parsed_url = urlparse(url)
#                             short_name = parsed_url.hostname  # даст 'nl-1.thetopvpn.ru'
#
#                             text = (
#                                     f"⚠️ Проблемы на сервере: <b>{html.escape(short_name)}</b>\n"
#                                     f"📊 Статистика:\n"
#                                     f"👥 Всего: <b>{stats['total']}</b>\n"
#                                     f"🟢 Онлайн: <b>{stats['online']}</b>\n"
#                                     f"⌛ Истекло: <b>{stats['expired']}</b>\n"
#                                     f"\nПричины:\n" + "\n".join([html.escape(reason) for reason in alert_reasons])
#                             )
#                             await bot.send_message(chat_id, text, parse_mode="HTML")
#
#                     except Exception as e:
#                         safe_url = html.escape(url)
#                         safe_error = html.escape(str(e))
#                         # logging.error(f"[monitor error] URL: {url} | Exception: {e}")
#                         await bot.send_message(
#                             chat_id,
#                             f"🚫 <b>{safe_url}</b>\nОшибка: <code>{safe_error}</code>",
#                             parse_mode="HTML"
#                         )
#
#         except Exception as err:
#             print(f"[monitor error] {err}")
#
#         await asyncio.sleep(600)  # каждые 10 минут


async def monitor_servers(bot):
    failed_once = {}  # Сбрасывается каждый раз при новом запуске monitor_servers
    await asyncio.sleep(10)

    while True:
        try:
            import sqlite3
            from database import get_servers
            from services.xui_api import get_server_stats_raw

            with sqlite3.connect("servers.db") as conn:
                cur = conn.execute("SELECT DISTINCT chat_id FROM servers")
                chat_ids = [row[0] for row in cur.fetchall()]

            for chat_id in chat_ids:
                servers = get_servers(chat_id)
                for _, url in servers:
                    key = (chat_id, url)

                    try:
                        stats = await get_server_stats_raw(url)

                        # Очистить флаг ошибки, если все успешно
                        if key in failed_once:
                            del failed_once[key]

                        alert_reasons = []
                        if stats["online"] < 10:
                            alert_reasons.append("🟥 Онлайн < 10")
                        if stats["expired"] > 10:
                            alert_reasons.append("🟨 Истекших ключей > 10")

                        if alert_reasons:
                            from urllib.parse import urlparse
                            short_name = urlparse(url).hostname
                            text = (
                                f"⚠️ Проблемы на сервере: <b>{html.escape(short_name)}</b>\n"
                                f"📊 Статистика:\n"
                                f"👥 Всего: <b>{stats['total']}</b>\n"
                                f"🟢 Онлайн: <b>{stats['online']}</b>\n"
                                f"⌛ Истекло: <b>{stats['expired']}</b>\n"
                                f"\nПричины:\n" + "\n".join([html.escape(r) for r in alert_reasons])
                            )
                            await bot.send_message(chat_id, text, parse_mode="HTML")

                    except Exception as e:
                        if key not in failed_once:
                            failed_once[key] = asyncio.create_task(
                                schedule_retry(bot, chat_id, url, e)
                            )

        except Exception as err:
            print(f"[monitor error] {err}")

        await asyncio.sleep(600)
