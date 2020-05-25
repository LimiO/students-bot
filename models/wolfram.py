from typing import Optional, Union
import asyncio
import sys
import os

from peewee import Model, CharField, IntegerField, PrimaryKeyField
from PIL import Image
import aiohttp

from utils import Limiter
from misc import db


class Wolfram(Model, Limiter):
    id = PrimaryKeyField()
    app_id = CharField(max_length=20)
    limit = IntegerField(default=2000)

    async def check_request(self, query: Optional[str],
                            background: Optional[str] = "000000",
                            foreground: Optional[str] = "white",
                            fontsize: Optional[str] = "14",
                            width: Union[str] = "500") -> bool:
        url = 'http://api.wolframalpha.com/v1/simple'
        data = {
            'appid': self.app_id,
            'i': query,
            'background': background,
            'foreground': foreground,
            'fontsize': fontsize,
            'width': width
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    file_name = f'{self.id}_{self.limit}.gif'
                    with open(file_name, 'wb') as file:
                        file.write(await response.content.read())
                    self.process_image(file_name)
                    return True
                return False

    @staticmethod
    def process_image(infile):
        image = Image.open(infile)
        palette = image.getpalette()

        try:
            image.putpalette(palette)
            new_im = Image.new("RGBA", image.size)
            new_im.paste(image)
            new_im.save(f'{infile.split(".")[0]}.png')
        except EOFError:
            pass

    def delete_photos(self):
        file_start = f'{self.id}_{self.limit}'
        os.system(f'rm -r {file_start}.png')
        os.system(f'rm -r {file_start}.gif')

    class Meta:
        database = db
        db_table = 'wolfram'


if __name__ == '__main__':
    wolfram = Wolfram(app_id='PEXXAK-3GLT4V5VK6')
    wolfram.process_image('None_2000.gif')
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(wolfram.check_request('1+2'))
