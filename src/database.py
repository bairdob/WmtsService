import asyncio
import sqlite3


class AsyncSQLite:
    """
    Асинхронный контекстный менеджер для подключения к SQLite.
    """

    def __init__(self, path: str):
        """
        Инициализация.

        :param path: Путь до SQLite.
        """
        self.path = path
        self.connection: sqlite3.Connection = None

    async def __aenter__(self) -> 'AsyncSQLite':
        """
        Вход в контекстный менеджер.

        :return: подключение к SQLite.
        """
        loop = asyncio.get_running_loop()
        self.connection = await loop.run_in_executor(
            None, lambda: sqlite3.connect(self.path, check_same_thread=False)
        )
        return self

    async def __aexit__(self, exc_type: type, exc_val: Exception, exc_tb: type) -> None:
        """
        Выход из контекстного менеджера.

        :param exc_type: Тип исключения.
        :param exc_val: Инстанс исключения.
        :param exc_tb: Трассировка исключения.
        """
        if self.connection:
            await asyncio.get_running_loop().run_in_executor(
                None, self.connection.close
            )

    async def get_db_data(self, query: str, fetch_all: bool = False) -> list:
        """
        Получение данных из БД на основе запроса.

        :param query: SQL-запрос.
        :param fetch_all: True - получить все строки, False - получить одну строку.
        :return: Результат запроса.
        """
        cursor = self.connection.cursor()
        cursor.execute(query)

        results = (
            await asyncio.get_running_loop().run_in_executor(None, cursor.fetchall)
            if fetch_all
            else await asyncio.get_running_loop().run_in_executor(None, cursor.fetchone)
        )

        cursor.close()

        if not results:
            raise sqlite3.OperationalError

        return results

    async def insert_data(self, query: str, values: tuple) -> None:
        """
        Вставка данных в базу данных с использованием запроса и значений.

        :param query: SQL-запрос.
        :param values: Значения для вставки.
        """
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        await asyncio.get_running_loop().run_in_executor(None, self.connection.commit)
        cursor.close()
