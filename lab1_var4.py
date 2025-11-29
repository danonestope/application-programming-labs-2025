import re
import sys
from datetime import datetime
from typing import List, Optional, Tuple


class Person:
    def __init__(self, last_name: str, first_name: str, gender: str,
                 birth_date: str, contact: str, city: str) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.gender = gender
        self.birth_date = birth_date
        self.contact = contact
        self.city = city

    def get_birth_date_object(self) -> Optional[datetime]:
        """Преобразует строку даты в объект datetime"""
        try:
            # Пробуем разные разделители
            for separator in ['/', '.', '-']:
                if separator in self.birth_date:
                    day, month, year = map(int, self.birth_date.split(separator))
                    return datetime(year, month, day)
            return None
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Неверный формат даты: {self.birth_date}") from e

    def calculate_age(self) -> Optional[int]:
        """Вычисляет возраст"""
        try:
            birth_date = self.get_birth_date_object()
            if not birth_date:
                return None

            today = datetime.now()
            age = today.year - birth_date.year

            # Проверяем, был ли уже день рождения в этом году
            if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                age -= 1

            return age
        except Exception as e:
            raise ValueError(f"Ошибка при вычислении возраста для {self.last_name} {self.first_name}") from e

    def __str__(self) -> str:
        try:
            age = self.calculate_age()
            age_str = f", {age} лет" if age else ""
            return f"{self.last_name} {self.first_name}{age_str}, {self.city}"
        except Exception:
            return f"{self.last_name} {self.first_name}, {self.city} (возраст не определен)"


def read_people_from_file(filename: str) -> List[Person]:
    """Читает анкеты из файла и возвращает список людей"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

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

        if not people:
            raise ValueError(f"В файле {filename} не найдено валидных анкет")

        return people

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл {filename} не найден") from e
    except PermissionError as e:
        raise PermissionError(f"Нет прав для чтения файла {filename}") from e
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"Ошибка кодировки файла {filename}") from e
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла {filename}: {e}") from e


def find_oldest_and_youngest(people: List[Person]) -> Tuple[Optional[Person], Optional[Person]]:
    """Находит самого старого и самого молодого человека"""
    if not people:
        return None, None

    try:
        # Фильтруем людей с валидными датами
        people_with_dates = []
        for person in people:
            try:
                if person.get_birth_date_object():
                    people_with_dates.append(person)
            except ValueError:
                # Пропускаем людей с невалидными датами
                continue

        if not people_with_dates:
            return None, None

        # Сортируем по дате рождения
        people_sorted = sorted(people_with_dates, key=lambda p: p.get_birth_date_object())

        oldest = people_sorted[0]  # Первый в отсортированном списке (самый старый)
        youngest = people_sorted[-1]  # Последный в отсортированном списке (самый молодой)

        return oldest, youngest
    except Exception as e:
        raise Exception("Ошибка при определении самого старого и самого молодого человека") from e


def print_results(oldest: Optional[Person], youngest: Optional[Person], input_file: str) -> None:
    """Печатает результаты в консоль"""
    print(f"Обработан файл: {input_file}")
    print("\n" + "=" * 40)
    print("РЕЗУЛЬТАТЫ:")
    print("=" * 40)

    if oldest and youngest:
        print(f"\nСамый старший человек:")
        print(f"  {oldest}")
        print(f"  Дата рождения: {oldest.birth_date}")

        print(f"\nСамый младший человек:")
        print(f"  {youngest}")
        print(f"  Дата рождения: {youngest.birth_date}")

        if oldest == youngest:
            print("\n⚠️  Это один и тот же человек!")
    else:
        print("\nНе удалось определить возраст людей.")


def main() -> None:
    """Основная функция программы"""
    try:
        # Используем фиксированное имя файла вместо аргументов командной строки
        input_file = "data.txt"

        # Чтение и обработка данных
        people = read_people_from_file(input_file)
        print(f"Найдено анкет: {len(people)}")

        oldest, youngest = find_oldest_and_youngest(people)

        # Вывод результатов в консоль
        print_results(oldest, youngest, input_file)

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        print("Убедитесь, что файл data.txt находится в той же папке, что и программа")
        sys.exit(1)
    except PermissionError as e:
        print(f"Ошибка доступа: {e}")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Ошибка кодировки: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка данных: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()