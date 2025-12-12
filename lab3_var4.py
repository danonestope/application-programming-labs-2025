import cv2
import numpy as np
import argparse
from pathlib import Path


def rotate_image(image, angle):
    """
    Поворачивает изображение на заданный угол вокруг центра.
    """
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


def process_single_image(input_path, output_path, angle, show_preview=False):
    """
    Обрабатывает одно изображение.
    """
    # Загружаем изображение
    img = cv2.imread(input_path)

    if img is None:
        print(f"  ⚠️  Не удалось загрузить: {input_path}")
        return False

    # Получаем информацию об изображении
    img_info = {
        'original_size': img.shape,
        'channels': img.shape[2] if len(img.shape) == 3 else 1,
        'dtype': str(img.dtype)
    }

    # Поворачиваем изображение
    rotated_img = rotate_image(img, angle)

    # Сохраняем результат
    cv2.imwrite(output_path, rotated_img)

    return True, img_info, rotated_img.shape


def process_folder(input_folder, output_folder, angle, preview=False):
    input_path = Path(input_folder)

    if not input_path.exists():
        print(f"Ошибка: папка '{input_folder}' не найдена!")
        return

    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp']

    image_files = []
    for format in supported_formats:
        image_files.extend(list(input_path.glob(f'*{format}')))
        image_files.extend(list(input_path.glob(f'*{format.upper()}')))

    if not image_files:
        print("Не найдено изображений в папке!")
        return

    successful = 0
    failed = 0

    for i, image_path in enumerate(image_files, 1):

        name_without_ext = image_path.stem
        extension = image_path.suffix

        output_filename = f"{name_without_ext}_rotated_{int(angle)}deg{extension}"
        output_filepath = output_path / output_filename


        try:
            # Обрабатываем изображение
            success, img_info, new_size = process_single_image(
                str(image_path),
                str(output_filepath),
                angle,
                show_preview=False
            )

            if success:
                successful += 1
            else:
                failed += 1

        except Exception as e:
            print(f"  ✗ Ошибка: {str(e)}")
            failed += 1

    print("\n" + "=" * 60)
    print("СТАТИСТИКА ОБРАБОТКИ")
    print("=" * 60)
    print(f"Успешно обработано: {successful}")
    print(f"Не удалось обработать: {failed}")
    print(f"Выходная папка: {output_folder}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='Поворот всех изображений в папке на заданный угол'
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
        help='Показать предпросмотр результатов'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Подробный вывод информации'
    )

    # Парсим аргументы
    args = parser.parse_args()

    # Обрабатываем папку
    process_folder(args.input_folder, args.output, args.angle, args.preview)


if __name__ == "__main__":
    main()