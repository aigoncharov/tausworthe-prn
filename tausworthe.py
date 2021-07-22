
from bitarray import bitarray
from bitarray.util import ba2int


class TausworthePRN:
    def __init__(self, seed: bitarray, q: int, r: int, l: int):
        self.seed = seed
        self.seq = seed
        self.q = q
        self.r = r
        self.l = l
        self.base = pow(2, l)

    def next(self):
        next_bits = bitarray([self.__next_bit() for _ in range(self.l)])
        return ba2int(next_bits) / self.base

    def __next_bit(self):
        next_bit = self.seq[-self.q] ^ self.seq[-self.r]
        self.seq.append(next_bit)
        self.seq.pop(0)
        return next_bit
