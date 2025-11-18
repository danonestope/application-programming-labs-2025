<<<<<<< HEAD
import re
from datetime import datetime
=======
def read_profiles():
    """Считывание анкеток"""
    profiles = []
>>>>>>> d0bb973c9edcaef2d54252df723b2cc6f202951f


class Person:
    def __init__(self, last_name, first_name, gender, birth_date, contact, city):
        self.last_name = last_name
        self.first_name = first_name
        self.gender = gender
        self.birth_date = birth_date
        self.contact = contact
        self.city = city

    def get_birth_date_object(self):
        """Преобразует строку даты в объект datetime"""
        try:
            # Пробуем разные разделители
            for separator in ['/', '.', '-']:
                if separator in self.birth_date:
                    day, month, year = map(int, self.birth_date.split(separator))
                    return datetime(year, month, day)
            return None
        except:
            return None

    def calculate_age(self):
        """Вычисляет возраст"""
        birth_date = self.get_birth_date_object()
        if not birth_date:
            return None

        today = datetime.now()
        age = today.year - birth_date.year

        # Проверяем, был ли уже день рождения в этом году
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1

        return age

    def __str__(self):
        age = self.calculate_age()
        age_str = f", {age} лет" if age else ""
        return f"{self.last_name} {self.first_name}{age_str}, {self.city}"


def read_people_from_file(filename):
    """Читает анкеты из файла и возвращает список людей"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
<<<<<<< HEAD

        people = []
        profiles = content.strip().split('\n\n')

        for profile in profiles:
            if not profile.strip():
                continue

            # Ищем данные в формате "Поле: значение"
            data = {}
            for line in profile.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip().lower()] = value.strip()

            # Создаем человека если есть все необходимые поля
            if all(field in data for field in ['фамилия', 'имя', 'дата рождения']):
                person = Person(
                    last_name=data['фамилия'],
                    first_name=data['имя'],
                    gender=data.get('пол', ''),
                    birth_date=data['дата рождения'],
                    contact=data.get('номер телефона или email', ''),
                    city=data.get('город', '')
                )
                people.append(person)

        return people

    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден")
=======
        """Рзделяет на блоки по двойному переносу"""
        profile_blocks = content.split('\n\n')

        for block in profile_blocks:
            lines = block.strip().split('\n') 
            """Разделяет на блоки по переносу строки"""
            if len(lines) >= 6:
                profile = {
                    'surname': lines[1].strip().split(": ")[-1],
                    'name': lines[2].strip().split(": ")[-1],
                    'gender': lines[3].strip().split(": ")[-1],
                    'birth_date': lines[4].strip().split(": ")[-1],
                    'contact': lines[5].strip().split(": ")[-1],
                    'city': lines[6].strip().split(": ")[-1]
                }
                """Сохраняет это в profiles как строку, split'ом выделяем только данные человека"""
                profiles.append(profile)

    except FileNotFoundError:
        print("Ошибка")
>>>>>>> d0bb973c9edcaef2d54252df723b2cc6f202951f
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


<<<<<<< HEAD
def find_oldest_and_youngest(people):
    """Находит самого старого и самого молодого человека"""
    if not people:
        return None, None

    # Фильтруем людей с валидными датами
    people_with_dates = [p for p in people if p.get_birth_date_object()]
=======

def extract_year(birth_date_str):
    """Извлекает год из даты рождения (простая версия)"""
    import re
    year_match = re.search(r'\b(\d{4})\b', birth_date_str)
    if year_match:
        return int(year_match.group(1))
    return None


def find_oldest_and_youngest(profiles):
    """Находит самого старого и самого молодого человека по году рождения"""
    if not profiles:
        return None, None
    valid_profiles = []
    for profile in profiles:
        year = extract_year(profile['birth_date'])
        if year and 1900 <= year <= 2025:  # Простая проверка года
            valid_profiles.append(profile)
>>>>>>> d0bb973c9edcaef2d54252df723b2cc6f202951f

    if not people_with_dates:
        return None, None

<<<<<<< HEAD
    # Сортируем по дате рождения
    people_sorted = sorted(people_with_dates, key=lambda p: p.get_birth_date_object())
=======
    """Сортировка только по дате"""
    sorted_profiles = sorted(valid_profiles, key=lambda x: extract_year(x['birth_date']))
>>>>>>> d0bb973c9edcaef2d54252df723b2cc6f202951f

    oldest = people_sorted[0]  # Первый в отсортированном списке (самый старый)
    youngest = people_sorted[-1]  # Последний в отсортированном списке (самый молодой)

    return oldest, youngest

<<<<<<< HEAD
=======

def print_profile(profile, label):
    """Вывод анкет"""
    print(f"\n{label}:")
    print(f"Фамилия: {profile['surname']}")
    print(f"Имя: {profile['name']}")
    print(f"Пол: {profile['gender']}")
    print(f"Дата рождения: {profile['birth_date']}")
    print(f"Контакт: {profile['contact']}")
    print(f"Город: {profile['city']}")

    """Вычисляем возраст"""
    year = extract_year(profile['birth_date'])
    if year:
        age = 2025 - year
        print(f"Примерный возраст: {age} лет")


>>>>>>> d0bb973c9edcaef2d54252df723b2cc6f202951f
def main():
    filename = "data.txt"

    print(f"Чтение файла: {filename}")
    people = read_people_from_file(filename)

    print(f"Найдено анкет: {len(people)}")

    if not people:
        return

    # Находим самого старого и самого молодого
    oldest, youngest = find_oldest_and_youngest(people)

    print("\n" + "=" * 40)
    print("РЕЗУЛЬТАТЫ:")
    print("=" * 40)

    if oldest and youngest:
        print(f"\nСамый старший человек:")
        print(f"  {oldest}")
        print(f"  Дата рождения: {oldest.birth_date}")


<<<<<<< HEAD
        print(f"\nСамый младший человек:")
        print(f"  {youngest}")
        print(f"  Дата рождения: {youngest.birth_date}")

        if oldest == youngest:
            print("\n  Это один и тот же человек!")
    else:
        print("\nНе удалось определить возраст людей.")


if __name__ == '__main__':
=======
if __name__ == "__main__":
>>>>>>> d0bb973c9edcaef2d54252df723b2cc6f202951f
    main()
