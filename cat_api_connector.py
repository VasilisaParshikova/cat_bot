from aiohttp import ClientSession
from aiogram.types import BufferedInputFile


class CatConnector:
    __instance = None
    __basic_url = "https://cataas.com/cat/"
    __image_url = 'cat'
    __gif_url = 'gif'

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(CatConnector, cls).__new__(cls)
        return CatConnector.__instance

    async def get_image(self):
        async with ClientSession() as session:
            response = await session.get(self.__basic_url + self.__image_url)
            if response.status != 200:
                return False
            else:
                content = await response.read()
                file = BufferedInputFile(content, filename='image.jpg')
                return file

    async def get_gif(self):
        async with ClientSession() as session:
            response = await session.get(self.__basic_url + self.__gif_url)
            if response.status != 200:
                return False
            else:
                content = await response.read()
                file = BufferedInputFile(content, filename='image.gif')
                return file


cat_connector = CatConnector()
