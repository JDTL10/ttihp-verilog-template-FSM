import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from cocotb.result import TestFailure


@cocotb.test()
async def test_fsm_leds(dut):
    """Prueba FSM: Se enciende un LED adecuado según los sensores"""

    # Iniciar el reloj
    clock = Clock(dut.clk, 10, units="ns")  # 100 MHz
    cocotb.start_soon(clock.start())

    # Reset activo en bajo
    dut.rst_n.value = 0
    dut.ena.value = 1  # habilita el diseño
    dut.ui_in.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1  # salir de reset

    async def apply_inputs_and_check(ui_bits, expected_leds, desc):
        dut.ui_in.value = ui_bits
        await RisingEdge(dut.clk)
        await Timer(20, units="ns")  # esperar lógica interna
        result = dut.uo_out.value.integer & 0b00000111  # solo los 3 LSB

        cocotb.log.info(f"[{desc}] ui_in={bin(ui_bits)}, uo_out={bin(result)}")

        if result != expected_leds:
            raise TestFailure(f"Error: salida {bin(result)} esperada {bin(expected_leds)}")

    # Casos de prueba:
    # uo_out[0] = led_low
    # uo_out[1] = led_medium
    # uo_out[2] = led_high

    # 1. Alta calidad (todos los sensores OK) → solo led_high_o
    await apply_inputs_and_check(0b00000111, 0b100, "Alta calidad")

    # 2. Media calidad (peso y tamaño ok, color no) → solo led_medium_o
    await apply_inputs_and_check(0b00000011, 0b010, "Media calidad")

    # 3. Baja calidad (solo peso ok, tamaño no) → solo led_low_o
    await apply_inputs_and_check(0b00000001, 0b001, "Baja calidad")

    # 4. Rechazado (peso no ok) → ningún LED
    await apply_inputs_and_check(0b00000010, 0b000, "Rechazado")

    cocotb.log.info("✅ Todas las pruebas de FSM pasaron correctamente.")
