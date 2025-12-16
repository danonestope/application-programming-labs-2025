"""Основной модуль программы для скачивания и обработки изображений собак."""

import argparse
import sys
from pathlib import Path

# Импорт собственных модулей
from image_downloader import ImageDownloader
from annotation_generator import AnnotationGenerator
from image_iterator import ImageIterator


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.
    
    Returns:
        argparse.Namespace: Объект с аргументами
    """
    parser = argparse.ArgumentParser(description='Скачать ч/б фото собак')
    parser.add_argument('--folder', required=True, help='Папка для сохранения')
    parser.add_argument('--csv', required=True, help='CSV файл аннотации')
    parser.add_argument('--count', type=int, default=50, help='Количество фото')
    return parser.parse_args()


def test_iterator(csv_file: str, max_items: int = 5) -> None:
    """
    Тестирует работу итератора изображений.
    
    Args:
        csv_file: Путь к CSV файлу с аннотацией
        max_items: Максимальное количество элементов для вывода
    """
    try:
        print("\nТест итератора (первые несколько путей):")
        iterator = ImageIterator(csv_file)
        
        for i, path in enumerate(iterator):
            if i >= max_items:
                break
            print(f"  {path}")
            
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Ошибка при тестировании итератора: {e}")


def main() -> None:
    """Основная функция программы."""
    try:
        # Парсинг аргументов
        args = parse_arguments()
        
        # Скачивание изображений
        downloader = ImageDownloader(args.folder)
        downloader.download_images('dogs on black and white background', args.count)
        
        # Создание аннотации
        AnnotationGenerator.create_annotation_csv(args.csv, args.folder)
        
        # Проверка количества скачанных файлов
        image_files = list(Path(args.folder).glob('*.*'))
        print(f"Скачано файлов: {len(image_files)}")
        
        # Тест итератора
        test_iterator(args.csv)
        
        print("\nПрограмма успешно завершена!")
        
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"Ошибка доступа: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()