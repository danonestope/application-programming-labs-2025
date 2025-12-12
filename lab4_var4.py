import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image
import argparse


def create_dataframe_from_csv(csv_file):
    """Создание DataFrame из CSV файла"""
    df = pd.read_csv(csv_file, encoding='utf-8')
    
    # Переименовываем колонки для лучшей читаемости
    df = df.rename(columns={
        'Абсолютный путь': 'absolute_path',
        'Относительный путь': 'relative_path'
    })
    
    return df


def add_image_area_column(df):
    """Добавление колонки с площадью изображений и категориями для гистограммы"""
    
    areas = []
    area_ranges = []
    
    for _, row in df.iterrows():
        try:
            # Пытаемся открыть изображение
            img = Image.open(row['absolute_path'])
            width, height = img.size
            area = width * height
            
            # Определяем категорию площади
            if area < 10000:
                category = "0-10k"
            elif area < 50000:
                category = "10k-50k"
            elif area < 100000:
                category = "50k-100k"
            elif area < 500000:
                category = "100k-500k"
            elif area < 1000000:
                category = "500k-1M"
            else:
                category = ">1M"
            
            areas.append(area)
            area_ranges.append(category)
            
        except Exception as e:
            # Если не удалось открыть изображение, ставим значения по умолчанию
            print(f"Ошибка при обработке {row['absolute_path']}: {e}")
            areas.append(0)
            area_ranges.append("Unknown")
    
    df['image_area'] = areas
    df['area_category'] = area_ranges
    
    return df


def sort_by_area(df, ascending=True):
    """Сортировка DataFrame по площади изображений"""
    return df.sort_values(by='image_area', ascending=ascending)


def filter_by_area(df, min_area=0, max_area=float('inf')):
    """Фильтрация DataFrame по диапазону площадей"""
    return df[(df['image_area'] >= min_area) & (df['image_area'] <= max_area)]


def plot_area_histogram(df):
    """Построение гистограммы распределения площадей"""
    
    # Подготовка данных для гистограммы
    categories = [
        "0-10k", "10k-50k", "50k-100k", 
        "100k-500k", "500k-1M", ">1M", "Unknown"
    ]
    
    # Считаем количество файлов в каждой категории
    counts = []
    for category in categories:
        count = len(df[df['area_category'] == category])
        counts.append(count)
    
    # Создаем график
    plt.figure(figsize=(12, 6))
    
    bars = plt.bar(categories, counts, color='skyblue', edgecolor='black')
    
    # Добавляем значения над столбцами
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(count), ha='center', va='bottom')
    
    # Настройка графика
    plt.title('Распределение изображений по площади (в пикселях)', fontsize=14, fontweight='bold')
    plt.xlabel('Диапазон площади', fontsize=12)
    plt.ylabel('Количество файлов', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    return plt


def main():
    parser = argparse.ArgumentParser(description='Анализ данных изображений')
    parser.add_argument('--csv', required=True, help='CSV файл аннотации')
    parser.add_argument('--output_csv', default='analyzed_data.csv', 
                       help='Файл для сохранения DataFrame')
    parser.add_argument('--output_plot', default='area_distribution.png',
                       help='Файл для сохранения графика')
    
    args = parser.parse_args()
    
    print("1. Создание DataFrame...")
    df = create_dataframe_from_csv(args.csv)
    print(f"   Загружено {len(df)} записей")
    
    print("\n2. Добавление колонки с площадью изображений...")
    df = add_image_area_column(df)
    print(f"   Добавлены колонки: image_area, area_category")
    
    print("\n3. Сортировка данных по площади...")
    sorted_df = sort_by_area(df)
    print(f"   Первые 5 значений площадей: {sorted_df['image_area'].head().tolist()}")
    
    print("\n4. Фильтрация данных (только площади от 50000 до 500000)...")
    filtered_df = filter_by_area(sorted_df, min_area=50000, max_area=500000)
    print(f"   Найдено {len(filtered_df)} файлов в заданном диапазоне")
    
    print("\n5. Построение гистограммы...")
    plt = plot_area_histogram(df)
    
    print("\n6. Сохранение результатов...")
    # Сохраняем DataFrame
    df.to_csv(args.output_csv, index=False, encoding='utf-8')
    print(f"   DataFrame сохранен в {args.output_csv}")
    
    # Сохраняем график
    plt.savefig(args.output_plot, dpi=300, bbox_inches='tight')
    print(f"   График сохранен в {args.output_plot}")
    
    print("\n7. Статистика по категориям:")
    for category in df['area_category'].unique():
        count = len(df[df['area_category'] == category])
        print(f"   {category}: {count} файлов")
    
    # Показываем график
    plt.show()
    
    print("\nАнализ завершен!")


if __name__ == "__main__":
    main()