__author__ = "VadimTrubay"

from abc import ABC, abstractmethod
from collections import UserList
from colorama import init, Fore, Style
from datetime import datetime, timedelta, date
import numexpr
import os.path
import os
from pathlib import Path
import pickle
import re
import shutil
import sys
from typing import Iterator, List, Dict
from time import sleep


fields_dict_contact = ["firstname", "lastname", "phone", "birthday", "address", "email", "status", "note"]
fields_dict_note = ["title", "note", "tag"]


suff_dict = {'images': ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.ico', '.bmp', '.webp', '.svg'],
             'documents': ['.md', '.epub', '.txt', '.docx', '.doc', '.ods', '.odt', '.dotx', '.docm', '.dox',
                           '.rvg', '.rtf', '.rtfd', '.wpd', '.xls', '.xlsx', '.ppt', '.pptx', '.csv', '.xml'],
             'archives': ['.tar', '.gz', '.zip', '.rar'],
             'audio': ['.aac', '.m4a', '.mp3', '.ogg', '.raw', '.wav', '.wma'],
             'video': ['.avi', '.flv', '.wmv', '.mov', '.mp4', '.webm', '.vob', '.mpg', '.mpeg', '.3gp'],
             'pdf': ['.pdf'],
             'html': ['.html', '.htm', '.xhtml'],
             'exe_msi': ['.exe', '.msi']}


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


def print_filesort_menu():
    print_red_message("{:^42}".format("Filesort"))
    print_white_message(42 * "-" + "")
    print_green_message('1. run filesort')
    print_green_message('2. exit')
    print_white_message(42 * "-" + "")


def print_calculator_menu():
    print_red_message("{:^42}".format("Calculator"))
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


class FileSort:
    @staticmethod
    def normalize(name: str, suffix: str) -> str:
        cyrillic = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        translation = (
            "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
            "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja")

        trans = {}
        for c, l in zip(cyrillic, translation):
            trans[ord(c)] = l
            trans[ord(c.upper())] = l.upper()
        new_name = name.translate(trans)
        new_name = re.sub(r'\W', '_', new_name)
        return new_name + suffix

    @staticmethod
    def unpack_archive(path: Path):
        if path.is_dir():
            for item in path.iterdir():
                if item.name == 'archives':
                    for arch in item.iterdir():
                        name = item / arch.stem
                        name.mkdir(parents=True, exist_ok=True)
                        try:
                            shutil.unpack_archive(arch, name)
                            print_white_message(f"unpack archive: {arch}")
                        except shutil.ReadError:
                            continue

    @staticmethod
    def print_result_sort(path: Path):
        if path.is_dir():
            for item in path.iterdir():
                if item.is_dir():
                    result = [f for f in os.listdir(item)]
                    print_white_message(f"files in category {item.name}: {', '.join(result)}")
                else:
                    continue


    def sort_func(self, path: Path):
        try:
            for item in path.iterdir():
                if item.is_dir():
                    self.sort_func(item)
                    if not list(item.iterdir()):
                        item.rmdir()
                        print_white_message(f"directory {item} removed")
                else:
                    try:
                        new_name = self.normalize(item.stem, item.suffix)
                        for key, value in suff_dict.items():
                            if item.suffix in value:
                                target_dir = path / key
                                target_dir.mkdir(exist_ok=True)
                                shutil.move(item, target_dir / new_name)
                                print_white_message(f"file {new_name} has been successfully moved")
                                break
                        else:
                            target_dir = path / 'unknown'
                            target_dir.mkdir(exist_ok=True)
                            shutil.move(item, target_dir / new_name)
                            print_white_message(f"file {new_name} has been successfully moved")

                    except Exception as e:
                        print(f"error while processing {item}: {e}")

        except FileExistsError as error:
            print(error)


class BotFilesort:

    def __init__(self):
        self.filesort = FileSort()

    def handle(self):
        while True:
            try:
                print_green_message("enter the path to sort")
                path = Path(input(Fore.BLUE + ">>>:"))
                if path.exists():
                    self.filesort.sort_func(path)
                    self.filesort.unpack_archive(path)
                    self.filesort.print_result_sort(path)
                    print_yellow_message('sorting completed successfully')
                    input(Fore.MAGENTA + "press Enter to continue")
                    break

                else:
                    print_red_message(f'path {path} is not found, try again')
                    log(f'path {path} is not found, try again')
                    input(Fore.MAGENTA + "press Enter to continue")
                    continue

            except KeyboardInterrupt:
                input(Fore.MAGENTA + "press Enter to continue")


def filesort():
    init()
    botfilesort = BotFilesort()
    while True:
        os.system('cls')
        print_filesort_menu()
        print_white_message("your choose(number)")
        user_input = input(Fore.BLUE + ">>>:")

        if user_input == "1":
            botfilesort.handle()

        elif user_input == "2":
            print_goodbye()
            break


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
