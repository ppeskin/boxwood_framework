from time import time


# структурный паттерн - Декоратор

# 0. Добавить декоратор для добавления связки url-view в приложение, чтобы
# можно было добавлять url-ы, как в фреймворке Flask @app(‘/some_url/’).
class App:
    def __init__(self, routes, url):
        '''
        Сохраняем значение переданного параметра
        '''
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        '''
        Сам декоратор
        '''
        self.routes[self.url] = cls()


# 1. Добавить декоратор @debug, для view. Если мы указываем данный декоратор
# над view, то в терминал выводятся название функции и время ее выполнения.
class Debug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        '''
        сам декоратор
        '''

        def timeit(method):
            '''
            нужен для того, чтобы декоратор класса wrapper обернул в timeit
            каждый метод декорируемого класса
            '''

            def timed(*args, **kw):
                ts = time()
                result = method(*args, **kw)
                te = time()
                delta = te - ts

                print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)
