"""Модуль для генерации CSV аннотаций изображений."""

import csv
import os
from typing import List
from pathlib import Path


class AnnotationGenerator:
    """Класс для создания CSV аннотаций изображений."""
    
    @staticmethod
    def create_annotation_csv(csv_file: str, folder_path: str) -> None:
        """
        Создает CSV файл с аннотацией изображений.
        
        Args:
            csv_file: Путь к CSV файлу для сохранения аннотации
            folder_path: Путь к папке с изображениями
            
        Raises:
            FileNotFoundError: Если папка с изображениями не найдена
            PermissionError: Если нет прав для записи файла
            UnicodeEncodeError: Если ошибка кодировки при записи
        """
        try:
            print(f"Создаю аннотацию {csv_file}...")
            
            # Получаем список файлов изображений
            image_files = AnnotationGenerator._get_image_files(folder_path)
            
            # Создаем CSV файл
            AnnotationGenerator._write_csv_file(csv_file, folder_path, image_files)
            
            print(f"Создан CSV файл с {len(image_files)} записями")
            
        except FileNotFoundError:
            raise
        except PermissionError:
            raise
        except UnicodeEncodeError:
            raise
        except Exception as e:
            raise Exception(f"Ошибка при создании аннотации: {e}") from e
    
    @staticmethod
    def _get_image_files(folder_path: str) -> List[Path]:
        """
        Получает список файлов изображений из указанной папки.
        
        Args:
            folder_path: Путь к папке с изображениями
            
        Returns:
            List[Path]: Список путей к файлам изображений
        """
        image_files: List[Path] = []
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            image_files.extend(Path(folder_path).glob(f'*{ext}'))
            image_files.extend(Path(folder_path).glob(f'*{ext.upper()}'))
        return image_files
    
    @staticmethod
    def _write_csv_file(csv_file: str, folder_path: str, image_files: List[Path]) -> None:
        """
        Записывает данные в CSV файл.
        
        Args:
            csv_file: Путь к CSV файлу
            folder_path: Путь к папке с изображениями
            image_files: Список путей к изображениям
        """
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Абсолютный путь', 'Относительный путь'])
            
            for img_path in image_files:
                abs_path = str(img_path.absolute())
                rel_path = str(img_path.relative_to(folder_path))
                writer.writerow([abs_path, rel_path])