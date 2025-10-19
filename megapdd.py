from aiohttp import ClientSession
from asyncio import get_event_loop, new_event_loop, run


class Megapdd():
    def __init__(self):
        self.session = ClientSession()
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "host": "megapdd.ru",
            "user-agent": "love_linux_mint",
            'Accept-Encoding': 'deflate, zstd',
            'Accept-Language': 'ru-RU,ru;q=0.9',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="137", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'}
        self.api = "https://megapdd.ru/api"

    def __del__(self):
        try:
            loop = get_event_loop()
            loop.create_task(self._close_session())
        except RuntimeError:
            loop = new_event_loop()
            loop.run_until_complete(self._close_session())

    async def _close_session(self):
        if not self.session.closed:
            await self.session.close()

    async def exam_collections(self):
        async with self.session.get(f"{self.api}/collections", headers=self.headers) as req:
            return await req.json()

    async def exam_start(self, collection_id: int):
        async with self.session.get(f"{self.api}/collections/{collection_id}/exam", headers=self.headers) as req:
            return await req.json()

    async def ticket_details(self, collection_id: int):
        async with self.session.get(f"{self.api}/collections/{collection_id}/ticket-details", headers=self.headers) as req:
            return await req.json()

    async def get_questions(self, collection_id, ticket_id):
        async with self.session.get(f"{self.api}/collections/{collection_id}/tickets/{ticket_id}/questions", headers=self.headers) as req:
            return await req.json()


async def main():
    client = Megapdd()
    print(await client.get_questions(1, 3))
run(main())
