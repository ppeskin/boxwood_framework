import copy
import quopri
from patterns.behavioral_patterns import ConsoleWriter, Subject
from patterns.architectural_system_pattern_unit_of_work import DomainObject
import sqlite3
import threading


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name


# преподаватель
class Teacher(User):
    pass


# студент
class Student(User, DomainObject):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


# инструктор
class Instructor(User):
    pass


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'instructor': Instructor,
        'student': Student,
        'teacher': Teacher
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# порождающий паттерн Прототип - Курс
class CoursePrototype:
    # прототип курсов обучения
    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


# OffLine курс
class OfflineCourse(Course):
    pass


# Интерактивный курс
class InteractiveCourse(Course):
    pass


# Курс в записи
class RecordCourse(Course):
    pass


# порождающий паттерн Абстрактная фабрика - фабрика курсов
class CourseFactory:
    types = {
        'offline': OfflineCourse,
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# Категория
class Category:
    # реестр?
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


# Основной интерфейс проекта
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id_):
        for item in self.categories:
            print('item', item.id)
            if item.id == id_:
                return item
        raise Exception(f'Нет категории с id = {id_}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)


class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            idx, name = item
            student = Student(name)
            student.id = idx
            result.append(student)
        return result

    def find_by_id(self, idx):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (idx,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={idx} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        # try:
        #     self.connection.commit()
        # except Exception as e:
        #     raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel?
        # Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.id))
        # try:
        #     self.connection.commit()
        # except Exception as e:
        #     raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        # try:
        #     self.connection.commit()
        # except Exception as e:
        #     raise DbDeleteException(e.args)

    # def commit(self):
    #     print('StudentMapper.commit()')
    #     try:
    #         self.connection.commit()
    #     except Exception as e:
    #         raise DbCommitException(e.args)


# connection = sqlite3.connect('patterns.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:

    connection = sqlite3.connect('patterns.sqlite')

    mappers = {
        'student': StudentMapper,
        # 'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):
        print(f"ой ой{obj.__class__}")
        if isinstance(obj, Student):
            return StudentMapper(MapperRegistry.connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](MapperRegistry.connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
