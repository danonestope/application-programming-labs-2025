import argparse
import sys
import matplotlib.pyplot as plt  # Добавлен импорт plt
from typing import List, Tuple

from data_processor import DataProcessor
from visualizer import Visualizer


def parse_arguments():
    parser = argparse.ArgumentParser(description='Анализ данных изображений')
    
    parser.add_argument('--csv', required=True, help='CSV файл аннотации')
    parser.add_argument('--ranges', default='', help='Диапазоны: "0-10000:Small,10000-50000:Medium,..."')
    parser.add_argument('--min-area', type=float, default=0, help='Минимальная площадь')
    parser.add_argument('--max-area', type=float, default=float('inf'), help='Максимальная площадь')
    parser.add_argument('--output-csv', default='analyzed_data.csv', help='Файл для DataFrame')
    parser.add_argument('--output-plot', default='area_distribution.png', help='Файл для графика')
    parser.add_argument('--show-plot', action='store_true', help='Показать график')
    
    return parser.parse_args()


def main():
    try:
        args = parse_arguments()
        
        print("1. Загрузка данных...")
        df = DataProcessor.create_dataframe_from_csv(args.csv)
        print(f"   Загружено {len(df)} записей")
        
        print("\n2. Настройка диапазонов...")
        if args.ranges:
            area_ranges = DataProcessor.parse_custom_ranges(args.ranges)
            print("   Используются пользовательские диапазоны")
        else:
            area_ranges = DataProcessor.create_default_area_ranges()
            print("   Используются диапазоны по умолчанию")
        
        print("\n3. Анализ изображений...")
        df = DataProcessor.add_image_area_column(df, area_ranges)
        
        print("\n4. Сортировка данных...")
        sorted_df = DataProcessor.sort_by_area(df, ascending=False)
        
        print("\n5. Фильтрация данных...")
        filtered_df = DataProcessor.filter_by_area(sorted_df, args.min_area, args.max_area)
        
        print("\n6. Расчет статистики...")
        Visualizer.display_statistics(filtered_df)
        
        print("\n7. Создание графика...")
        fig = Visualizer.plot_area_histogram(filtered_df, area_ranges)
        
        print("\n8. Сохранение результатов...")
        filtered_df.to_csv(args.output_csv, index=False, encoding='utf-8')
        print(f"   DataFrame сохранен в {args.output_csv}")
        
        fig.savefig(args.output_plot, dpi=300, bbox_inches='tight')
        print(f"   График сохранен в {args.output_plot}")
        
        if args.show_plot:
            plt.show()
        
        print("\nАнализ завершен!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()