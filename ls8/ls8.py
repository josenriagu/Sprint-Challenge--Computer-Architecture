#!/usr/bin/env python3

"""Main."""

import sys
from cpu import CPU

cpu = CPU()

cpu.load("call.ls8")
cpu.run()