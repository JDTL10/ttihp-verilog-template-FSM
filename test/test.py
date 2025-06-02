import cocotb
from cocotb.triggers import RisingEdge
from cocotb.result import TestFailure

async def apply_and_check(dut, ui_in_val, expected_leds, desc):
    dut.ui_in.value = ui_in_val
    # Esperar 4 ciclos para que FSM complete estado OUTPUT_RESULT
    for _ in range(4):
        await RisingEdge(dut.clk)

    # Leer salida
    leds_out = dut.uo_out.value.integer & 0x7  # Solo bits 0-2 LEDs

    dut._log.info(f"[{desc}] ui_in: 0b{ui_in_val:03b} -> uo_out LEDs: 0b{leds_out:03b} (esperado 0b{expected_leds:03b})")

    if leds_out != expected_leds:
        raise TestFailure(f"FAIL {desc}: Entrada ui_in=0b{ui_in_val:03b} | Salida LEDs=0b{leds_out:03b}, esperada=0b{expected_leds:03b}")

@cocotb.test()
async def test_fsm_leds_verbose(dut):
    dut._log.info("Prueba FSM con logs extendidos para debug")

    dut.clk.value = 0
    dut.rst_n.value = 0
    dut.ui_in.value = 0

    # Reset activo
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.rst_n.value = 1

    # Ciclo inicial
    await RisingEdge(dut.clk)

    # Pruebas: ui_in[2:0] -> LEDs [led_high, led_medium, led_low]
    await apply_and_check(dut, 0b111, 0b100, "Alta calidad")
    await apply_and_check(dut, 0b110, 0b000, "No cumple media ni baja")  # Esta entrada no debe encender ningún led
    await apply_and_check(dut, 0b011, 0b010, "Media calidad")
    await apply_and_check(dut, 0b010, 0b000, "No cumple")
    await apply_and_check(dut, 0b001, 0b001, "Baja calidad")
    await apply_and_check(dut, 0b000, 0b000, "Rechazado/no peso")

    dut._log.info("Todas las pruebas pasaron correctamente.")


