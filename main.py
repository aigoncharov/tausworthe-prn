#!/usr/bin/env python3

import sys
from tausworthe import TausworthePRN
from nubia import Nubia
from nubia import command, argument
import time
from bitarray import bitarray
from bitarray.util import int2ba, ba2int


SEED_DEFAULT = time.perf_counter_ns()


@command
@argument("seed", type=int, description="Decimal seed number", aliases=["s"])
@argument("q", type=int, description="Big position offset")
@argument("r", type=int, description="Little position offset")
@argument("l", type=int, description="Number of bits for decimal conversion")
@argument("cnt", type=int, description="Number of PRNs to generate")
def generate(seed: int = SEED_DEFAULT, q: int = 31, r: int = 5, l: int = 5, cnt: int = 10):
    seed_bin = bitarray()
    if len(seed_bin) < q:
        seed_bin.extend(int2ba(seed))
    if len(seed_bin) > q:
        seed_bin = seed_bin[len(seed_bin) - q:]

    # TODO: Validation

    res = []
    generator = TausworthePRN(seed_bin, q, r, l)
    for _ in range(cnt):
        res.append(generator.next())

    print("Generating {} PRNs for seed {} with q {} and r {}, using {} bits for each number".format(
        cnt, ba2int(seed_bin), q, r, l))
    print("PRNs:\n")

    for prn in res:
        print("{}\n".format(prn))


if __name__ == "__main__":
    shell = Nubia(
        name="Tausworthe PRN",
        command_pkgs=[generate],
    )
    sys.exit(shell.run())
