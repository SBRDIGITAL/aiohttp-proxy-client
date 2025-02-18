from asyncio import run

from pprint import pprint
from traceback import print_exc

from app.app import Proxer, AsyncHttpClient, AsyncHttpClientHelper

        
        
async def main():
    """
    ## Основная функция для демонстрации работы клиента.
    
    Пример использования классов `AsyncHttpClient` и `Proxer`.
    """  
    proxer = Proxer()
    proxy, login, password = proxer.get_random_proxy()
    proxy_auth = AsyncHttpClientHelper.get_proxy_auth(login, password)
    try:
        client = AsyncHttpClient()
        response = await client.fetch(
            url='https://jsonplaceholder.typicode.com/posts',
            method='GET', mode='JSON', proxy=proxy, proxy_auth=proxy_auth
        )
        pprint(response)
        
    except:
        print_exc()
        
    finally:
        await client.close()


if __name__ == '__main__':
    run(main())