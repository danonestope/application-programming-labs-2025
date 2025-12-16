import pandas as pd
from PIL import Image
from typing import List, Tuple


class DataProcessor:
    
    @staticmethod
    def create_dataframe_from_csv(csv_file: str) -> pd.DataFrame:
        df = pd.read_csv(csv_file, encoding='utf-8')
        df = df.rename(columns={
            'Абсолютный путь': 'absolute_path',
            'Относительный путь': 'relative_path'
        })
        return df
    
    @staticmethod
    def add_image_area_column(df: pd.DataFrame, area_ranges: List[Tuple[float, float, str]]) -> pd.DataFrame:
        areas = []
        area_categories = []
        
        for _, row in df.iterrows():
            try:
                img = Image.open(row['absolute_path'])
                width, height = img.size
                area = width * height
                category = DataProcessor._get_area_category(area, area_ranges)
                areas.append(area)
                area_categories.append(category)
                
            except Exception:
                areas.append(0)
                area_categories.append("Error")
        
        df['image_area'] = areas
        df['area_category'] = area_categories
        return df
    
    @staticmethod
    def _get_area_category(area: float, area_ranges: List[Tuple[float, float, str]]) -> str:
        for min_val, max_val, category in area_ranges:
            if min_val <= area < max_val:
                return category
        
        if area_ranges:
            # Исправлено: убираем некорректное форматирование
            last_max = area_ranges[-1][1]
            if last_max == float('inf'):
                # Если последний диапазон до бесконечности, возвращаем его название
                return area_ranges[-1][2]
            else:
                # Иначе создаем категорию "больше чем"
                return f">{last_max}"
        
        return "Unknown"
    
    @staticmethod
    def create_default_area_ranges() -> List[Tuple[float, float, str]]:
        return [
            (0, 10000, "0-10k"),
            (10000, 50000, "10k-50k"),
            (50000, 100000, "50k-100k"),
            (100000, 500000, "100k-500k"),
            (500000, 1000000, "500k-1M"),
            (1000000, float('inf'), ">1M")
        ]
    
    @staticmethod
    def parse_custom_ranges(range_str: str) -> List[Tuple[float, float, str]]:
        if not range_str:
            return DataProcessor.create_default_area_ranges()
        
        ranges = []
        parts = range_str.split(',')
        for part in parts:
            if ':' in part:
                range_part, name = part.split(':', 1)
                if '-' in range_part:
                    min_str, max_str = range_part.split('-', 1)
                    min_val = float(min_str.strip())
                    
                    # Обработка бесконечности
                    if max_str.strip().lower() == 'inf':
                        max_val = float('inf')
                    else:
                        max_val = float(max_str.strip())
                    
                    ranges.append((min_val, max_val, name.strip()))
        return ranges
    
    @staticmethod
    def sort_by_area(df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
        return df.sort_values(by='image_area', ascending=ascending)
    
    @staticmethod
    def filter_by_area(df: pd.DataFrame, min_area: float = 0, max_area: float = float('inf')) -> pd.DataFrame:
        return df[(df['image_area'] >= min_area) & (df['image_area'] <= max_area)]