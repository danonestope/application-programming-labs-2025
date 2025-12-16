"""Модуль для работы с итератором изображений."""

import csv
from typing import List, Iterator
from pathlib import Path


class ImageIterator:
    """Итератор для перебора путей к изображениям из CSV файла."""
    
    def __init__(self, csv_file: str) -> None:
        """
        Инициализирует итератор изображений.
        
        Args:
            csv_file: Путь к CSV файлу с аннотацией изображений
            
        Raises:
            FileNotFoundError: Если файл не найден
            PermissionError: Если нет прав для чтения файла
            UnicodeDecodeError: Если ошибка кодировки файла
            csv.Error: Если ошибка при чтении CSV файла
        """
        self.csv_file = csv_file
        self.index = 0
        self.paths: List[str] = []
        
        try:
            self._load_paths_from_csv()
        except FileNotFoundError:
            raise
        except PermissionError:
            raise
        except UnicodeDecodeError:
            raise
        except csv.Error as e:
            raise csv.Error(f"Ошибка при чтении CSV файла {csv_file}: {e}") from e
        except Exception as e:
            raise Exception(f"Неожиданная ошибка при инициализации итератора: {e}") from e
    
    def _load_paths_from_csv(self) -> None:
        """Загружает пути из CSV файла."""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Пропускаем заголовок
                self.paths = [row[0] for row in reader]
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Файл {self.csv_file} не найден") from e
        except PermissionError as e:
            raise PermissionError(f"Нет прав для чтения файла {self.csv_file}") from e
        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(f"Ошибка кодировки файла {self.csv_file}") from e
    
    def __iter__(self) -> Iterator[str]:
        """
        Возвращает итератор.
        
        Returns:
            Iterator[str]: Итератор по путям к изображениям
        """
        return self
    
    def __next__(self) -> str:
        """
        Возвращает следующий путь к изображению.
        
        Returns:
            str: Путь к следующему изображению
            
        Raises:
            StopIteration: Когда пути закончились
        """
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        raise StopIteration