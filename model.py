from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value.isalpha():
            raise ValueError("Incorrect name")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit():
            raise ValueError("Incorrect phone number")
        if len(value) != 10:
            raise ValueError("The phone number has 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            date_to_string = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError('Invalid date')
        super().__init__(date_to_string)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        self.phones.remove(self.find_phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str):
        if not self.find_phone(old_phone):
            raise ValueError("Phone not found")
        else:
            self.add_phone(new_phone)
            self.remove_phone(old_phone)

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)

        if self.birthday:
            birthday_day = self.birthday.value.strftime('%d.%m.%Y')
        else:
            birthday_day = 'No date'

        return (f"Contact name: "
                f"{self.name.value}, "
                f"Phones: {phones}, "
                f"Birthday: {birthday_day}"
                )


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name, None)

    def delete(self, name: str):
        name = name.strip()
        if name in self.data:
            del self.data[name]

    def _adjust_for_weekend(self, birthday):
        if birthday.weekday() == 5:
            return birthday + timedelta(days=2)

        if birthday.weekday() == 6:
            return birthday + timedelta(days=1)

        return birthday


    def get_upcoming_birthdays(self, days = 7):
        upcoming_birthdays = []
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
               birthday_this_year = birthday.replace(year=today.year + 1)

            if 0 <= (birthday_this_year - today).days <= days:
                congratulation_date_str = self._adjust_for_weekend(birthday_this_year)
                upcoming_birthdays.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congratulation_date_str
                    }
                )

        return upcoming_birthdays









