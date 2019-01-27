from calendar import TextCalendar, month_name
from collections import OrderedDict
from abc import ABCMeta, abstractmethod


class BookIOErrors(Exception):
    """базовый класс исключений"""


class PageNotFoundError(BookIOErrors):
    """для ситуаций, когда методы обращаются к несуществующей странице"""


class TooLongTextError(BookIOErrors):
    """для ситуаций, когда записываемый текст не помещается на странице"""


class PermissionDeniedError(BookIOErrors):
    """для ситуаций, когда запись в книгу запрещена"""


class NotExistingExtensionError(BookIOErrors):
    """если вызываемый метод у класса книги отсутствует"""


class Page:
    """класс страница"""

    def __init__(self, text=None, max_sign=2000):
        self._text = text or ''
        self.max_sign = max_sign

    def __str__(self):
        '''возвращает текст страницы'''
        return self._text

    def __len__(self):
        '''возвращает количество знаков в странице'''
        return len(self._text)

    def __iadd__(self, other):
        '''сложение для object += "other"'''
        if isinstance(other, str):
            if len(self)+len(other) <= self.max_sign:
                self._text += other
                return self
            else:
                raise TooLongTextError
        else:
            raise TypeError

    def __add__(self, other):
        '''сложение для object + "string"'''
        if isinstance(other, str):
            if len(self)+len(other) <= self.max_sign:
                self._text += other
                return self
            else:
                raise TooLongTextError
        else:
            raise TypeError

    def __radd__(self, other):
        '''сложение для "string" + object'''
        if isinstance(other, str):
            return str(other+self._text)
        else:
            raise TypeError

    def __gt__(self, obj):
        '''сравнение ">" двух обьектов класса'''
        if isinstance(obj, Page) or isinstance(obj, str):
            return len(self) > len(obj)
        else:
            raise TypeError

    def __lt__(self, obj):
        '''сравнение "<" двух обьектов класса'''
        if isinstance(obj, Page) or isinstance(obj, str):
            return len(self) < len(obj)
        else:
            raise TypeError

    def __eq__(self, obj):
        '''сравнение "==" двух обьектов класса'''
        if isinstance(obj, Page) or isinstance(obj, str):
            return len(self) == len(obj)
        else:
            raise TypeError

    def __ge__(self, obj):
        '''сравнение ">=" двух обьектов класса'''
        if isinstance(obj, Page) or isinstance(obj, str):
            return len(self) >= len(obj)
        else:
            raise TypeError

    def __le__(self, obj):
        '''сравнение "<=" двух обьектов класса'''
        if isinstance(obj, Page) or isinstance(obj, str):
            return len(self) <= len(obj)
        else:
            raise TypeError


class PageTableContents(Page):
    '''класс страницы оглавления'''

    def __init__(self, text=None, max_sign=2000):
        self._text = text or 'TABLE OF CONTENT\n'
        self.max_sign = max_sign
        self._parser_text_table()

    def _parser_text_table(self):
        '''создает оглавление из входящего текста'''
        table = {}
        for value in map(lambda x: x.split(':'), self._text.split('\n')):
            table[value[0]] = int(value[1]) if len(value) == 2 else ''
        self._table = OrderedDict(table)

    def __str__(self):
        '''возвращает текст страницы'''
        string = ''
        for key in self._table:
            if self._table[key] == '':
                string += key
            else:
                string += '\n'+key+':'+str(self._table[key])
        string += '\n'
        return string

    def search(self, chapter):
        '''поиск номера страницы по названию главы'''
        if chapter in self._table:
            return self._table[chapter]
        else:
            raise PageNotFoundError

    def __iadd__(self, other):
        '''сложение для object += "other"'''
        raise PermissionDeniedError

    def __add__(self, other):
        '''сложение для object + "string"'''
        raise PermissionDeniedError

    def __radd__(self, other):
        '''сложение для "string" + object'''
        raise PermissionDeniedError


class Book:
    """класс книга"""

    def __init__(self, title, content=None):
        self.title = title
        self._content = content or []

    def __getitem__(self, num_page):
        '''обращение к элементам обьекта с помощью []'''
        if 1 <= num_page <= len(self):
            return self._content[num_page-1] # нумерация страниц начинается с 1
        else:
            raise PageNotFoundError

    def __setitem__(self, num_page, value):
        '''перезапись страницы в книге'''
        if 1 <= num_page <= len(self):
            self._content[num_page-1] = Page(value) # нумерация страниц начинается с 1
        else:
            raise PageNotFoundError

    def __gt__(self, obj):
        '''сравнение ">" двух обьектов класса'''
        if isinstance(obj, Book):
            return len(self) > len(obj)
        else:
            raise TypeError

    def __lt__(self, obj):
        '''сравнение "<" двух обьектов класса'''
        if isinstance(obj, Book):
            return len(self) < len(obj)
        else:
            raise TypeError

    def __eq__(self, obj):
        '''сравнивание "==" двух обьектов класса'''
        if isinstance(obj, Book):
            return len(self) == len(obj)
        else:
            raise TypeError

    def __ge__(self, obj):
        '''сравнение ">=" двух обьектов класса'''
        if isinstance(obj, Book):
            return len(self) >= len(obj)
        else:
            raise TypeError

    def __le__(self, obj):
        '''сравнение "<=" двух обьектов класса'''
        if isinstance(obj, Book):
            return len(self) <= len(obj)
        else:
            raise TypeError

    def __len__(self):
        '''длинна книги'''
        return len(self._content)


class CalendarBookmark:
    """класс дескриптор - закладка для ежедневника"""

    def __init__(self):
        """конструктор"""
        self.value = 0

    def __get__(self, obj, obj_type):
        '''возвращает закладку'''
        return self.value

    def __set__(self, obj, value):
        '''устанавливает закладку'''
        if value == 0 or value < 1 or value > obj._size:
            raise PageNotFoundError
        else:
            self.value = value


class CalendarBook(Book):
    """класс книги - ежедневник с закладкой"""
    bookmark = CalendarBookmark()

    def __init__(self, title, content=None):
        """конструктор"""
        super().__init__(title, content)
        self._calendar(int(title))

    def _calendar(self, year):
        '''функция создания контента ежедневника'''
        string_to_table = 'TABLE OF CONTENT\n'
        calendar = TextCalendar()
        for month in range(1, 13):
            self._content.append(calendar.formatmonth(year, month))
            string_to_table += month_name[month]+':'+str(len(self._content))+'\n'
            for day in calendar.itermonthdates(year, month):
                if day.month == month:
                    self._content.append(str(day))
        self._content.append(PageTableContents(string_to_table))
        self._size = len(self._content)

    def __delattr__(self, name):
        '''удаление атрибута'''
        raise AttributeError


class Person:
    __metaclass__ = ABCMeta

    """класс описывающий человека"""
    def __init__(self, name):
        """конструктор"""
        self.name = name

    @abstractmethod
    def set_bookmark(self, book, value):
        '''устанавливает закладку в книгу'''
        book.bookmark = value

    @abstractmethod
    def get_bookmark(self, book):
        '''возвращает закладку из книги'''
        return book.bookmark

    @abstractmethod
    def del_bookmark(self, book):
        '''удаляет закладку из книги'''
        del book.bookmark


class Reader:
    '''читает страницу num_page из book'''

    def read(self, book, num_page):
        return book[num_page]


class Writer:
    '''записывает в книгу новый текст'''

    def write(self, book, num_page, text):
        book[num_page] += text


class AdvancedPerson(Person, Reader, Writer):
    """класс человека умеющего читать, писать, пользоваться закладками"""

    def set_bookmark(self, book, num_page):
        '''устанавливает закладку в книгу'''
        book.bookmark

    def get_bookmark(self, book):
        '''возвращает закладку из книги'''
        return book.bookmark

    def del_bookmark(self, book, person):
        '''удаляет закладку из книги'''
        del book.bookmark

    def search(self, book, chapter):
        '''возвращает номер страницы главы'''
        if len(book) != 0 and isinstance(book[len(book)], PageTableContents):
            return book[len(book)].search(chapter)
        else:
            raise NotExistingExtensionError

    def read(self, book, chapter):
        '''читает страницу num_page из book'''
        if isinstance(chapter, str):
            return Reader().read(book, int(self.search(book, chapter)))
        else:
            return Reader().read(book, chapter)

    def write(self, book, page, text):
        '''записывает в книгу новый текст'''
        Writer().write(book, page, text)
