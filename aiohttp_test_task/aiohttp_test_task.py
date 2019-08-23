from aiohttp import web, ClientSession
import json

USERS_URL = 'https://api.test.brn.pw/clients/'
TARIFFS_URL = 'https://api.test.brn.pw/tariffs/'


async def get_ext_info(id, url):
    async with ClientSession() as session:
        async with session.get(url + id) as resp:
            resp_dist = await resp.json()
    return resp_dist


async def get_info(request):
    lines = {}
    async for line in request.content:
        lines = json.loads(line.decode())

    try:
        ext_user = await get_ext_info(str(lines['user_id']), USERS_URL)
        client = {
            "id": ext_user['id'],
            "name": ext_user['name'],
            "username": ext_user['username'],
            "email": ext_user['email']
        }
    except:
        client = {}

    try:
        ext_tariff = await get_ext_info(str(lines['tariff_id']), TARIFFS_URL)
        tariff = {
            "id": ext_tariff['id'],
            "name": ext_tariff['name'],
            "size": ext_tariff['size'],
            "websites": ext_tariff['websites'],
            "databases": ext_tariff['databases']
        }
    except:
        tariff = {}

    result = {
        "id": 6,
        "success": True,
        "status": "TRIAL",
        "client": client,
        "tariff": tariff,
    }

    return web.Response(text=json.dumps(result))


app = web.Application()
app.router.add_get('/', get_info, name='resp')
web.run_app(app, host='127.0.0.1', port=8080)