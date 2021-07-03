# Фукции, генерирующие тестовые данные
def generate_string(n):
    return "x" * n


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'  # 20 популярных китайских иероглифов


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'