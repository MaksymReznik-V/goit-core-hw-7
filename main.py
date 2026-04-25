from model import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return 'Enter the command argument or correct argument'
        except AttributeError:
            return 'Contact not found'

    return inner


# Розділяємо введені дані на команди та аргументи
def parser_input(user_input):
    if not user_input:
        return None, []

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Додаємо новий контакт до словника
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    if phone:
        record.add_phone(phone)
    return message


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday_date, *_ = args
    record = book.find(name)

    record.add_birthday(birthday_date)
    return 'Birthday add'


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)

    return f"{record.name.value}: {record.birthday.value}"


def birthday(book: AddressBook):
    result_birthday = []
    birthdays = book.get_upcoming_birthdays()

    if not birthdays:
        return 'Birthdays not found'

    for item in birthdays:
        result_birthday.append(
            f"{item['name']}: "
            f"{item['congratulation_date'].strftime('%d.%m.%Y')}"
        )

    return '\n'.join(result_birthday)


# Заміна телефону
@input_error
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    record.edit_phone(old_phone, new_phone)
    return 'Phone edit'


# Виводимо номер телефону потрібного користувача
@input_error
def phone_username(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)

    return ", ".join(p.value for p in record.phones)


# Виводимо адресну книгу
@input_error
def all_contacts(book: AddressBook):
    if not book:
        return 'AddressBook is clean'

    return '\n'.join(
        str(record) for record in book.data.values()
    )


# Основна логіка та вивід даних
def main():
    book = AddressBook()

    print("Welkome to assistent bot!")

    while True:
        user_input = input('Enter you command: ').strip().lower()
        command, *args = parser_input(user_input)

        if command in ['close', 'exit']:
            print('Good bay!')
            break
        elif not command:
            print('Enter command')
            continue

        elif command == 'hello':
            print('How can I help you?')
        elif command == 'add':
            print(add_contact(args, book))
        elif command == 'add-birthday':
            print(add_birthday(args, book))
        elif command == 'show-birthday':
            print(show_birthday(args, book))
        elif command == 'birthdays':
            print(birthday(book))
        elif command == 'phone':
            print(phone_username(args, book))
        elif command == 'change':
            print(change_phone(args, book))
        elif command == 'all':
            print(all_contacts(book))
        else:
            print('Invalid command')


if __name__ == "__main__":
    main() 