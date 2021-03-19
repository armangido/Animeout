import requests
import re
from bs4 import BeautifulSoup

class Animeout():

    def __init__(self,search=None):
        self.search = requests.utils.quote(search) if search is not None else None #Url encode

    def __scrape__(self,content,text,name='a'):
        if isinstance(content,requests.models.Response):
            content = content.text
        soup = BeautifulSoup(
            content,
            'html.parser'
        )
        links = [
            link['href'] for link 
            in soup.find_all(
                lambda t: t.name == name and text in t.text
            )
        ]
        self.sorted_links = {}
        for link in links:
            try:
                quality = re.search(r'\d{3,4}',link).group(0)
                self.sorted_links[quality].append(link)
            except KeyError:
                self.sorted_links.update({quality:[link]})
        return self.sorted_links

    # param object: Can be a URL or a Response object

    def _scrape_ddl(self,object):
        if not isinstance(object,requests.models.Response) and isinstance(object,str):
            object = requests.get(object)
        if object.status_code == 200:
            return self.__scrape__(object.text,text='Direct Download')
        else:
            raise Exception(f'Response is not 200 OK| Status code: {object.status_code}')

    def _scrape_mega(self,object):
        if not isinstance(object,requests.models.Response) and isinstance(object,str):
            object = requests.get(object)
        object = requests.get(object)
        if object.status_code == 200:
            return self.__scrape__(object.text,text='MEGA')
        else:
            raise Exception(f'Response is not 200 OK| Status code: {object.status_code}')

    #Currently not supporting pages

    def _search(self):
        if self.search is not None:
            response = requests.get(f'https://www.animeout.xyz/?s={self.search}')
            if response.status_code == 200:
                soup = BeautifulSoup(response.text,'html.parser')
                return {link.text : link.get('href') for link in soup.find_all('h3',class_='post-title entry-title') for link in link.find_all('a')}
            else:
                raise Exception(f'Response is not 200 OK| Status code: {response.status_code}')