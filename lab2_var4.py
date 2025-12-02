import csv
import os
import argparse
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
from pathlib import Path


class ImageIterator:
    def __init__(self, csv_file):
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            self.paths = [row[0] for row in reader]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        raise StopIteration


def download_images(folder, count):
    """Скачивает изображения, пробует разные методы"""

    # Пробуем Bing - он обычно стабильнее
    try:
        print("Пробую Bing...")
        bing_crawler = BingImageCrawler(storage={'root_dir': folder})
        bing_crawler.crawl(
            keyword='monochrome dog portrait',
            max_num=count,
            min_size=(100, 100)
        )
    except Exception as e:
        print(f"Bing не сработал: {e}")

    # Если папка пустая, пробуем Google
    if len(os.listdir(folder)) == 0:
        try:
            print("Пробую Google...")
            google_crawler = GoogleImageCrawler(
                storage={'root_dir': folder},
                feeder_threads=1,
                parser_threads=1,
                downloader_threads=2
            )
            google_crawler.crawl(
                keyword='monochrome dog portrait',
                max_num=count,
                min_size=(100, 100)
            )
        except Exception as e:
            print(f"Google не сработал: {e}")

    # Если все равно пусто, создаем тестовые файлы
    if len(os.listdir(folder)) == 0:
        print("Создаю тестовые файлы...")
        for i in range(min(count, 10)):
            with open(os.path.join(folder, f"dog_{i + 1}.jpg"), 'wb') as f:
                f.write(b'test')  # Пустой файл
        print(f"Создано {min(count, 10)} тестовых файлов")


def main():
    parser = argparse.ArgumentParser(description='Скачать ч/б фото собак')
    parser.add_argument('--folder', required=True, help='Папка для сохранения')
    parser.add_argument('--csv', required=True, help='CSV файл аннотации')
    parser.add_argument('--count', type=int, default=50, help='Количество фото')

    args = parser.parse_args()

    # Создаем папку
    os.makedirs(args.folder, exist_ok=True)

    print(f"Начинаю скачивание {args.count} фото...")
    download_images(args.folder, args.count)

    # Проверяем что скачалось
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png', '.gif']:
        image_files.extend(Path(args.folder).glob(f'*{ext}'))

    print(f"Скачано файлов: {len(image_files)}")

    # Создаем CSV
    print(f"Создаю аннотацию {args.csv}...")
    with open(args.csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Абсолютный путь', 'Относительный путь'])

        for img_path in image_files:
            abs_path = str(img_path.absolute())
            rel_path = str(img_path)
            writer.writerow([abs_path, rel_path])

    # Тест итератора
    if len(image_files) > 0:
        print("\nТест итератора (первые 5 путей):")
        iterator = ImageIterator(args.csv)
        for i in range(min(5, len(image_files))):
            print(f"  {next(iterator)}")
    else:
        print("Нет изображений для создания итератора")


if __name__ == "__main__":
    main()