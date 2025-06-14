# from datetime import datetime, timezone
# from py3xui import AsyncApi
# from config import USERNAME, PASSWORD
# import httpx
#
#
# async def get_server_stats(url: str) -> str:
#     try:
#         api = AsyncApi(url, USERNAME, PASSWORD)
#         await api.login()
#
#         inbounds = await api.inbound.get_list()
#         inbound = next((i for i in inbounds if i.id == 1), None)
#         if not inbound:
#             return f"❌ <b>{url}</b>\nInbound ID=1 не найден"
#
#         clients = inbound.settings.clients or []
#         online_clients = await api.client.online()
#         now_ts = datetime.now(timezone.utc).timestamp()
#         max_reasonable_ts = datetime(2100, 1, 1, tzinfo=timezone.utc).timestamp()
#
#         expired_count = 0
#         logs = []
#
#         for i, client in enumerate(clients):  # проверяем всех
#             data = client.dict()
#             email = data.get("email", "no-email")
#             expiry = data.get("expiry_time", 0)
#
#             try:
#                 expiry_ts = int(expiry) / 1000
#                 readable = datetime.fromtimestamp(expiry_ts, tz=timezone.utc).isoformat()
#                 now_str = datetime.fromtimestamp(now_ts, tz=timezone.utc).isoformat()
#
#                 log = f"Клиент {i + 1}: {email} | expiry: {expiry} → {readable} | now: {now_str}"
#
#                 if expiry_ts == 0:
#                     logs.append(log + " → 🟢 бессрочный")
#                     continue
#                 if expiry_ts > max_reasonable_ts:
#                     logs.append(log + " → 🛑 слишком далеко")
#                     continue
#                 if expiry_ts < now_ts:
#                     expired_count += 1
#                     logs.append(log + " → ⌛ истёк")
#                 else:
#                     logs.append(log + " → ✅ активен")
#             except Exception as e:
#                 logs.append(f"Клиент {i + 1}: {email} | Ошибка: {e}")
#
#         print(f"\n=== СЕРВЕР: {url} ===")
#         print(f"Всего клиентов: {len(clients)} | Онлайн: {len(online_clients)} | Истёкших: {expired_count}")
#         for l in logs:
#             print(l)
#
#         res = f"📡 <b>{url}</b>\n"
#         res += f"👥 Всего: <b>{len(clients)}</b> | 🟢 Онлайн: <b>{len(online_clients)}</b> | ⌛ Истекло: <b>{expired_count}</b>\n\n"
#         return res
#
#     except httpx.ReadTimeout:
#         return f"⚠️ <b>{url}</b>\nОшибка: ⏱ Сервер не ответил вовремя (таймаут)"
#     except Exception as e:
#         return f"⚠️ <b>{url}</b>\nОшибка: {e}"


from datetime import datetime, timezone
from py3xui import AsyncApi
from config import USERNAME, PASSWORD
import httpx


async def get_server_stats(url: str) -> str:
    try:
        api = AsyncApi(url, USERNAME, PASSWORD)
        await api.login()

        inbounds = await api.inbound.get_list()
        inbound = next((i for i in inbounds if i.id == 1), None)
        if not inbound:
            return f"❌ <b>{url}</b>\nInbound ID=1 не найден"

        clients = inbound.settings.clients or []
        online_clients = await api.client.online()
        now_ts = datetime.now(timezone.utc).timestamp()
        max_ts = datetime(2100, 1, 1, tzinfo=timezone.utc).timestamp()

        expired_count = 0

        for client in clients:
            expiry = client.expiry_time or 0
            try:
                expiry_ts = int(expiry) / 1000
                if expiry_ts == 0 or expiry_ts > max_ts:
                    continue
                if expiry_ts < now_ts:
                    expired_count += 1
            except:
                continue

        res = f"📡 <b>{url}</b>\n"
        res += f"👥 Всего: <b>{len(clients)}</b> | 🟢 Онлайн: <b>{len(online_clients)}</b> | ⌛ Истекло: <b>{expired_count}</b>\n\n"
        return res

    except httpx.ReadTimeout:
        return f"⚠️ <b>{url}</b>\nОшибка: ⏱ Сервер не ответил вовремя (таймаут)"
    except Exception as e:
        return f"⚠️ <b>{url}</b>\nОшибка: {e}"


async def get_server_stats_raw(url: str) -> dict:
    try:
        api = AsyncApi(url, USERNAME, PASSWORD)
        await api.login()

        inbounds = await api.inbound.get_list()
        inbound = next((i for i in inbounds if i.id == 1), None)
        if not inbound:
            raise Exception("Inbound ID=1 не найден")

        clients = inbound.settings.clients or []
        online_clients = await api.client.online()
        now_ts = datetime.now(timezone.utc).timestamp()
        max_ts = datetime(2100, 1, 1, tzinfo=timezone.utc).timestamp()

        expired_count = 0
        for client in clients:
            expiry = getattr(client, "expiry_time", 0) or 0
            try:
                expiry_ts = int(expiry) / 1000
                if 0 < expiry_ts < now_ts < max_ts:
                    expired_count += 1
            except:
                continue

        return {
            "url": url,
            "total": len(clients),
            "online": len(online_clients),
            "expired": expired_count
        }

    except httpx.ReadTimeout:
        raise Exception("⏱ Сервер не ответил вовремя (таймаут)")
    except Exception as e:
        raise e
