#!/usr/bin/env python3

"""Main."""

import sys
from cpu import CPU

cpu = CPU()

cpu.load("sctest.ls8")
cpu.run()