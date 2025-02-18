import random


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