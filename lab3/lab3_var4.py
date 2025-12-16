"""Основной модуль программы для поворота изображений."""

import argparse
import sys
from typing import List, Dict, Tuple, Any

# Импорт собственных модулей
from image_processor import ImageProcessor
from file_manager import FileManager
from visualizer import Visualizer


def parse_arguments() -> argparse.Namespace:
    """Парсит аргументы командной строки"""
    parser = argparse.ArgumentParser(
        description='Поворот всех изображений в папке на заданный угол',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        'input_folder',
        type=str,
        help='Путь к папке с изображениями'
    )
    
    parser.add_argument(
        'angle',
        type=float,
        help='Угол поворота в градусах (положительный - против часовой стрелки)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='rotated_images',
        help='Папка для сохранения результатов (по умолчанию: rotated_images)'
    )
    
    parser.add_argument(
        '-p', '--preview',
        action='store_true',
        help='Показать предпросмотр первого изображения с помощью matplotlib'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Подробный вывод информации о каждом изображении'
    )
    
    parser.add_argument(
        '--no-plot',
        action='store_true',
        help='Не показывать графики статистики'
    )
    
    return parser.parse_args()


def process_folder(input_folder: str, output_folder: str, angle: float, 
                  verbose: bool = False) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Обрабатывает все изображения в папке"""
    try:
        # Находим файлы изображений
        image_files = FileManager.find_image_files(input_folder)
        
        if not image_files:
            print("Не найдено изображений в папке!")
            return [], {}
        
        print(f"Найдено изображений: {len(image_files)}")
        print(f"Угол поворота: {angle}°")
        
        # Создаем выходную директорию
        output_path = FileManager.create_output_directory(output_folder)
        print(f"Выходная папка: {output_folder}")
        
        # Обрабатываем изображения
        processed_info = []
        successful = 0
        failed = 0
        
        for image_path in image_files:
            # Формируем имя выходного файла
            name_without_ext = image_path.stem
            extension = image_path.suffix
            output_filename = f"{name_without_ext}_rotated_{int(angle)}deg{extension}"
            output_filepath = output_path / output_filename
            
            # Обрабатываем изображение
            success, info = FileManager.process_single_image(
                image_path, output_filepath, angle, verbose
            )
            
            if success:
                successful += 1
                processed_info.append(info)
            else:
                failed += 1
        
        # Формируем статистику
        statistics: Dict[str, Any] = {
            'total': len(image_files),
            'successful': successful,
            'failed': failed,
            'output_folder': str(output_path.absolute()),
            'angle': angle
        }
        
        return processed_info, statistics
        
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        return [], {}
    except PermissionError as e:
        print(f"Ошибка доступа: {e}")
        return [], {}
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return [], {}


def main() -> None:
    """Основная функция программы"""
    try:
        # Парсинг аргументов
        args = parse_arguments()
        
        # Обработка папки
        images_info, statistics = process_folder(
            args.input_folder, 
            args.output, 
            args.angle, 
            args.verbose
        )
        
        if statistics.get('total', 0) == 0:
            return
        
        # Показ статистики
        Visualizer.show_statistics(statistics)
        
        # Подробная информация (если нужно)
        if args.verbose and images_info:
            Visualizer.show_detailed_info(images_info)
        
        # Предпросмотр первого изображения (если нужно)
        if args.preview and images_info:
            print("\nЗагружаю первое изображение для предпросмотра...")
            image_files = FileManager.find_image_files(args.input_folder)
            if image_files:
                first_image_path = image_files[0]
                original_img = ImageProcessor.load_image(str(first_image_path))
                if original_img is not None:
                    rotated_img = ImageProcessor.rotate_image(original_img, args.angle)
                    ImageProcessor.display_images(original_img, rotated_img, args.angle)
        
        # График статистики (если не отключен)
        if not args.no_plot:
            Visualizer.plot_processing_results(statistics)
        
        print("\nОбработка завершена!")
        
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()