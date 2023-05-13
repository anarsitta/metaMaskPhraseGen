import hashlib
import random
import sys
from pathlib import Path


class Bip39Check(object):
    def __init__(self, filename: str):
        self.radix: int = 2048
        self.word_dict: dict = {}
        self.word_list_bip: list = []
        self.word_list_gen: list = []
        self.counter: int = 0
        self.gen_radix: int = 0

        # Заполнение списка слов bip39
        words_path_bip: Path = Path('wordlist', 'bip39.txt')
        with words_path_bip.open('r') as file:
            for w in file.readlines():
                word = w.strip() if sys.version < '3' else w.strip()
                self.word_dict[word] = self.counter
                self.word_list_bip.append(word)
                self.counter += 1

        # Заполнение списка создания фразы
        words_path_gen: Path = Path('wordlist', filename)
        with words_path_gen.open('r') as file:
            for w in file.readlines():
                word = w.strip() if sys.version < '3' else w.strip()
                self.word_list_gen.append(word)
                self.gen_radix += 1

        if len(self.word_dict) != self.radix:
            raise ValueError('Expecting %d words, not %d', self.radix, len(self.word_dict))

    def phrase_generate(self, used_words: list, size: int = 23):
        """generates a phrase of a certain length"""
        new_phrase: list = []
        index_phrase: list = []
        used_word: list = used_words

        while len(index_phrase) != size:
            word_index: int = random.randrange(self.gen_radix)
            if word_index in index_phrase:
                continue
            if self.word_list_gen[word_index] in used_word:
                continue
            new_phrase.append(self.word_list_gen[word_index])
            index_phrase.append(word_index)

        return new_phrase

    def check_size(self, phrase: list, size: int = 23):
        """check size phrase"""
        self.size = len(phrase) + 1
        if self.size != size + 1:
            raise ValueError('Expecting 23 words')

    def compute_entropy(self, phrase):
        """computed entropy"""
        self.entropy = 0
        for w in phrase:
            idx = self.word_dict[w]
            self.entropy = (self.entropy << 11) + idx
        return self.entropy

    def scan(self):
        checksum_bits = self.size // 3
        entropy_len = (self.size * 11 - checksum_bits) // 8
        entropy_to_fill = 11 - checksum_bits
        entropy_base = self.entropy << (entropy_to_fill)
        couldbe = []

        for i in range(0, 2 ** entropy_to_fill):
            entropy_candidate = entropy_base | i
            binary = bin(entropy_candidate)[2:]
            entropy_str = entropy_candidate.to_bytes((entropy_candidate.bit_length() + 7) // 8, 'big')
            hash = (hashlib.sha256(entropy_str).digest()[0])
            checksum = hash >> (8 - checksum_bits)
            final_word_idx = (i << checksum_bits) + checksum
            checkword = self.word_list_bip[final_word_idx]
            couldbe.append(checkword)
        return couldbe


if __name__ == '__main__':
    m = Bip39Check('gew_words.txt')
    used_words = ['art']
    phrase = m.phrase_generate(used_words)
    print('phrase: ', phrase)
    print(len(phrase))
    m.check_size(phrase)
    m.compute_entropy(phrase)
    candidates = m.scan()
    print('result: ', candidates)
