# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start test sequence")

    # Start clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Helper function
    async def run_test(A, B, OpSel, expected_result):
        ui_in_value = (B << 4) | A  # Pack B (upper 4) + A (lower 4)
        dut.ui_in.value = ui_in_value

        await ClockCycles(dut.clk, 1)

        result_bits = dut.uo_out.value.integer & 0b1111  # 4 LSB
        carry = (dut.uo_out.value.integer >> 4) & 0b1
        overflow = (dut.uo_out.value.integer >> 5) & 0b1
        zero = (dut.uo_out.value.integer >> 6) & 0b1
        negative = (dut.uo_out.value.integer >> 7) & 0b1

        dut._log.info(f"A={A}, B={B}, OpSel={OpSel:02b}, Result={result_bits}, Carry={carry}, Overflow={overflow}, Zero={zero}, Negative={negative}")

        assert result_bits == (expected_result & 0b1111), f"Expected result {expected_result}, got {result_bits}"

    # TEST 1: SUM (OpSel=00)
    await run_test(A=5, B=3, OpSel=0b00, expected_result=(5 + 3))

    # TEST 2: RESTA (OpSel=01)
    await run_test(A=7, B=2, OpSel=0b01, expected_result=(7 - 2))

    # TEST 3: AND (OpSel=10)
    await run_test(A=6, B=3, OpSel=0b10, expected_result=(6 & 3))

    # TEST 4: OR (OpSel=11)
    await run_test(A=4, B=1, OpSel=0b11, expected_result=(4 | 1))

    dut._log.info("All tests passed!")
