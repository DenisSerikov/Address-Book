from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget

# генерация приложения
Form, Window = uic.loadUiType("untitled.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec_()
import json
import os

class Person(object):
    def __init__(self, name=None, middle_name=None, surname=None, address=None, phone=None):
        self.name = name
        self.middle_name = middle_name
        self.surname = surname
        self.address = address
        self.phone = phone

    def __str__(self):
        return "{} {:>15} {:>15} {:>15} {:>15}".format(self.surname, self.name, self.middle_name, self.address,
                                                       self.phone)

    def __iter__(self):
        yield 'name', self.name
        yield 'middle_name', self.middle_name,
        yield 'surname', self.surname
        yield 'address', self.address
        yield 'phone', self.phone

    def get_fio(self):
        return "{} {} {}".format(self.surname, self.name, self.middle_name)

class Application(object):
    def __init__(self, database):
        self.database = database
        self.persons = []
        if not os.path.exists(self.database):
            pass
        else:
            with open(self.database, 'r') as person_list:
                persons = json.load(person_list)
                for pers in persons:
                    self.persons.append(Person(**pers))

        self.size = len(self.persons)

    def add(self):
        name, middle_name, surname, address, phone = self.getdetails()
        if name not in self.persons:
            self.persons.append(Person(name, middle_name, surname, address, phone))
        else:
            print("Контакт уже добавлен")

    def viewall(self):
        if self.persons:
            print("{} {:>15} {:>15} {:>15} {:>15}".format('Имя', 'Отчество', 'Фамилия', 'Адрес', 'Телефон'))
            for person in self.persons:
                print(person)
        else:
            print("Нет контактов")

    def search(self):
        name = input("Введите ФИО: ")
        result = list(filter(lambda x: x.get_fio().count(name), self.persons))
        if result:
            for name in result:
                print(name)
        else:
            print("Контакт не найден")

    def getdetails(self):
        name = input("Имя: ")
        middle_name = input("Отчество: ")
        surname = input("Фамилия: ")
        address = input("Адрес: ")
        phone = input("Телефон: ")
        return name, middle_name, surname, address, phone

    def update(self):
        name = input("Введите ФИО: ")
        try:
            result = self.persons.index(list(filter(lambda x: x.get_fio().count(name), self.persons))[0])
            print("Найдено. Внесите изменения:")
            name, middle_name, surname, address, phone = self.getdetails()
            self.persons[result] = Person(name, middle_name, surname, address, phone)
            print("Изменено")
        except (ValueError, IndexError):
            print("Контакт не найден")

    def delete(self):
        name = input("Введите ФИО: ")
        try:
            result = self.persons.index(list(filter(lambda x: x.get_fio().count(name), self.persons))[0])
            self.persons.pop(result)
            print("Удалено")
        except (ValueError, IndexError):
            print("Контакт не найден")

    def reset(self):
        self.persons = []

    def __del__(self):
        with open(self.database, 'w') as db:
            persons = []
            for pers in self.persons:
                persons.append(dict(pers))
            json.dump(persons, db)


