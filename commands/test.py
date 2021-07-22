from time import perf_counter_ns
from nubia.internal.typing import argument, command
from bitarray import bitarray
from bitarray.util import int2ba, ba2int
from tausworthe import TausworthePRN
import matplotlib.pyplot as plt
from numpy import histogram, sqrt


SEED_DEFAULT = 42424242424242
# Number of cells for the goodness-of-fit test
k = 101
chi2_ref = 124.342
z_ref = 1.96


@command
@argument("seed", type=int, description="Decimal seed number")
@argument("q", type=int, description="Big position offset")
@argument("r", type=int, description="Little position offset")
@argument("l", type=int, description="Number of bits for decimal conversion")
@argument("cnt", type=int, description="Number of PRNs to generate")
def test(seed: int = SEED_DEFAULT, q: int = 31, r: int = 5, l: int = 20, cnt: int = 10000):
    """
    Generate a series of PRNs using Tausworthe PRN generator. Test the result for independence and goodness-of-fit
    """

    seed_bin = bitarray()
    while len(seed_bin) < q:
        seed_bin.extend(int2ba(seed))
    if len(seed_bin) > q:
        seed_bin = seed_bin[len(seed_bin) - q:]

    # TODO: Validation

    print("Generating {} PRNs for seed {} with q {} and r {}, using {} bits for each number\n".format(
        cnt, ba2int(seed_bin), q, r, l))

    res = []
    generator = TausworthePRN(seed_bin, q, r, l)
    for _ in range(cnt):
        res.append(generator.next())

    print("Generated {} PRNs\n".format(len(res)))

    fig1, ax1 = plt.subplots(figsize=(16, 16))

    x = [prn for i, prn in enumerate(res) if i % 2 == 0]
    y = [prn for i, prn in enumerate(res) if i % 2 != 0]
    assert(len(x) == len(y))
    print("Aggregated {} pairs\n".format(len(x)))

    ax1.scatter(x, y)

    ax1.set_title("{} PRNs (q {}, r {}, l {})\n".format(cnt, q, r, l))

    fig1.savefig("PRNs-{}-{}-{}-{}.png".format(cnt, q, r, l))
    plt.close(fig1)
    print("Printed a graph\n")

    print("Running goodness-of-fit test with {} cells\n".format(k))
    ei = cnt / k
    os, _ = histogram(res, bins=k, range=[0, 1])
    chi2 = 0
    for o in os:
        chi2 += pow((o - ei), 2) / ei
    print("Chi squared is {}, while reference chi squared {} (a = 0.05)\n".format(
        chi2, chi2_ref))

    gof_passed = chi2 < chi2_ref

    if not gof_passed:
        print("Goodness-of-fit test failed\n")
        return 0
    print("Goodness-of-fit test passed\n")

    print("Running independence test\n")
    runs = 1
    run_direction = 'up'
    num = res[0]
    for next_num in res[1:]:
        next_direction = 'down' if (next_num - num) < 0 else 'up'
        num = next_num
        if next_direction != run_direction:
            run_direction = next_direction
            runs += 1
    print("Found {} runs\n".format(runs))
    z0 = (runs - (2 * cnt) / 3) / sqrt((16 * cnt - 29) / 90)
    print("Z0 is {}, while reference Z-score (a=0.05) is {}\n".format(z0, z_ref))

    if z0 < 0:
        z0 = -z0
    indep_passed = z0 < z_ref
    if not indep_passed:
        print("Independence test failed\n")
        return 0
    print("Independence test passed\n")
