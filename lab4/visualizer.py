import matplotlib.pyplot as plt
from typing import List, Tuple
import pandas as pd


class Visualizer:
    
    @staticmethod
    def plot_area_histogram(df: pd.DataFrame, area_ranges: List[Tuple[float, float, str]]) -> plt.Figure:
        # Получаем все категории из диапазонов
        categories = [category for _, _, category in area_ranges]
        
        # Добавляем Error только если есть ошибки
        error_count = len(df[df['area_category'] == "Error"])
        if error_count > 0:
            categories.append("Error")
        
        counts = []
        for category in categories:
            count = len(df[df['area_category'] == category])
            counts.append(count)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(categories, counts, color='skyblue', edgecolor='black')
        
        # Используем разные цвета для Error
        for i, (bar, category) in enumerate(zip(bars, categories)):
            if category == "Error":
                bar.set_color('lightcoral')
        
        for bar, count in zip(bars, counts):
            if count > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                       str(count), ha='center', va='bottom')
        
        ax.set_title('Распределение изображений по площади')
        ax.set_xlabel('Диапазон площади')
        ax.set_ylabel('Количество файлов')
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def display_statistics(df: pd.DataFrame) -> None:
        print("\nСтатистика:")
        print(f"  Всего файлов: {len(df)}")
        
        if 'image_area' in df.columns:
            valid_df = df[df['area_category'] != 'Error']
            error_count = len(df) - len(valid_df)
            
            print(f"  Валидных изображений: {len(valid_df)}")
            print(f"  Ошибочных файлов: {error_count}")
            
            if len(valid_df) > 0:
                print(f"  Средняя площадь: {valid_df['image_area'].mean():,.0f}")
                print(f"  Минимальная площадь: {valid_df['image_area'].min():,.0f}")
                print(f"  Максимальная площадь: {valid_df['image_area'].max():,.0f}")
            else:
                print("  Нет валидных изображений для статистики")