from model import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return 'Give me true name and phone please.'
        except KeyError:
            return 'User is not found'
        except IndexError:
            return 'Enter the argument for the command'

    return inner


# Розділяємо введені дані на команди та аргументи
def parser_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Додаємо новий контакт до словника
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

    if record is None:
        raise KeyError('Contact not found')

    record.add_birthday(birthday_date)
    return 'Birthday add'


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError('Contact not found')

    if record.birthday is None:
        raise ValueError('Birthday not found')

    return f"{record.name.value}: {record.birthday.value.strftime('%d.%m.%Y')}"


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


# Змінюємо телефон замінючи значення у парі ключ-значення при співпадінні з ключа з аргументом
@input_error
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError ('Name not found')

    for p in record.phones:
        if p.value == old_phone:
            p.value = new_phone
            return 'New phone save'

    raise ValueError('Phone not found')


# Виводимо потрібний номер телефону при співпадінні ключа зі значенням агрументу
@input_error
def phone_username(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError('Contact not found')

    return ", ".join(p.value for p in record.phones)


# Виводимо весь список доданих
def all_contacts(book: AddressBook):
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

        elif command == 'hello':
            print('How can I help you?')
        elif command == 'add':
            print(add_contact(args, book))
        elif command == 'add-birthday':
            print(add_birthday(args, book))
        elif command == 'show-birthday':
            print(show_birthday(args, book))
        elif command == 'birthday':
            print(birthday(book))
        elif command == 'phone':
            print(f'Telephone {phone_username(args, book)}')
        elif command == 'change':
            print(change_phone(args, book))
        elif command == 'all':
            print(all_contacts(book))
        else:
            print('Invalid command')


if __name__ == "__main__":
    main() 