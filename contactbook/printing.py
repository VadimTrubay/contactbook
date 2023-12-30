from time import sleep
from typing import List, Dict

from colorama import Fore

from contactbook.main import FIELDS_CONTACT, FIELDS_NOTE


def print_main_menu():
    """
    The print_main_menu function prints the main menu of the program.
    """
    print_red_message("{:^42}".format("Menu"))
    print_white_message(42 * "-" + "")
    print_green_message('1. address book')
    print_green_message('2. note book')
    print_green_message('3. file sort')
    print_green_message('4. calculator')
    print_green_message('5. exit')
    print_white_message(42 * "-" + "\n")


def print_contactbook_menu():
    """
    The print_contactbook_menu function prints the menu of the contactbook.
    """
    print_red_message("{:^42}".format("Contactbook"))
    print_white_message(42 * "-" + "")
    print_green_message('1. show all contacts')
    print_green_message('2. add new contact')
    print_green_message('3. find contacts by pattern')
    print_green_message('4. edit contact')
    print_green_message('5. congratulate contacts')
    print_green_message('6. days to birthday')
    print_green_message('7. delete contact')
    print_green_message('8. clear contactbook')
    print_green_message('9. save contactbook')
    print_green_message('10. load contactbook')
    print_green_message('11. exit')
    print_white_message(42 * "-" + "")


def print_notebook_menu():
    """
    The print_notebook_menu function prints the menu for the notebook program.
    """
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
    """
    The print_filesort_menu function prints the menu for the filesort program.
    """
    print_red_message("{:^42}".format("Filesort"))
    print_white_message(42 * "-" + "")
    print_green_message('1. run filesort')
    print_green_message('2. exit')
    print_white_message(42 * "-" + "")


def print_calculator_menu():
    """
    The print_calculator_menu function prints the calculator menu to the console.
    """
    print_red_message("{:^42}".format("Calculator"))
    print_white_message(42 * "-" + "")
    print_green_message('1. run calculator')
    print_green_message('2. exit')
    print_white_message(42 * "-" + "")


def print_red_message(value: str = "", end="\n"):
    """
    The print_red_message function prints a message in red.
    :param value: str: Specify the type of value that will be passed to the function
    :param end: Specify what to print at the end of the output
    """
    print(Fore.RED + f"{value}", end=end)


def print_green_message(value: str = "", end="\n"):
    """
    The print_green_message function prints a green message to the console.
    :param value: str: Specify the value that will be printed to the console
    :param end: Specify what character should be used to end the line
    """
    print(Fore.GREEN + f"{value}", end=end)


def print_white_message(value: str = "", end="\n"):
    """
    The print_white_message function prints a message in white.
    :param value: str: Specify the value that will be printed
    :param end: Specify what character to print at the end of the string
    """
    print(Fore.WHITE + f"{value}", end=end)


def print_blue_message(value: str = "", end="\n"):
    """
    The print_blue_message function prints a message in blue.
    :param value: str: Specify the type of value that will be passed to the function
    :param end: Specify what character should be used to end the line
    """
    print(Fore.BLUE + f"{value}", end=end)


def print_yellow_message(value: str = "", end="\n"):
    """
    The print_yellow_message function prints a yellow message to the console.
    :param value: str: Specify the value that will be printed
    :param end: Specify what character to print at the end of the line
    """
    print(Fore.YELLOW + f"{value}", end=end)


def print_record(value: Dict):
    """
    The print_record function prints a record to the console.
        Args:
            value (dict): A dictionary containing the fields and values of a record.

    :param value: Dict: Specify the type of value that is passed to the function
    :return: The record with the fields and values
    """
    fields_dict = 0
    print_white_message("-" * 25)
    if len(value) == 8:
        fields_dict = FIELDS_CONTACT
    if len(value) == 3:
        fields_dict = FIELDS_NOTE
    for field in fields_dict:
        print_green_message(f"{field}: ", end="")
        print_white_message(f"{value.get(field)}")
    print_white_message("-" * 25)


def print_all_name_contacts(all_contacts: List):
    """
    The print_all_name_contacts function prints all the names of contacts in a sorted list.
        Args:
            all_contacts (List): A list of contact dictionaries.

    :param all_contacts: List: Specify the type of the parameter
    :return: A list of all the names in the contacts
    """
    print_green_message("all names:")
    for contact in sorted(all_contacts):
        print_white_message(contact)


def print_all_titles(all_titles: List):
    """
    The print_all_titles function prints all the titles in a list of dictionaries.
    :param all_titles: List: Specify that the function expects a list of strings
    """
    print_green_message("all titles:")
    for title in sorted(all_titles):
        print_white_message(title)


def print_congratulate(congratulate: Dict):
    """
    The print_congratulate function prints the names of people to congratulate on their birthdays.
    It takes a dictionary as an argument, and iterates through it is keys (dates) and values (names).
    If there are any names in the value list, they are printed with a green date label.
    """
    if congratulate:
        for day, contact in congratulate.items():
            if contact:
                print_green_message(f"{day}: ", end="")
                print_white_message(f"{', '.join(contact)}")


def print_goodbye():
    """
    The print_goodbye function prints a yellow goodbye message to the user.
    """
    print_yellow_message('Good bye!')
    sleep(1)
