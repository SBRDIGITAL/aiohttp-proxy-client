from typing import Literal


class AppLiterals:
    """
    ## Содержит литералы типов для использования в аннотациях.
    
    Attributes:
        ReqMethods (Literal['GET', 'POST']): Допустимые `HTTP` методы запросов.
        ReqReturnMode (Literal['JSON', 'TEXT']): Форматы возвращаемых ответов.
    """
    ReqMethods = Literal['GET', 'POST']
    ReqReturnMode = Literal['JSON', 'TEXT']
    