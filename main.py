import datetime
from pathlib import Path

from word24 import Bip39Check


def get_pattern(pattern_name: str = 'pattern.txt', size: int = 23):
    """Получение слов из паттерна а также их индекса"""
    pattern: Path = Path(pattern_name)
    pattern_lines: list = []
    result_lines: list = []

    with pattern.open('r') as pat:
        pattern_lines = pat.readlines()

    if not pattern_lines:
        raise Exception('Настройте паттерн правильно')

    if len(pattern_lines) != size:
        raise Exception('Размер паттерна превышает/недостает допустимым нормам.')

    for index, row in enumerate(pattern_lines):
        if '-' in row:
            continue
        result_lines.append({'index': index, 'word': row.replace('\n', '')})

    return result_lines


if __name__ == '__main__':
    # Получение слов из паттерна для генерации
    secret_keys = get_pattern()
    used_words = [sec['word'] for sec in secret_keys]

    m = Bip39Check('gen_words.txt')

    # Открытие потоков и запись даты
    common_file = open("common.txt", "a")
    secret_file = open("secret.txt", "a")
    common_file.writelines(f'\n\n\n============={datetime.datetime.now()}==============\n\n')
    secret_file.writelines(f'\n\n\n============={datetime.datetime.now()}==============\n\n')

    repeats: int = int(input('Enter number repeats: '))

    for ii in range(repeats):
        minor_phrase = m.phrase_generate(used_words)
        m.check_size(minor_phrase)
        major_phrase = minor_phrase.copy()

        for index, word in enumerate(major_phrase):
            for sec in secret_keys:
                if index == sec['index']:
                    major_phrase[index] = sec['word']

        m.compute_entropy(major_phrase)
        candidates = m.scan()

        # Добавление 24-го слова
        major_phrase.append(candidates[0])
        minor_phrase.append(candidates[0])

        # Запись результатов в файл
        common_file.writelines(' '.join(minor_phrase) + "\n")
        secret_file.writelines(' '.join(major_phrase) + "\n")

    # Закрытие потоков чтения файла
    common_file.close()
    secret_file.close()
