"""Модуль для визуализации результатов обработки изображений."""

import matplotlib.pyplot as plt
from typing import List, Dict, Any
import numpy as np


class Visualizer:
    """Класс для визуализации результатов обработки изображений."""
    
    @staticmethod
    def show_statistics(statistics: Dict[str, Any]) -> None:
        """Отображает статистику обработки изображений"""
        print("\n" + "=" * 60)
        print("СТАТИСТИКА ОБРАБОТКИ")
        print("=" * 60)
        print(f"Общее количество изображений: {statistics.get('total', 0)}")
        print(f"Успешно обработано: {statistics.get('successful', 0)}")
        print(f"Не удалось обработать: {statistics.get('failed', 0)}")
        print(f"Выходная папка: {statistics.get('output_folder', '')}")
        print("=" * 60)
        
        if statistics.get('successful', 0) > 0 and statistics.get('total', 0) > 0:
            success_rate = (statistics['successful'] / statistics['total']) * 100
            print(f"Процент успешной обработки: {success_rate:.1f}%")
    
    @staticmethod
    def show_detailed_info(images_info: List[Dict[str, Any]]) -> None:
        """Отображает подробную информацию об обработанных изображениях"""
        if not images_info:
            print("Нет информации для отображения")
            return
        
        print("\n" + "=" * 60)
        print("ПОДРОБНАЯ ИНФОРМАЦИЯ ОБ ИЗОБРАЖЕНИЯХ")
        print("=" * 60)
        
        for i, info in enumerate(images_info, 1):
            print(f"\n{i}. {info['filename']}:")
            print(f"   Исходный размер: {info['original'].get('width', 'N/A')}x{info['original'].get('height', 'N/A')}")
            print(f"   Новый размер: {info['rotated'].get('width', 'N/A')}x{info['rotated'].get('height', 'N/A')}")
            print(f"   Сохранен как: {info['output_filename']}")
    
    @staticmethod
    def plot_processing_results(statistics: Dict[str, Any]) -> None:
        """Создает график с результатами обработки"""
        if statistics.get('total', 0) == 0:
            print("Нет данных для построения графика")
            return
        
        labels = ['Успешно', 'Неудачно']
        sizes = [statistics.get('successful', 0), statistics.get('failed', 0)]
        colors = ['#4CAF50', '#F44336']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        
        # Круговая диаграмма
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Результаты обработки изображений')
        ax1.axis('equal')
        
        # Столбчатая диаграмма
        x_pos = np.arange(len(labels))
        bars = ax2.bar(x_pos, sizes, color=colors)
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(labels)
        ax2.set_ylabel('Количество')
        ax2.set_title('Статистика обработки')
        
        # Добавляем значения на столбцы
        for bar, size in zip(bars, sizes):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{size}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()