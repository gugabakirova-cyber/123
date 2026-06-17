import re
import pytesseract
from PIL import Image, ImageOps, ImageFilter, ImageEnhance


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path):

    import os
    from PIL import Image, ImageOps, ImageFilter, ImageEnhance
    import pytesseract

    extension = os.path.splitext(image_path)[1].lower()

    if extension == '.pdf':
        from pdf2image import convert_from_path

        pages = convert_from_path(
            image_path,
            dpi=300,
            poppler_path=r"C:\Users\alibi\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"
        )

        image = pages[0]
    else:
        image = Image.open(image_path)

    # Ч/Б режим
    image = image.convert("L")

    # Края режем мягко, чтобы не потерять названия товаров
    width, height = image.size
    left = int(width * 0.03)
    right = int(width * 0.97)
    top = int(height * 0.03)
    bottom = int(height * 0.99)

    image = image.crop((left, top, right, bottom))

    # Увеличиваем изображение
    image = image.resize(
        (
            image.width * 2,
            image.height * 2
        )
    )

    # Мягкая автонастройка контраста
    image = ImageOps.autocontrast(image)

    # Контраст НЕ слишком сильный
    contrast = ImageEnhance.Contrast(image)
    image = contrast.enhance(1.7)

    # Резкость умеренная
    sharpness = ImageEnhance.Sharpness(image)
    image = sharpness.enhance(1.4)

    # Легкое сглаживание шума
    image = image.filter(ImageFilter.MedianFilter(size=3))

    # OCR
    text = pytesseract.image_to_string(
        image,
        lang="rus+eng",
        config="--oem 3 --psm 6 -c preserve_interword_spaces=1"
    )

    return text

def clean_ocr_text(text):

    cleaned=[]

    for line in text.splitlines():

        line=line.strip()

        if not line:
            continue

        # убираем лишние символы OCR, но НЕ удаляем суммы:
        # суммы нужны для автоматической загрузки в Продажи
        line=re.sub(
            r'[|<>{}[\]]',
            '',
            line
        )

        line=re.sub(
            r'\s+',
            ' ',
            line
        )

        cleaned.append(line)

    return '\n'.join(cleaned)


def _money_to_float(value):
    value = str(value or '').replace(' ', '').replace(',', '.')
    try:
        return float(value)
    except ValueError:
        return 0.0


def parse_iiko_report(text):

    items = []

    ignored_words = [
        'терминал',
        'пользователь',
        'текущее',
        'время',
        'наименование',
        'продажи',
        'итого',
        'расход',
        'блюд',
        'сумма',
        'код',
        'к-во'
    ]

    for raw_line in text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        lower = line.lower()

        if any(word in lower for word in ignored_words):
            continue

        # Убираем мусорные символы OCR
        line = re.sub(r'[|•]', ' ', line)
        line = re.sub(r'\s+', ' ', line).strip()

        # Убираем код блюда в начале
        line_without_code = re.sub(r'^\d+\s+', '', line).strip()

        # Ищем количество + сумма в конце строки
        sale_match = re.search(
            r'^(?P<name>.+?)\s+(?P<qty>\d+(?:[,.]\d+)?)\s+(?P<amount>\d{1,3}(?:\s\d{3})*(?:[,.]\d{1,2})?)$',
            line_without_code
        )

        if not sale_match:
            continue

        name = sale_match.group('name').strip()
        quantity = float(sale_match.group('qty').replace(',', '.'))
        total = _money_to_float(sale_match.group('amount'))
        price = round(total / quantity, 2) if quantity else total

        # Если OCR склеил несколько товаров в одну строку,
        # оставляем только последнюю нормальную часть названия
        split_markers = [
            ' Bon Aqua',
            ' Cola',
            ' Fanta',
            ' Piko',
            ' Sprite',
            ' Айс латте',
            ' Американо',
            ' Десерт',
            ' Домашний',
            ' Капучино',
            ' Клубничный',
            ' Кумыс',
            ' Лимон',
            ' Лимонад',
            ' Мохито',
            ' Мороженое',
            ' Морс',
            ' Стафф',
            ' Чай',
            ' Шоколадный',
            ' Шұбат',
            ' Бар'
        ]

        for marker in split_markers:
            if marker in name:
                name = name[name.rfind(marker):].strip()

        # Чистим лишние цифры в начале названия
        name = re.sub(r'^\d+\s+', '', name).strip()

        if name:
            items.append({
                'name': name,
                'quantity': quantity,
                'total': total,
                'price': price
            })

    return items

def extract_text_from_pdf(pdf_path):

    from pypdf import PdfReader

    reader = PdfReader(pdf_path)

    text = ''

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + '\n'

    return text