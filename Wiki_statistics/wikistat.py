from bs4 import BeautifulSoup
import re
import os


class Graf:
    '''Неориентированный граф.
    '''

    def __init__(self, adjacency_list):
        '''Конструктор графа, принимает матрицу смежности вершин.
        '''
        # Смежность вершин.  
        self.adjacency_list = adjacency_list

    def BFS(self, start, finish):
        '''Поиск в ширину (англ. breadth-first search, BFS) — метод
        обхода графа и поиска пути в графе.
        '''
        # Используемые вершины будут храниться в этом множестве.  
        used = set()
        # Создаем очередь.  
        queue = list()
        # Будем запоминать родительскую страницу для текущей.  
        parents = dict()
        for vertex in self.adjacency_list.keys():
            parents[vertex] = ''
        # Поместим в начало очереди вершину дерева.  
        queue.append(start)
        used.add(start)
        parents[start] = start
        # Пока очередь не пуста.  
        while len(queue) != 0:
            # Берем элемент вначале очереди.  
            current = queue[0]
            del queue[0]
            for i in range(len(self.adjacency_list[current])):
                # Осматриваем соседей.  
                to = self.adjacency_list[current][i]
                # если не заходили к ним,  
                if to not in used:
                    # то заходим
                    used.add(to)
                    # и ставим их в очередь
                    queue.append(to)
                    # запоминаем родительскую страницу.  
                    parents[to] = current
        # Кратчайший путь:
        way = [finish]
        while finish != start:
            finish = parents[finish]
            way.append(finish)
        return way


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_tree(start, end, path):
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")  # Искать ссылки можно как угодно, не обязательно через re
    files = dict.fromkeys(os.listdir(path))  # Словарь вида {"filename1": None, "filename2": None, ...}
    for file_name in files:
        files[file_name] = []
        with open(path+file_name) as file:
            for artical in re.findall(link_re, file.read()):
                if artical in files.keys() and artical not in files[file_name]:
                    files[file_name].append(artical)
    return files


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(start, end, path):
    files = build_tree(start, end, path)
    graf = Graf(files)
    bridge = graf.BFS(start, end)
    return bridge


def parse(start, end, path):
    """
    Если не получается найти список страниц bridge, через ссылки на которых можно добраться от start до end, то,
    по крайней мере, известны сами start и end, и можно распарсить хотя бы их: bridge = [end, start]. Оценка за тест,
    в этом случае, будет сильно снижена, но на минимальный проходной балл наберется, и тест будет пройден.
    Чтобы получить максимальный балл, придется искать все страницы. Удачи!
    """

    bridge = build_bridge(start, end, path)  # Искать список страниц можно как угодно, даже так: bridge = [end, start]
    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        imgs = 0
        headerss = 0
        linkslen = 0
        lists = 0
        with open("{}{}".format(path, file)) as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        # Количество картинок (img) с шириной (width) не меньше 200
        for pic in body.find_all('img', width=True):
            if int(pic['width']) >= 200:
                imgs += 1
        
        # Количество заголовков, первая буква текста внутри которого: E, T или C
        for headers in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if headers.string == None:
                for header in headers.find_all('span'):
                    if header.string != None:
                        if header.string[0] == 'E' or header.string[0] == 'T' or header.string[0] == 'C':
                            headerss += 1
            else:
                if headers.string[0] == 'E' or headers.string[0] == 'T' or headers.string[0] == 'C':
                    headerss += 1
        
        # Длина максимальной последовательности ссылок, между которыми нет других тегов
        tag = body.find_next("a")
        linkslen = -1
        while (tag):
            curlen = 1
            for tag in tag.find_next_siblings():
                if tag.name != 'a':
                    break
                curlen += 1
            if curlen > linkslen:
                linkslen = curlen
            tag = tag.find_next("a")
        
        # Количество списков, не вложенных в другие списки
        for tag in body.find_all(['ol', 'ul']):
            if tag.parent.name != 'li':
                lists += 1

        out[file] = [imgs, headerss, linkslen, lists]

    return out
