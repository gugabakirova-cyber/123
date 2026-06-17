import re


def _money_to_float(value):
    value = str(value or '').replace(' ', '').replace(',', '.')
    try:
        return float(value)
    except ValueError:
        return 0.0


def clean_invoice_text(text):
    text = text.replace('\r', '\n')

    start_markers = [
        '№ Код Наименование',
        'Код Наименование',
        'Наименование Кол-во',
        'Наименование'
    ]

    end_markers = [
        'Итого:',
        'Всего наименований',
        'Всего к оплате'
    ]

    start = -1

    for marker in start_markers:
        index = text.find(marker)
        if index != -1:
            start = index
            break

    if start != -1:
        text = text[start:]

    end = -1

    for marker in end_markers:
        index = text.find(marker)
        if index != -1:
            end = index
            break

    if end != -1:
        text = text[:end]

    return text.strip()


def parse_invoice_text(text):
    """Парсит накладную из OCR/PDF.

    Поддерживает два частых варианта:
    1) код + название на одной строке, количество/цена на следующей;
    2) табличная строка: название + количество + ед. + цена + сумма.
    """
    items = []

    lines = [
        re.sub(r'\s+', ' ', line.strip())
        for line in text.splitlines()
        if line.strip()
    ]

    current_name = None

    for line in lines:
        lower = line.lower()
        if any(word in lower for word in ['наименование', 'кол-во', 'цена', 'сумма', 'ед.']):
            continue

        # Вариант 2: ПЮРЕ ... 5,000 шт 3 255,00 16 275,00
        row_match = re.match(
            r'^(?P<name>.+?)\s+(?P<qty>\d+(?:[,.]\d+)?)\s+(?P<unit>шт|кг|л|мл|гр|г|уп)\s+(?P<price>[\d\s]+[,.]\d{2})(?:\s+(?P<sum>[\d\s]+[,.]\d{2}))?$',
            line,
            re.IGNORECASE
        )
        if row_match:
            items.append({
                'name': row_match.group('name').strip(),
                'quantity': float(row_match.group('qty').replace(',', '.')),
                'unit': row_match.group('unit'),
                'price': _money_to_float(row_match.group('price'))
            })
            current_name = None
            continue

        # Вариант 1: 1 00000000057 ПЮРЕ ФРУКТОВОЕ...
        start_match = re.match(r'^\d+\s+\d{5,}\s+(.+)$', line)
        if start_match:
            current_name = start_match.group(1).strip()
            continue

        if current_name:
            # 5,000 шт 3 255,00 16 275,00
            value_match = re.match(
                r'^(\d+(?:[,.]\d+)?)\s+(шт|кг|л|мл|гр|г|уп)\s+([\d\s]+[,.]\d{2})',
                line,
                re.IGNORECASE
            )

            if value_match:
                items.append({
                    'name': current_name,
                    'quantity': float(value_match.group(1).replace(',', '.')),
                    'unit': value_match.group(2),
                    'price': _money_to_float(value_match.group(3))
                })
                current_name = None
            else:
                current_name += ' ' + line

    return items
