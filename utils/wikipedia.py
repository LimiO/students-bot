from typing import Optional, Union, List, Dict

from bs4 import BeautifulSoup
import aiohttp


class Wiki:
    @classmethod
    async def get_page(cls, page_id: int, lang: Optional[str] = 'ru',
                       is_one: bool = False) -> Union[List[str], str, None]:
        url = f'https://{lang}.wikipedia.org/w/api.php'
        params = {
            "action": "parse",
            "pageid": page_id,
            "format": "json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as request:
                json = (await request.json())
                if 'error' not in json:
                    soup = BeautifulSoup(json["parse"]["text"]["*"], 'lxml')
                    els = soup.find_all('p')
                    if is_one:
                        return els[0].text
                    return [el.text for el in els]
                return None

    @classmethod
    async def search(cls, query: str, lang: str = 'ru') -> Union[Dict[str, int], None]:
        url = f'https://{lang}.wikipedia.org/w/api.php'
        params = {
            "action": "query",
            "srsearch": query,
            "list": "search",
            "format": "json",
            "prop": "links"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as request:
                json = await request.json()
                if not json.get("query"):
                    return None
                return {page["title"]: page["pageid"] for page in json["query"]["search"][:3]}