__author__ = "VadimTrubay"

from abc import ABC, abstractmethod
from collections import UserList
from colorama import init, Fore, Style
from datetime import datetime, timedelta, date
import numexpr
import os.path
import os
import pickle
import re
import shutil
from typing import Iterator, List, Dict
from time import sleep


fields_dict_contact = ["firstname", "lastname", "phone", "birthday", "address", "email", "status", "note"]
fields_dict_note = ["title", "note", "tag"]


def log(name: str = "", obj: str = "", action: str = ""):
    current_time = datetime.strftime(datetime.now(), '[%Y-%m-%d] [%H:%M:%S]')
    message = f'{current_time} - {name} {obj} {action}'
    with open('logs.txt', 'a') as file:
        file.write(f'{message}\n')


def print_main_menu():
    print_red_message("{:^42}".format("Menu"))
    print_white_message(42 * "-" + "")
    print_green_message('1. address book')
    print_green_message('2. note book')
    print_green_message('3. file sort')
    print_green_message('4. calculator')
    print_green_message('5. exit')
    print_white_message(42 * "-" + "\n")


def print_contactbook_menu():
    print_red_message("{:^42}".format("Contactbook"))
    print_white_message(42 * "-" + "")
    print_green_message('1. show all contacts')
    print_green_message('2. add new contact')
    print_green_message('3. find contacts by pattern')
    print_green_message('4. edit contact')
    print_green_message('5. congratulate contacts')
    print_green_message('6. days to birthday')
    print_green_message('7. delete contact')
    print_green_message('8. clear Contactbook')
    print_green_message('9. save Contactbook')
    print_green_message('10. load Contactbook')
    print_green_message('11. exit')
    print_white_message(42 * "-" + "")


def print_notebook_menu():
    print_red_message("{:^42}".format("Notebook"))
    print_white_message(42 * "-" + "")
    print_green_message('1. show all notes')
    print_green_message('2. add new note')
    print_green_message('3. find note by title')
    print_green_message('4. find note by tag')
    print_green_message('5. edit note')
    print_green_message('6. delete note')
    print_green_message('7. clear notebook')
    print_green_message('8. save notebook')
    print_green_message('9. load notebook')
    print_green_message('10. exit')
    print_white_message(42 * "-" + "")


def print_calculator_menu():
    print_red_message("{:^42}".format("Notebook"))
    print_white_message(42 * "-" + "")
    print_green_message('1. run calculator')
    print_green_message('2. exit')
    print_white_message(42 * "-" + "")


def print_red_message(name: str = "", obj: str = "", action: str = "", end="\n"):
    print(Fore.RED + f"{name} {obj} {action}", end=end)


def print_green_message(name: str = "", obj: str = "", action: str = "", end="\n"):
    print(Fore.GREEN + f"{name} {obj} {action}", end=end)


def print_white_message(name: str = "", obj: str = "", action: str = "", end="\n"):
    print(Fore.WHITE + f"{name} {obj} {action}", end=end)


def print_blue_message(name: str = "", obj: str = "", action: str = "", end="\n"):
    print(Fore.BLUE + f"{name} {obj} {action}", end=end)


def print_yellow_message(name: str = "", obj: str = "", action: str = "", end="\n"):
    print(Fore.YELLOW + f"{name} {obj} {action}", end=end)


def print_contact(value: str):
    fields_dict = 0
    print_white_message("-" * 25)
    if len(value) == 8:
        fields_dict = fields_dict_contact
    if len(value) == 3:
        fields_dict = fields_dict_note
    for field in fields_dict:
        print_green_message(f"{field}: ", end="")
        print_white_message(f"{value.get(field)}")
    print_white_message("-" * 25)


def print_all_name_contacts(all_contacts: List):
    print_green_message("all names:")
    for contact in sorted(all_contacts):
        print_white_message(contact)


def print_all_titles(all_titles: List):
    print_green_message("all titles:")
    for title in sorted(all_titles):
        print_white_message(title)


def print_note(note: str):
    print_white_message("-" * 25)
    for field in fields_dict_note:
        print_green_message(f"{field}: ", end="")
        print_white_message(f"{note.get(field)}")
    print_white_message("-" * 25)


def print_congratulate(congratulate: Dict):
    if congratulate:
        for day, contact in congratulate.items():
            if contact:
                print_green_message(f"{day}: ", end="")
                print_white_message(f"{', '.join(contact)}")
    else:
        print_red_message("no birthdays")


def print_goodbye():
    print_yellow_message('Good bye!')
    sleep(1)


def iterator(n: int, data: list) -> Iterator[list]:
    index = 0
    temp = []
    for value in data:
        temp.append(value)
        index += 1
        if index >= n:
            yield temp
            temp.clear()
            index = 0
    if temp:
        yield temp


def get_page(n: int, data):
    gen = iterator(n, data)
    for i in range(len(data)):
        try:
            result = next(gen)
            for value in result:
                print_contact(value)
            print_red_message(f"page {i + 1}")
            input(Fore.YELLOW + "press enter for next page>")

        except StopIteration:
            break


class RecordContactbook:

    def __init__(self, firstname="", lastname="", phone="", birthday="",
                 address="", email="", status="", note=""):

        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.birthday = birthday
        self.address = address
        self.email = email
        self.status = status
        self.note = note


class Contactbook(UserList):

    def __init__(self):
        super().__init__()
        self.data = []


    def __str__(self) -> List[str]:
        result = []
        for contact in self.data:
            result.append(f"firstname: {contact['firstname']}\n"
                          f"lastname: {contact['lastname']}\n"
                          f"phone: {contact['phone']}\n"
                          f"birthday: {contact['birthday']}\n"
                          f"address: {contact['address']}\n"
                          f"email: {contact['email']}\n"
                          f"status: {contact['status']}\n"
                          f"note: {contact['note']}\n")

        return result


    def __setitem__(self, key, value: str):
        self.data[key] = {"firstname": value.firstname,
                          "lastname": value.lastname,
                          "phone": value.phone,
                          "birthday": value.birthday,
                          "address": value.address,
                          "email": value.email,
                          "status": value.status,
                          "note": value.note
                          }


    def __getitem__(self, key) -> Dict:
        return self.data[key]


    def add(self, record: RecordContactbook):
        contact = {"firstname": record.firstname,
                   "lastname": record.lastname,
                   "phone": record.phone,
                   "birthday": record.birthday,
                   "address": record.address,
                   "email": record.email,
                   "status": record.status,
                   "note": record.note
                   }

        self.data.append(contact)


    def find_info(self, parameter: str, pattern: str) -> List:
        result = []
        for contact in self.data:
            if pattern in contact[parameter]:
                result.append(contact)
        return result


    def edit(self, firstname: str, lastname: str, parameter: str, new_value: str):
        for contact in self.data:
            if contact["firstname"] == firstname and contact["lastname"] == lastname:
                contact[parameter] = new_value
                break
            else:
                continue

    @staticmethod
    def __get_current_week() -> List:
        now = datetime.now()
        current_weekday = now.weekday() + 1
        if current_weekday < 5:
            week_start = now - timedelta(days=0 + current_weekday)
        else:
            week_start = now - timedelta(days=current_weekday - 4)

        return [week_start.date(), week_start.date() + timedelta(days=7)]


    def congratulate(self) -> Dict[str, List[str]]:
        WEEKDAYS = ["", "monday", "tuesday", "wednesday", "thursday", "friday"]
        congratulate = {"monday": [], "tuesday": [], "wednesday": [], "thursday": [], "friday": []}
        for contact in self.data:
            if contact["birthday"]:
                birthday = contact["birthday"]
                birth_day = datetime.strptime(birthday, "%d.%m.%Y")
                birth_day = date(birth_day.year, birth_day.month, birth_day.day)
                current_date = date.today()
                new_birthday = birth_day.replace(year=current_date.year)
                birthday_weekday = new_birthday.weekday() + 1
                if self.__get_current_week()[0] <= new_birthday < self.__get_current_week()[1]:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(contact["firstname"]  + " " + contact["lastname"])
                    else:
                        congratulate["monday"].append(contact["firstname"] + " " + contact["lastname"])
        return  congratulate


    def days_to_birthday(self, firstname: str, lastname: str):
        days = 0
        for contact in self.data:
            if firstname == contact["firstname"] and lastname == contact["lastname"]:
                birthday = contact["birthday"]
                birth_day = datetime.strptime(birthday, '%d.%m.%Y')
                birth_day = date(birth_day.year, birth_day.month, birth_day.day)
                current_date = date.today()
                user_date = birth_day.replace(year=current_date.year)
                delta_days = user_date - current_date
                if delta_days.days >= 0:
                    days = delta_days.days
                else:
                    user_date = user_date.replace(year=user_date.year + 1)
                    delta_days = user_date - current_date
                    days = delta_days.days
                break

        return days


    def delete(self, firstname: str, lastname: str):
        for contact in self.data:
            if firstname == contact["firstname"] and lastname == contact["lastname"]:
                print_yellow_message("are you sure for delete contact? (y/n)")
                del_contact = input(Fore.BLUE + '>>>:')
                if del_contact == "y":
                    self.data.remove(contact)
                    break
                else:
                    break


    def clear_contactbook(self):
        self.data.clear()


    def save(self, file_name: str):
        with open(f'{file_name}.bin', 'wb') as file:
            pickle.dump(self.data, file)
        log('contactbook saved')


    def load(self, file_name: str):
        empty_ness = os.stat(f"{file_name}.bin")
        if empty_ness.st_size != 0:
            with open(f"{file_name}.bin", 'rb') as file:
                self.data = pickle.load(file)
            log('contactbook loaded')
        else:
            print_red_message('contactbook created')
            log('contactbook created')
        return self.data


class FieldContactbook(ABC):

    @abstractmethod
    def __getitem__(self):
        pass


class FirstNameContactbook(FieldContactbook):
    def __init__(self, value=""):
        while True:
            if value:
                self.value = value
            else:
                print_green_message("first name*")
                self.value = input(Fore.BLUE + ">>>:")
            try:
                if re.match(r"^[a-zA-Z\d,. !_-]{1,20}$", self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log("incorrect value")
                print_red_message("incorrect value, try again")


    def __getitem__(self):
        return self.value


class LastNameContactbook(FieldContactbook):
    def __init__(self, value=""):
        while True:
            if value:
                self.value = value
            else:
                print_green_message("last name*")
                self.value = input(Fore.BLUE + ">>>:")
            try:
                if re.match(r"^[a-zA-Z\d,. !_-]{1,20}$", self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log("incorrect value")
                print("incorrect value, try again")


    def __getitem__(self):
        return self.value


class PhoneContactbook(FieldContactbook):
    def __init__(self, value=""):
        while True:
            if value:
                self.value = value
            else:
                print_green_message("phone")
                self.value = input(Fore.BLUE + ">>>:")
            try:
                if re.match(r"^[0-9-+() ]{8,17}$", self.value) or self.value == "":
                    break
                else:
                    raise ValueError
            except ValueError:
                log("incorrect  number")
                print_red_message("incorrect number, try again")


    def __getitem__(self):
        return self.value


class BirthdayContactbook(FieldContactbook):
    def __init__(self, value=""):
        while True:
            if value:
                self.value = value
            else:
                print_green_message("birthday(dd.mm.YYYY)")
                self.value = input(Fore.BLUE + ">>>:")
            try:
                if re.match(r'^\d{2}.\d{2}.\d{4}$', self.value) or self.value == "":
                    break
                else:
                    raise ValueError
            except ValueError:
                log("incorrect  birthday")
                print_red_message("incorrect birthday, try again")


    def __getitem__(self):
        return self.value


class AddressContactbook(FieldContactbook):
    def __init__(self, value=""):
        while True:
            if value:
                self.value = value
            else:
                print_green_message("address")
                self.value = input(Fore.BLUE + ">>>:")
            try:
                if self.value or self.value == "":
                    break
                else:
                    raise ValueError
            except ValueError:
                log("incorrect value")
                print_red_message("incorrect value, try again")


    def __getitem__(self):
        return self.value


class EmailContactbook(FieldContactbook):

    def __init__(self, value=""):
        while True:
            if value:
                self.value = value
            else:
                print_green_message("email")
                self.value = input(Fore.BLUE + ">>>:")
            try:
                if re.match(r"^(\w|\.|_|-)+@(\w|_|-|\.)+[.]\w{2,3}$", self.value) or self.value == "":
                    break
                else:
                    raise ValueError
            except ValueError:
                log("incorrect  email")
                print_red_message("incorrect email, try again")


    def __getitem__(self):
        return self.value


class StatusContactbook(FieldContactbook):

    def __init__(self, value=""):
        while True:
            self.status_types = ["", "family", "friend", "work"]
            if value:
                self.value = value
            else:
                print_green_message("status(family, friend, work)")
                self.value = input(Fore.BLUE + '>>>:')
            try:
                if self.value in self.status_types:
                    break
                else:
                    raise ValueError
            except ValueError:
                log("there is no such status")
                print_red_message("incorrect status, try again")


    def __getitem__(self):
        return self.value


class NoteContactbook(FieldContactbook):

    def __init__(self, value =""):
        while True:
            if value:
                self.value = value
            else:
                print_green_message("note")
                self.value = input(Fore.BLUE + ">>>:")
            try:
                if self.value or self.value == "":
                    break
                else:
                    raise ValueError
            except ValueError:
                log("incorrect value")
                print_red_message("incorrect value, try again")


    def __getitem__(self):
        return self.value


class BotContactbook:
    def __init__(self):
        self.contactbook = Contactbook()


    def handle(self, command):
        try:
            if command == "1":
                while True:
                    try:
                        print_green_message("number of note per page")
                        n = int(input(Fore.BLUE + ">>>:"))
                    except ValueError:
                        print_red_message("incorrect number of note, try again")
                        continue
                    else:
                        if self.contactbook:
                            get_page(n, self.contactbook)
                            break
                        else:
                            print_red_message("contactbook empty")
                            break

            elif command == "2":
                firstname = FirstNameContactbook().value.strip().lower()
                lastname = LastNameContactbook().value.strip().lower()

                if firstname and lastname:
                    if self.contactbook:
                        for item in self.contactbook:
                            if firstname == item["firstname"] and lastname == item["lastname"]:
                                print_red_message("  this contact already exists\n" + "  enter command to edit")
                                log("contact", f"{firstname} {lastname}", "already exists")
                                break
                        else:
                            phone = PhoneContactbook().value.strip()
                            birthday = BirthdayContactbook().value.strip()
                            address = AddressContactbook().value.strip()
                            email = EmailContactbook().value.strip()
                            status = StatusContactbook().value.strip()
                            note = NoteContactbook().value.strip()
                            record = RecordContactbook(firstname, lastname, phone,
                                                       birthday, address, email, status, note)
                            self.contactbook.add(record)
                            print_red_message("contact", f"{firstname} {lastname}", "added")
                            log("contact", f"{firstname} {lastname}", "added")
                    else:
                        phone = PhoneContactbook().value.strip()
                        birthday = BirthdayContactbook().value.strip()
                        address = AddressContactbook().value.strip()
                        email = EmailContactbook().value.strip()
                        status = StatusContactbook().value.strip()
                        note = NoteContactbook().value.strip()
                        record = RecordContactbook(firstname, lastname, phone,
                                                   birthday, address, email, status, note)
                        self.contactbook.add(record)
                        print_red_message("contact", f"{firstname} {lastname}", "added")
                        log("contact", f"{firstname} {lastname}", "added")
                else:
                    print_red_message("please enter a name")

            elif command == "3":
                print_green_message("enter the parameter to find")
                parameter = input(Fore.BLUE + ">>>:").strip()
                print_green_message("enter the pattern:")
                pattern = input(Fore.GREEN + ">>>:").strip()
                if pattern:
                    result = self.contactbook.find_info(parameter, pattern)
                    if result:
                        for contact in result:
                            print_contact(contact)
                    else:
                        print_red_message("no matches found for pattern")
                else:
                    print_red_message("please enter a pattern")

            elif command == "4":
                all_contacts = []
                for contact in self.contactbook:
                    all_contacts.append(contact["firstname"] + " " + contact["lastname"])
                print_all_name_contacts(all_contacts)
                print_green_message("enter the firstname to edit")
                firstname = input(Fore.BLUE + ">>>:")
                print_green_message("enter the lastname to edit")
                lastname = input(Fore.BLUE + ">>>:")
                if firstname + " " + lastname in all_contacts:
                    print_green_message("enter the parameter to edit")
                    parameter = input(Fore.BLUE + ">>>:")
                    print_green_message("enter new value")
                    new_value = input(Fore.BLUE + ">>>:")
                    self.contactbook.edit(firstname, lastname, parameter, new_value)
                    print_red_message("contact", f"{firstname} {lastname}", "edited")
                    log("contact", f"{firstname} {lastname}", "edited")
                else:
                    log("contact not found")
                    print_red_message( "contact not found")

            elif command == "5":
                congratulate = self.contactbook.congratulate()
                print_congratulate(congratulate)

            # to be edited!!!
            elif command == "6":
                all_contacts = []
                for contact in self.contactbook:
                    all_contacts.append(contact["firstname"] + " " + contact["lastname"])
                print_all_name_contacts(all_contacts)
                print_green_message("enter the firstname to birthday")
                firstname = input(Fore.BLUE + ">>>:")
                print_green_message('enter the lastname to birthday')
                lastname = input(Fore.BLUE + ">>>:")
                if firstname + " " + lastname in all_contacts:
                    days = self.contactbook.days_to_birthday(firstname, lastname)
                    print_yellow_message(f"{days} days left until {firstname} {lastname}'s birthday")
                else:
                    log("contact not found")
                    print_red_message("contact not found")

            elif command == "7":
                all_contacts = []
                for contact in self.contactbook:
                    all_contacts.append(contact["firstname"] + " " + contact["lastname"])
                print_all_name_contacts(all_contacts)
                print_green_message("enter the firstname to delete")
                firstname = input(Fore.BLUE + ">>>:")
                print_green_message('enter the lastname to delete')
                lastname = input(Fore.BLUE + ">>>:")
                if firstname + ' ' + lastname in all_contacts:
                    self.contactbook.delete(firstname, lastname)
                    print_red_message("contact", f"{firstname} {lastname}", "deleted")
                    log("contact", f"{firstname} {lastname}", "deleted")
                else:
                    log("contact not found")
                    print_red_message("contact not found")

            elif command == "8":
                while True:
                    print_yellow_message("are you sure for delete all? (y/n)")
                    clear_all = input(Fore.BLUE + ">>>:")
                    if clear_all == "y":
                        self.contactbook.clear_contactbook()
                        print_red_message("contactbook cleared")
                        log("contactbook cleared")
                        break
                    else:
                        break

            elif command == "9":
                print_green_message("save file name")
                file_name = input(Fore.BLUE + '>>>:').strip()
                if file_name:
                    self.contactbook.save(file_name)
                    print_red_message(f'contactbook {file_name} saved')
                else:
                    print_red_message('please enter file name')

            elif command == "10":
                print_green_message("load file name")
                file_name = input(Fore.BLUE + ">>>:").strip()
                if file_name:
                    self.contactbook.load(file_name)
                    print_red_message(f"address_book {file_name} loaded")
                else:
                    print_red_message("please enter file name")

        except Exception as e:
            print(f"{e} invalid input, try again")


def contactbook():
    init()
    file_name = "contactbook_save"
    contactbot = BotContactbook()
    if os.path.exists(f"{file_name}.bin"):
        contactbot.contactbook.load(file_name)
    else:
        contactbot.contactbook.save(file_name)

    while True:
        os.system("cls")
        print_contactbook_menu()
        print_white_message("your choose(number)")
        user_input = input(Fore.BLUE + ">>>:")
        if user_input == "11":
            contactbot.contactbook.save(file_name)
            print_goodbye()
            break

        contactbot.handle(user_input)
        input(Fore.MAGENTA + "press Enter to continue")

        if user_input in ["2", "4", "7", "8"]:
            contactbot.contactbook.save(file_name)


class RecordNotebook:

    def __init__(self, title="", note="", tag=""):
        self.title = title
        self.note = note
        self.tag = tag


class NoteBook(UserList):

    def __init__(self):
        super().__init__()
        self.data = []

    def __str__(self) -> List[str]:
        result = []
        for contact in self.data:
            result.append(f"title: {contact['title']}\n"
                          f"note: {contact['note']}\n"
                          f"tag: {contact['tag']}\n")

        return result

    def __setitem__(self, key, value: str):
        self.data[key] = {"title": value.title,
                          "note": value.note,
                          "tag": value.tag
                          }

    def __getitem__(self, key):
        return self.data[key]

    def add(self, record: RecordNotebook):
        note = {"title": record.title,
                "note": record.note,
                "tag": record.tag
                }
        self.data.append(note)


    def find_note_by_title(self, title: str) -> List:
        titles = []
        for key in self.data:
            if title in key['title']:
                titles.append(key)
        return titles

    def find_note_by_tag(self, tag: str) -> List:
        tags = []
        for key in self.data:
            if tag in key['tag']:
                tags.append(key)
        return tags

    def edit_note(self, title: str, parameter: str, new_value: str):
        for note in self.data:
            if note['title'] == title:
                note[parameter] = new_value
                break
            else:
                continue

    def delete(self, note: str):
        for key in self.data:
            if key['title'] == note:
                print_green_message('are you sure for delete note? (y/n)')
                del_note = input(Fore.BLUE + '>>>:')
                if del_note == 'y':
                    self.data.remove(key)
                    break
                else:
                    break

    def clear_notebook(self):
        self.data.clear()

    def save(self, file_name: str):
        with open(f"{file_name}.bin", 'wb') as file:
            pickle.dump(self.data, file)
        log('notebook saved')

    def load(self, file_name: str):
        empty_ness = os.stat(f"{file_name}.bin")
        if empty_ness.st_size != 0:
            with open(f"{file_name}.bin", 'rb') as file:
                self.data = pickle.load(file)
            log('notebook loaded')
        else:
            print_red_message('notebook created')
            log('notebook created')
        return self.data


class FieldNotebook(ABC):

    @abstractmethod
    def __getitem__(self):
        pass


class TitleNotebook(FieldNotebook):

    def __init__(self, value=""):

        while True:
            if value:
                self.value = value
            else:
                print_green_message("title*")
                self.value = input(Fore.BLUE + '>>>:')
            try:
                if re.match(r'^[a-zA-Z\d,. !_-]{1,50}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log("incorrect title")
                print_red_message("incorrect title, try again")


    def __getitem__(self):
        return self.value


class NoteNotebook(FieldNotebook):

    def __init__(self, value=""):
        while True:
            if value:
                self.value = value
            else:
                print_green_message("note")
                self.value = input(Fore.BLUE + ">>>:")
            try:
                if re.match(r'^[a-zA-Z()?\d,. \-_!]{1,250}$', self.value) or self.value == "":
                    break
                else:
                    raise ValueError
            except ValueError:
                log('incorrect value')
                print_red_message('incorrect value, try again')

    def __getitem__(self):
        return self.value


class TagNotebook(FieldNotebook):

    def __init__(self, value=""):
        while True:
            if value:
                self.value = value
            else:
                print_green_message("tag")
                self.value = input(Fore.BLUE + ">>>:")
            try:
                if re.match(r'^[a-zA-Z\d,. !]{1,20}$', self.value) or self.value == "":
                    break
                else:
                    raise ValueError
            except ValueError:
                log("incorrect value")
                print_red_message("incorrect value, try again")


    def __getitem__(self):
        return self.value


class BotNotebook:

    def __init__(self):
        self.notebook = NoteBook()


    def handle(self, command: str):
        try:
            if command == "1":
                while True:
                    try:
                        print_green_message("number of note per page")
                        n = int(input(Fore.BLUE + ">>>:"))
                    except ValueError:
                        print_red_message("incorrect number of note, try again")
                        continue
                    else:
                        if self.notebook:
                            get_page(n, self.notebook)
                            break
                        else:
                            print_red_message("notebook empty")
                            break

            elif command == "2":
                title = TitleNotebook().value.strip().lower()

                if title:
                    if self.notebook:
                        for item in self.notebook:
                            if title == item['title']:
                                print_red_message("this title already exists\n" + "  enter command to edit")
                                log("title", f"{title}", "already exists")
                                break
                        else:
                            note = NoteNotebook().value.strip().lower()
                            tag = TagNotebook().value.strip().lower()
                            record = RecordNotebook(title, note, tag)
                            self.notebook.add(record)
                            print_red_message("title", f"{title}", "added")
                            log("title", f"{title}", "added")
                    else:
                        note = NoteNotebook().value.strip().lower()
                        tag = TagNotebook().value.strip().lower()
                        record = RecordNotebook(title, note, tag)
                        self.notebook.add(record)
                        print_red_message("title", f"{title}", "added")
                        log("title", f"{title}", "added")

                else:
                    print_red_message("please enter a title")


            elif command == "3":
                print_green_message("enter the title to find note")
                title = input(Fore.BLUE + ">>>:")
                if title:
                    result = self.notebook.find_note_by_title(title)
                    if result:
                        for res in result:
                            print_note(res)
                    else:
                        print_red_message("not found title")
                else:
                    print_red_message("please enter a word")


            elif command == "4":
                print_green_message("enter the tag to find note")
                tag = input(Fore.BLUE + ">>>:")
                if tag:
                    result = self.notebook.find_note_by_tag(tag)
                    if result:
                        for tag in result:
                            print_note(tag)
                    else:
                        print_red_message("not found title")
                else:
                    print_red_message("please enter a tag")


            elif command == "5":
                all_titles = []
                for key in self.notebook:
                    all_titles.append(key['title'])
                print_all_titles(all_titles)
                print_green_message("enter the title")
                title = input(Fore.BLUE + ">>>:")
                if title in all_titles:
                    print_green_message("enter the parameter to edit")
                    parameter = input(Fore.BLUE + ">>>:")
                    print_green_message("enter new value")
                    new_value = input(Fore.BLUE + ">>>:")
                    self.notebook.edit_note(title, parameter, new_value)
                    print_red_message("note", f"{title}", "edited")
                    log("note", f"{title}", "edited")
                else:
                    log("title not found")
                    print_red_message("title not found")

            elif command == "6":
                all_titles = []
                for key in self.notebook:
                    all_titles.append(key['title'])
                print_all_titles(all_titles)
                print_green_message("enter the title")
                title = input(Fore.BLUE + ">>>:")
                if title in all_titles:
                    self.notebook.delete(title)
                    print_red_message("note", f"{title}", "deleted")
                    log("note", f"{title}", "deleted")
                else:
                    log("title not found")
                    print_red_message("title not found")

            elif command == "7":
                while True:
                    print_yellow_message("are you sure for delete all? (y/n)")
                    clear_all = input(Fore.BLUE + ">>>:")
                    if clear_all == 'y':
                        self.notebook.clear_notebook()
                        print_red_message("notebook cleared")
                        log("notebook cleared")
                        break
                    else:
                        break

            elif command == "8":
                print_green_message("save file name")
                file_name = input(Fore.BLUE + ">>>:").strip()
                if file_name:
                    self.notebook.save(file_name)
                    print_red_message(f"notebook {file_name} saved")
                else:
                    print_red_message("please enter file name")

            elif command == "9":
                print_green_message("load file name")
                file_name = input(Fore.BLUE + ">>>:").strip()
                if file_name:
                    self.notebook.load(file_name)
                    print_red_message(f"notebook {file_name} loaded")
                else:
                    print_red_message("please enter file name")

        except Exception as e:
            print(f'{e} invalid input, try again')


def notebook():
    init()
    file_name = "notebook_save"
    notebot = BotNotebook()
    if os.path.exists(f"{file_name}.bin"):
        notebot.notebook.load(file_name)
    else:
        notebot.notebook.save(file_name)

    while True:
        os.system("cls")
        print_notebook_menu()
        print_white_message("your choose(number)")
        user_input = input(Fore.BLUE + ">>>:")
        if user_input == "10":
            notebot.notebook.save(file_name)
            print_goodbye()
            break

        notebot.handle(user_input)
        input(Fore.MAGENTA + "press Enter to continue")

        if user_input in ["2", "5", "6", "7"]:
            notebot.notebook.save(file_name)


def normalize(name):

    """
    The normalize function takes a string as an argument and returns the same string with all Cyrillic characters
    replaced by their Latin equivalents. The function also replaces spaces, punctuation marks, and other symbols with
    underscores.

    :param name: Pass the name of the file to be normalized
    :return: A string that is the same as the input
    """

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ!#$%&()*+,-/:;<>=?@[]^~{|}'\\`. "
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g",
        "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",
        "_",
        "_", "_", "_", "_", "_", "_", "_", "_", "_")
    TRANS = {}
    CYRILLIC = tuple(CYRILLIC_SYMBOLS)

    for c, l in zip(CYRILLIC, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    if re.search(r'\..{2,5}$', name):
        s_res = re.search(r'\..{2,5}$', name)
        suffix = s_res.group()
        name = name.removesuffix(suffix)
        name = name.translate(TRANS)
        name += suffix
    else:
        name = name.translate(TRANS)
    return name


def move_file(files_pattern, path, el, dst):

    """
    The move_file function takes in three arguments:
        1. files_pattern - a list of regex patterns to match against the file names
        2. path - the directory where all the files are located
        3. dst - destination folder for matched files

    :param files_pattern: Search for the file in the directory
    :param path: Specify the path of the directory where we want to search for files
    :param el: Represent the file name in the path
    :param dst: Specify the destination path
    :return: Nothing
    """

    for doc_pattern in files_pattern:
        if re.search(doc_pattern, el):
            new_el = normalize(el)
            src = os.path.join(path, el)
            dst = os.path.join(dst, new_el)

            try:
                shutil.copy(src, dst)
                print(Fore.WHITE + "  file is copied successfully", el)
                os.remove(src)
                print(Fore.WHITE + "  file is deleted successfully", el)

            except shutil.SameFileError:
                print(Fore.RED + "  source and destination represents the same file", el)
                os.remove(src)
                print(Fore.RED + "  file is deleted successfully", el)

            except PermissionError:
                print(Fore.RED + "  permission denied", el)

            except KeyboardInterrupt:
                print(Fore.RED + "  error occurred while copying file", el)


def move_unknown_file(file_pattern, path, el, dst):

    """
    The move_unknown_file function takes in three arguments:
        1. files_pattern - a list of regular expressions that match the file types we want to keep
        2. path - the directory where all our files are located
        3. el - an element from os.listdir(path) which is a string representing one of the files in path
            (this will be used as part of our source and destination paths)

    :param file_pattern: Determine whether the file is a document or not
    :param path: Specify the path to the folder where we want to move files from
    :param el: Get the name of the file
    :param dst: Specify the destination folder
    :return: Nothing
    """

    for doc_pattern in file_pattern:
        if re.search(doc_pattern, el) is None:
            new_el = normalize(el)
            src = os.path.join(path, el)
            dst = os.path.join(dst, new_el)
            try:
                shutil.copy(src, dst)
                os.remove(src)
                print(Fore.WHITE + "  file is copied successfully")
            except shutil.SameFileError:
                print(Fore.RED + "  source and destination represents the same file")
            except PermissionError:
                print(Fore.RED + "  permission denied")
            except OSError:
                pass


def rec_sort(path):

    """
    The move_unknown_file function takes in three arguments:
     1. path - the directory where all our files are located
    :param path: Specify the directory where all our files are located
    :return: Nothing
    """

    new_folders = ['images',
                   'documents',
                   'audio',
                   'video',
                   'archives',
                   'programs',
                   'unknown']

    for el in new_folders:
        try:
            os.mkdir(path + '\\' + el)
        except FileExistsError:
            print(Fore.RED + f"  file already exists: {el}")
        except OSError:
            print(Fore.RED + f"  error creating folder: {el}")

    dst_doc = os.path.join(path, 'documents')
    dst_img = os.path.join(path, 'images')
    dst_aud = os.path.join(path, 'audio')
    dst_vid = os.path.join(path, 'video')
    dst_arh = os.path.join(path, 'archives')
    dst_prg = os.path.join(path, 'programs')
    dst_un = os.path.join(path, 'unknown')
    el_list = os.listdir(path)

    for folder in new_folders:
        for el in el_list:
            if folder == el:
                el_list.remove(el)
    for el in el_list:
        image_files = ['\.jpeg$', '\.png$', '\.jpg$', '\.svg$', '\.tiff$', '\.tif$', '\.bmp$', '\.gif$']
        video_files = ['\.avi$', '\.mp4$', '\.mov$', '\.mkv$', '\.3gp$', '\.3g2$', '\.mpg$', '\.mpeg$']
        doc_files = ['\.doc$', '\.docx$', '\.txt$', '\.pdf$',
                     '\.xls$', '\.xlsx$', '\.pptx$', '\.mpp$', '\.html$', '\.csv$', '\.bin$', '\.rtf$']
        audio_files = ['\.mp3$', '\.ogg$', '\.wav$', '\.amr$', '\.mid$', '\.midi$', '\.mpa$', '\.wma$']
        arch_files = ['\.zip$', '\.gz$', '\.tar$', '\.7z$', '\.rar$']
        program_files = ['\.exe$', '\.bat$', '\.apk$']
        unknown_files = []
        unknown_files.extend(image_files)
        unknown_files.extend(video_files)
        unknown_files.extend(doc_files)
        unknown_files.extend(audio_files)
        unknown_files.extend(arch_files)
        unknown_files.extend(program_files)

        if not os.path.isdir(path + '\\' + el):
            move_file(image_files, path, el, dst_img)
            move_file(video_files, path, el, dst_vid)
            move_file(doc_files, path, el, dst_doc)
            move_file(audio_files, path, el, dst_aud)
            move_file(arch_files, path, el, dst_arh)
            move_file(program_files, path, el, dst_prg)
            move_unknown_file(unknown_files, path, el, dst_un)
        elif os.path.isdir(path + '\\' + el):
            rec_sort(path + '\\' + el)


def delete_empty_folders(path):

    """
    The delete_empty_folders function takes in one argument:
     1. path - the directory where all our files are located

    :param path: Specify the directory where all our files are located
    :return: Nothing
    """

    for el in os.listdir(path):
        if os.path.isdir(path + '\\' + el):
            try:
                os.rmdir(path + '\\' + el)
                print(Fore.WHITE + "  directory '%s' has been removed successfully" % (path + '\\' + el))
                log("directory '%s' has been removed successfully" % (path + '\\' + el))
                delete_empty_folders(path)
            except OSError:
                log("directory '%s' can not be removed" % (path + '\\' + el))
                delete_empty_folders(path + '\\' + el)


def about_filesort():

    """
    The function print about_filesort.

    :return:  about_filesort
    """

    print(Fore.RED + f" {' ' * 18}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ********************* DESCRIPTION ********************\n',
          Fore.GREEN + ' the script helps to sort files in folders according\n',
                       ' to popular file types as a result, files will be \n',
                       ' moved into folders: <images>, <documents>,\n',
                       ' <audio>, <video>, <archives>, <programs>, <unknown>\n',
                       ' if the folder does\'t contain files of some file\n',
                       ' type then a new folder for this type will not create\n',
          Fore.WHITE + '*******************************************************\n')


def menu_filesort():
    """
    The function print menu_filesort.

    :return:  menu_filesort
    """

    print(Fore.RED + f" {' ' * 4}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ****** FILE SORT ******\n',
          Fore.GREEN + ' 1. about\n',
                       ' 2. run file sort\n',
                       ' 3. exit\n',
          Fore.WHITE + '************************\n')


def filesort():

    """
    The filesort function is a CLI menu that allows the user to sort files in a directory.
    The user can choose from three options:
        1) About - displays information about the function and how it works.
        2) Sort - sorts all files in a given directory into subdirectories based on file type.
            The subdirectories are created if they do not already exist, and empty directories
            are deleted after sorting is complete.
            If an error occurs during sorting, the program will display an error message and return to main menu.

    :return: The filesort function
    """

    init()
    while True:
        os.system('cls')
        menu_filesort()
        print(Fore.GREEN + '  your choose(number)')
        user_input = input(Fore.BLUE + '  your choose(number)>>>: ')

        if user_input == '1':
            os.system('cls')
            about_filesort()
            input(Fore.YELLOW + '  press Enter to continue')

        elif user_input == '2':
            os.system('cls')
            print(Fore.RED + f" {' ' * 7}CLI ASSISTANT BOT")
            print(Fore.WHITE + ' ********** FILE SORT **********')
            print(Fore.GREEN + '  input the file path')
            path = input(Fore.BLUE + '  >>>: ')
            try:
                if os.path.exists(path):
                    rec_sort(path)
                    delete_empty_folders(path)
                    print(Fore.MAGENTA + '\n  sorting completed successfully')
                    input(Fore.YELLOW + '\n  press Enter to continue')
                else:
                    print(Fore.RED + f'\n  path {path} is not found, try again')
                    log(f'path {path} is not found, try again')
                    input(Fore.YELLOW + '\n  press Enter to continue')

            except KeyboardInterrupt:
                input(Fore.YELLOW + '\n  press Enter to continue')
                continue

        elif user_input == '3':
            print_goodbye()
            return 'exit'


def calculate():
    init()
    while True:
        os.system("cls")
        print_calculator_menu()
        print(Fore.WHITE + "your choose(number)")
        user_input = input(Fore.BLUE + ">>>:")
        if user_input == '1':
            print(Fore.GREEN + "enter a mathematical operation")
            operation = input(Fore.BLUE + ">>>:")
            try:
                result = numexpr.evaluate(operation)
                print(Fore.MAGENTA + f"result: {result.round(4)}")
                input(Fore.YELLOW + "press Enter to continue")
            except ValueError:
                print_red_message("incorrect operating, try again!")
                input(Fore.YELLOW + "press Enter to continue")
                continue
            except ZeroDivisionError:
                print_red_message("incorrect operating division by zero, try again!")
                input(Fore.YELLOW + "press Enter to continue")
                continue

        elif user_input == '2':
            print_goodbye()
            break



def main():
    init()
    while True:
        os.system("cls")
        print_main_menu()
        print(Fore.WHITE + "your choose(number)")
        user_input = input(Fore.BLUE + ">>>:")

        if user_input == "1":
            contactbook()

        elif user_input == "2":
            notebook()

        elif user_input == "3":
            filesort()

        elif user_input == "4":
            calculate()

        elif user_input == "5":
            print_goodbye()
            break


if __name__ == '__main__':
    main()
