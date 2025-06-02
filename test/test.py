import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from cocotb.result import TestFailure


@cocotb.test()
async def test_fsm_leds_verbose(dut):
    """Prueba FSM con logs extendidos para debug"""

    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut.rst_n.value = 0
    dut.ena.value = 1
    dut.ui_in.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1

    async def apply_and_check(ui_bits, expected_leds, desc):
        dut.ui_in.value = ui_bits
        await RisingEdge(dut.clk)
        await Timer(20, units="ns")

        actual = dut.uo_out.value.integer & 0b111  # solo 3 LSB LEDs

        cocotb.log.info(f"[{desc}] ui_in: {bin(ui_bits)} -> uo_out LEDs: {bin(actual)} (esperado {bin(expected_leds)})")

        if actual != expected_leds:
            raise TestFailure(
                f"FAIL {desc}: Entrada ui_in={bin(ui_bits)} | "
                f"Salida LEDs={bin(actual)}, esperada={bin(expected_leds)}"
            )

    await apply_and_check(0b111, 0b100, "Alta calidad")
    await apply_and_check(0b011, 0b010, "Media calidad")
    await apply_and_check(0b001, 0b001, "Baja calidad")
    await apply_and_check(0b010, 0b000, "Rechazado")

    cocotb.log.info("✅ Todas las pruebas FSM pasaron correctamente.")

