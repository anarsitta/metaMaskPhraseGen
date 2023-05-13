import datetime
from pathlib import Path

from word24 import Bip39Check


def get_pattern(pattern_name: str = 'pattern.txt', size: int = 23):
    """get words and index from pattern"""
    pattern: Path = Path(pattern_name)
    pattern_lines: list = []
    result_lines: list = []

    with pattern.open('r') as f_pattern:
        pattern_lines = f_pattern.readlines()

    if not pattern_lines:
        raise Exception('Adjust the drawing correctly')

    if len(pattern_lines) != size:
        raise Exception('The size of the pattern does not meet the required standards..')

    for i, row in enumerate(pattern_lines):
        if '-' in row:
            continue
        result_lines.append({'index': i, 'word': row.replace('\n', '')})
    return result_lines


if __name__ == '__main__':
    # get words for generated
    secret_keys = get_pattern()
    used_words = [sec['word'] for sec in secret_keys]

    m = Bip39Check('generate.txt')

    # open writers and write date
    file_without_replace = open("file_without_replace.txt", "a")
    file_with_replace = open("file_with_replace.txt", "a")
    file_without_replace.writelines(f'\n\n\n============={datetime.datetime.now()}==============\n\n')
    file_with_replace.writelines(f'\n\n\n============={datetime.datetime.now()}==============\n\n')

    # entering phrase col
    repeats: int = int(input('Enter number repeats: '))

    for ii in range(repeats):
        phrase_without_replace = m.phrase_generate(used_words)
        m.check_size(phrase_without_replace)
        phrase_with_replace = phrase_without_replace.copy()

        for i, word in enumerate(phrase_with_replace):
            for sec in secret_keys:
                if i == sec['index']:
                    phrase_with_replace[i] = sec['word']

        m.compute_entropy(phrase_with_replace)
        candidates = m.scan()

        # adding 24-th word
        phrase_with_replace.append(candidates[0])
        phrase_without_replace.append(candidates[0])

        # write result in files
        file_without_replace.writelines(' '.join(phrase_without_replace) + "\n")
        file_with_replace.writelines(' '.join(phrase_with_replace) + "\n")

    # closing file writers
    file_without_replace.close()
    file_with_replace.close()
