"""Модуль для обработки и поворота изображений."""

import cv2
import numpy as np
from typing import Tuple, Optional, Dict, Any
import matplotlib.pyplot as plt


class ImageProcessor:
    """Класс для обработки и поворота изображений."""
    
    @staticmethod
    def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
        """Поворачивает изображение на заданный угол вокруг центра"""
        if image is None or image.size == 0:
            raise ValueError("Пустое или некорректное изображение")
        
        try:
            # Получаем размеры изображения
            (h, w) = image.shape[:2]
            
            # Вычисляем центр изображения
            center = (w // 2, h // 2)
            
            # Получаем матрицу поворота
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            
            # Вычисляем новые размеры изображения после поворота
            cos = np.abs(rotation_matrix[0, 0])
            sin = np.abs(rotation_matrix[0, 1])
            
            new_w = int((h * sin) + (w * cos))
            new_h = int((h * cos) + (w * sin))
            
            # Корректируем матрицу поворота с учетом новых размеров
            rotation_matrix[0, 2] += (new_w / 2) - center[0]
            rotation_matrix[1, 2] += (new_h / 2) - center[1]
            
            # Применяем аффинное преобразование
            rotated_image = cv2.warpAffine(image, rotation_matrix, (new_w, new_h))
            
            return rotated_image
            
        except Exception as e:
            raise ValueError(f"Ошибка при повороте изображения: {e}") from e
    
    @staticmethod
    def load_image(image_path: str) -> Optional[np.ndarray]:
        """Загружает изображение из файла"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None
            # Конвертируем из BGR в RGB для отображения в matplotlib
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img_rgb
        except Exception as e:
            print(f"Ошибка при загрузке изображения {image_path}: {e}")
            return None
    
    @staticmethod
    def save_image(image: np.ndarray, output_path: str) -> bool:
        """Сохраняет изображение в файл"""
        try:
            # Конвертируем обратно в BGR для OpenCV
            img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            success = cv2.imwrite(output_path, img_bgr)
            return success
        except Exception as e:
            print(f"Ошибка при сохранении изображения {output_path}: {e}")
            return False
    
    @staticmethod
    def get_image_info(image: np.ndarray) -> Dict[str, Any]:
        """Получает информацию об изображении"""
        if image is None:
            return {}
        
        return {
            'original_size': image.shape,
            'height': image.shape[0],
            'width': image.shape[1],
            'channels': image.shape[2] if len(image.shape) == 3 else 1,
            'dtype': str(image.dtype),
            'min_value': float(image.min()),
            'max_value': float(image.max()),
            'mean_value': float(image.mean())
        }
    
    @staticmethod
    def display_images(original: np.ndarray, rotated: np.ndarray, 
                      angle: float, figsize: Tuple[int, int] = (12, 6)) -> None:
        """Отображает исходное и повернутое изображения с помощью matplotlib"""
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Отображаем исходное изображение
        axes[0].imshow(original)
        axes[0].set_title('Исходное изображение')
        axes[0].axis('off')
        
        # Добавляем информацию об исходном изображении
        orig_info = f"Размер: {original.shape[1]}x{original.shape[0]}\n"
        orig_info += f"Каналы: {original.shape[2] if len(original.shape) == 3 else 1}"
        axes[0].text(0.5, -0.1, orig_info, transform=axes[0].transAxes,
                    ha='center', va='top', fontsize=10)
        
        # Отображаем повернутое изображение
        axes[1].imshow(rotated)
        axes[1].set_title(f'Повернуто на {angle}°')
        axes[1].axis('off')
        
        # Добавляем информацию о повернутом изображении
        rotated_info = f"Размер: {rotated.shape[1]}x{rotated.shape[0]}\n"
        rotated_info += f"Каналы: {rotated.shape[2] if len(rotated.shape) == 3 else 1}"
        axes[1].text(0.5, -0.1, rotated_info, transform=axes[1].transAxes,
                    ha='center', va='top', fontsize=10)
        
        plt.tight_layout()
        plt.show()