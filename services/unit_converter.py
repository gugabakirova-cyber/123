
def normalize_unit(unit):
    if unit is None:
        return ''
    u = str(unit).strip().lower().replace('.', '')
    aliases = {
        'килограмм': 'кг', 'килограмма': 'кг', 'килограммы': 'кг', 'kg': 'кг', 'kgs': 'кг',
        'грамм': 'г', 'грамма': 'г', 'граммы': 'г', 'гр': 'г', 'g': 'г', 'gr': 'г',
        'литр': 'л', 'литра': 'л', 'литры': 'л', 'l': 'л', 'lt': 'л',
        'миллилитр': 'мл', 'миллилитра': 'мл', 'миллилитры': 'мл', 'ml': 'мл',
        'штука': 'шт', 'штук': 'шт', 'шт': 'шт', 'pcs': 'шт', 'pc': 'шт',
        'порция': 'порция', 'порции': 'порция'
    }
    return aliases.get(u, u)


def convert_quantity(quantity, from_unit, to_unit):
    """Convert quantity from ingredient/input unit into product stock unit."""
    value = float(quantity or 0)
    src = normalize_unit(from_unit)
    dst = normalize_unit(to_unit)

    if not src or not dst or src == dst:
        return value

    if src == 'г' and dst == 'кг':
        return value / 1000
    if src == 'кг' and dst == 'г':
        return value * 1000

    if src == 'мл' and dst == 'л':
        return value / 1000
    if src == 'л' and dst == 'мл':
        return value * 1000

    return value


def format_quantity(value):
    try:
        num = float(value or 0)
    except Exception:
        return str(value)
    if num.is_integer():
        return str(int(num))
    return ('%.3f' % num).rstrip('0').rstrip('.')
