#!/usr/bin/env python3

import sys
from nubia import Nubia

import commands


if __name__ == "__main__":
    shell = Nubia(
        name="Tausworthe PRN",
        command_pkgs=commands,
    )
    sys.exit(shell.run())
