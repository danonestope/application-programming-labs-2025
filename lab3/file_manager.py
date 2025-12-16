"""Модуль для управления файлами и директориями с изображениями."""

from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any


class FileManager:
    """Класс для работы с файлами и директориями изображений."""
    
    # Поддерживаемые форматы изображений
    SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', 
                         '.JPG', '.JPEG', '.PNG', '.BMP', '.TIFF', '.TIF', '.WEBP']
    
    @staticmethod
    def find_image_files(folder_path: str) -> List[Path]:
        """Находит все файлы изображений в указанной папке"""
        input_path = Path(folder_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Папка '{folder_path}' не найдена!")
        
        if not input_path.is_dir():
            raise ValueError(f"'{folder_path}' не является папкой!")
        
        try:
            image_files = []
            for format_ext in FileManager.SUPPORTED_FORMATS:
                image_files.extend(input_path.glob(f'*{format_ext}'))
            
            return sorted(image_files)  # Сортируем для предскатуемого порядка
            
        except PermissionError as e:
            raise PermissionError(f"Нет прав доступа к папке '{folder_path}'") from e
    
    @staticmethod
    def create_output_directory(output_folder: str) -> Path:
        """Создает выходную директорию если она не существует"""
        try:
            output_path = Path(output_folder)
            output_path.mkdir(parents=True, exist_ok=True)
            return output_path
        except PermissionError as e:
            raise PermissionError(f"Нет прав для создания директории '{output_folder}'") from e
    
    @staticmethod
    def process_single_image(input_path: Path, output_path: Path, 
                           angle: float, verbose: bool = False) -> Tuple[bool, Dict[str, Any]]:
        """Обрабатывает одно изображение"""
        try:
            if verbose:
                print(f"  Обработка: {input_path.name}")
            
            # Локальный импорт для избежания циклической зависимости
            from image_processor import ImageProcessor
            
            # Загружаем изображение
            img = ImageProcessor.load_image(str(input_path))
            if img is None:
                print(f"  ⚠️  Не удалось загрузить: {input_path.name}")
                return False, {}
            
            # Получаем информацию об исходном изображении
            img_info = ImageProcessor.get_image_info(img)
            
            # Поворачиваем изображение
            rotated_img = ImageProcessor.rotate_image(img, angle)
            
            # Получаем информацию о повернутом изображении
            rotated_info = ImageProcessor.get_image_info(rotated_img)
            
            # Сохраняем результат
            success = ImageProcessor.save_image(rotated_img, str(output_path))
            
            if not success:
                print(f"  ✗ Не удалось сохранить: {output_path.name}")
                return False, {}
            
            # Собираем полную информацию
            full_info: Dict[str, Any] = {
                'filename': input_path.name,
                'original': img_info,
                'rotated': rotated_info,
                'output_filename': output_path.name
            }
            
            return True, full_info
            
        except Exception as e:
            print(f"  ✗ Ошибка при обработке {input_path.name}: {str(e)}")
            return False, {}