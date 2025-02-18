import random
from typing import Literal, Optional
from asyncio import run

from aiohttp.helpers import BasicAuth
from aiohttp import ClientSession, ClientResponse

from pprint import pprint
from traceback import print_exc



class AppLiterals:
    """
    ## Содержит литералы типов для использования в аннотациях.
    
    Attributes:
        ReqMethods (Literal['GET', 'POST']): Допустимые `HTTP` методы запросов.
        ReqReturnMode (Literal['JSON', 'TEXT']): Форматы возвращаемых ответов.
    """
    ReqMethods = Literal['GET', 'POST']
    ReqReturnMode = Literal['JSON', 'TEXT']
    

class AsyncHttpClientHelper:
    """
    ## Вспомогательный класс для работы с `HTTP` клиентом.
    
    Предоставляет базовые методы для настройки подключения.
    """
    
    @classmethod
    def get_proxy_auth(cls, login: str, password: str, encoding: str = 'utf-8') -> BasicAuth:
        """
        ## Создает объект аутентификации для прокси.

        Args:
            login (str): Логин для авторизации на прокси.
            password (str): Пароль для авторизации на прокси.
            encoding (str, optional): Кодировка учетных данных. Defaults to `utf-8`.

        Returns:
            BasicAuth: Объект аутентификации.
        """      
        return BasicAuth(login, password, encoding)
    
    def get_session(self,
        proxy: Optional[str] = None,
        proxy_auth: Optional[BasicAuth] = None,
        cookies: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> ClientSession:
        """
        ## Создает новую клиентскую сессию.

        Args:
            proxy (Optional[str], optional): URL прокси-сервера. Defaults to None.
            proxy_auth (Optional[BasicAuth], optional): Данные аутентификации. Defaults to None.
            cookies (Optional[dict], optional): Куки для запросов. Defaults to None.
            headers (Optional[dict], optional): Заголовки запросов. Defaults to None.

        Returns:
            ClientSession: Объект клиентской сессии.
        """
        return ClientSession(proxy=proxy, proxy_auth=proxy_auth, cookies=cookies, headers=headers)


class AsyncHttpClient(AsyncHttpClientHelper):
    """
    ## Асинхронный `HTTP` клиент на основе `aiohttp`.
    """

    async def __return_result(self,
        mode: AppLiterals.ReqReturnMode,
        response: ClientResponse
    ) -> dict | list | str:
        """
        ## Обрабатывает ответ сервера и возвращает данные в указанном формате.

        Внутренний метод для унифицированной обработки HTTP ответов. 
        Автоматически проверяет статус ответа и преобразует данные.

        Args:
            mode (AppLiterals.ReqReturnMode): Режим обработки ответа:
                - 'JSON': возвращает распарсенный JSON-объект.
                - 'TEXT': возвращает сырой текст ответа.
            response (ClientResponse): Объект ответа от сервера.

        Returns:
            Union[dict, list, str, None]: Результат в указанном формате или None при ошибке.

        Raises:
            aiohttp.ClientResponseError: При HTTP ошибках (4xx/5xx).
            JSONDecodeError: При ошибках парсинга JSON (в режиме 'JSON').
        """      
        try:
            response.raise_for_status()
            if mode == 'JSON':
                return await response.json()
            elif mode == 'TEXT':
                return await response.text()
        except:
            print_exc()
    
    async def fetch(self,
        url: str,
        method: AppLiterals.ReqMethods,
        mode: AppLiterals.ReqReturnMode,
        proxy: Optional[str] = None,
        proxy_auth: Optional[BasicAuth] = None,
        cookies: Optional[dict] = None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None
    ) -> list | dict | str | None:
        """
        ## Выполняет HTTP запрос.

        Args:
            url (str): Целевой URL
            method (AppLiterals.ReqMethods): HTTP метод (GET/POST).
            mode (AppLiterals.ReqReturnMode): Формат ответа (JSON/TEXT).
            proxy (Optional[str], optional): Прокси-сервер. Defaults to None.
            proxy_auth (Optional[BasicAuth], optional): Аутентификация прокси. Defaults to None.
            cookies (Optional[dict], optional): Куки запроса. Defaults to None.
            headers (Optional[dict], optional): Заголовки запроса. Defaults to None.
            params (Optional[dict], optional): Параметры запроса. Defaults to None.

        Returns:
            Union[list, dict, str, None]: Ответ в указанном формате или None при ошибке.

        Raises:
            aiohttp.ClientError: Ошибки сетевого взаимодействия.
        """
        session = self.get_session(proxy, proxy_auth, cookies, headers)
        if method == 'GET':
            async with session.get(url, params=params) as response:
                return await self.__return_result(mode, response)
        elif method == 'POST':
            async with session.post(url, params=params) as response:
                return await self.__return_result(mode, response)

    async def close(self, session: Optional[ClientSession] = None) -> None:
        """
        ## Закрывает активную сессию.

        Args:
            session (Optional[ClientSession], optional): Конкретная сессия для закрытия. Defaults to None.
        """    
        if session:
            await session.close()


class Proxer:
    """
    ## Менеджер для работы с прокси.
    
    Attributes:
        pfp (str): Путь к файлу с прокси.
        proxies (list[str]): Загруженные прокси.
    """
    
    def __init__(self, proxy_file_path: str = 'proxy.txt'):
        self.pfp: str = proxy_file_path
        self.proxies: list[str] = self.load_proxies_from_file()

    def load_proxies_from_file(self) -> list[str]:
        """
        ## Загружает прокси из файла.

        Returns:
            list[str]: Список строк с прокси.
        """
        try:
            with open(self.pfp, 'r', encoding='utf-8') as f:
                return f.readlines()
        except FileNotFoundError as ex:
            print(f'Создай файл {self.pfp} и положи в него прокси, каждую на новой строке.')
            raise ex
    
    def get_random_proxy(self):
        """
        ## Возвращает случайный прокси из списка.

        Returns:
            tuple: Кортеж вида (протокол://хост:порт, логин, пароль).

        Raises:
            ValueError: При некорректном формате прокси.
        
        Пример использования:
            ```python
                proxer = Proxer()
                proxy, login, password = proxer.get_random_proxy()
            ```
        """       
        try:
            proxy = random.choice(self.proxies)
            if proxy:
                if "://" in proxy:
                    protocol, rest = proxy.split("://", 1)
                else:
                    protocol = "http"
                    rest = proxy
                    
                parts = rest.split(":")
                if len(parts) < 4:
                    raise ValueError("Invalid proxy format")
                return f"{protocol}://{parts[0]}:{parts[1]}", parts[2], parts[3]
            
        except Exception as ex:
            raise ex
        
        
        
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