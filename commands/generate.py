from time import perf_counter_ns
from nubia.internal.typing import argument, command
from bitarray import bitarray
from bitarray.util import int2ba, ba2int
from tausworthe import TausworthePRN


SEED_DEFAULT = perf_counter_ns()


@command
@argument("seed", type=int, description="Decimal seed number")
@argument("q", type=int, description="Big position offset")
@argument("r", type=int, description="Little position offset")
@argument("l", type=int, description="Number of bits for decimal conversion")
@argument("cnt", type=int, description="Number of PRNs to generate")
def generate(seed: int = SEED_DEFAULT, q: int = 31, r: int = 5, l: int = 10, cnt: int = 10):
    """
    Generate a PRN using Tausworthe PRN generator
    """

    seed_bin = bitarray()
    if len(seed_bin) < q:
        seed_bin.extend(int2ba(seed))
    if len(seed_bin) > q:
        seed_bin = seed_bin[len(seed_bin) - q:]

    # TODO: Validation

    print("Generating {} PRNs for seed {} with q {} and r {}, using {} bits for each number".format(
        cnt, ba2int(seed_bin), q, r, l))

    res = []
    generator = TausworthePRN(seed_bin, q, r, l)
    for _ in range(cnt):
        res.append(generator.next())

    print("PRNs:\n")

    for prn in res:
        print("{} ".format(prn))
