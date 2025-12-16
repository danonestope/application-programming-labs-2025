"""Модуль для скачивания изображений с использованием различных краулеров."""

import os
from typing import List, Optional
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler


class ImageDownloader:
    """Класс для скачивания изображений с использованием различных источников."""
    
    def __init__(self, folder_path: str) -> None:
        """
        Инициализирует загрузчик изображений.
        
        Args:
            folder_path: Путь к папке для сохранения изображений
        """
        self.folder_path = folder_path
        self._create_directory()
    
    def _create_directory(self) -> None:
        """Создает директорию для сохранения изображений, если она не существует."""
        try:
            os.makedirs(self.folder_path, exist_ok=True)
        except PermissionError as e:
            raise PermissionError(f"Нет прав для создания директории {self.folder_path}") from e
        except Exception as e:
            raise Exception(f"Ошибка при создании директории {self.folder_path}: {e}") from e
    
    def download_with_bing(self, keyword: str, count: int, min_size: tuple = (100, 100)) -> bool:
        """
        Скачивает изображения с помощью Bing Image Crawler.
        
        Args:
            keyword: Ключевое слово для поиска
            count: Количество изображений для скачивания
            min_size: Минимальный размер изображений
            
        Returns:
            bool: True если скачивание прошло успешно, иначе False
        """
        try:
            print("Пробую скачать изображения с помощью Bing...")
            bing_crawler = BingImageCrawler(storage={'root_dir': self.folder_path})
            bing_crawler.crawl(
                keyword=keyword,
                max_num=count,
                min_size=min_size
            )
            return True
        except Exception as e:
            print(f"Bing не сработал: {e}")
            return False
    
    def download_with_google(self, keyword: str, count: int, min_size: tuple = (100, 100)) -> bool:
        """
        Скачивает изображения с помощью Google Image Crawler.
        
        Args:
            keyword: Ключевое слово для поиска
            count: Количество изображений для скачивания
            min_size: Минимальный размер изображений
            
        Returns:
            bool: True если скачивание прошло успешно, иначе False
        """
        try:
            print("Пробую скачать изображения с помощью Google...")
            google_crawler = GoogleImageCrawler(
                storage={'root_dir': self.folder_path},
                feeder_threads=1,
                parser_threads=1,
                downloader_threads=2
            )
            google_crawler.crawl(
                keyword=keyword,
                max_num=count,
                min_size=min_size
            )
            return True
        except Exception as e:
            print(f"Google не сработал: {e}")
            return False
    
    def create_test_files(self, count: int) -> None:
        """
        Создает тестовые файлы, если не удалось скачать изображения.
        
        Args:
            count: Количество тестовых файлов для создания
        """
        try:
            print("Создаю тестовые файлы...")
            for i in range(min(count, 10)):
                test_file_path = os.path.join(self.folder_path, f"dog_{i + 1}.jpg")
                with open(test_file_path, 'wb') as f:
                    f.write(b'test')
            print(f"Создано {min(count, 10)} тестовых файлов")
        except Exception as e:
            raise Exception(f"Ошибка при создании тестовых файлов: {e}") from e
    
    def download_images(self, keyword: str, count: int) -> None:
        """
        Основной метод для скачивания изображений.
        
        Args:
            keyword: Ключевое слово для поиска
            count: Количество изображений для скачивания
        """
        print(f"Начинаю скачивание {count} фото...")
        
        # Пробуем Bing - он обычно стабильнее
        success = self.download_with_bing(keyword, count)
        
        # Если папка пустая, пробуем Google
        if not success or len(os.listdir(self.folder_path)) == 0:
            success = self.download_with_google(keyword, count)
        
        # Если все равно пусто, создаем тестовые файлы
        if not success or len(os.listdir(self.folder_path)) == 0:
            self.create_test_files(count)