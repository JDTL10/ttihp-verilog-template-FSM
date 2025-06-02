import cocotb
from cocotb.triggers import RisingEdge, Timer

async def apply_and_check(dut, inputs, expected_leds, label):
    dut._log.info(f"[{label}] ui_in: {bin(inputs)} -> esperando LEDs: {bin(expected_leds)}")
    dut.ui_in.value = inputs
    await RisingEdge(dut.clk)
    await Timer(1, units='ns')  # Pequeño delay para asegurar transición
    leds = dut.uo_out.value.integer & 0b111
    assert leds == expected_leds, (
        f"FAIL {label}: Entrada ui_in={bin(inputs)} | "
        f"Salida LEDs={bin(leds)}, esperada={bin(expected_leds)}"
    )

@cocotb.test()
async def test_fsm_leds_verbose(dut):
    """Prueba FSM con logs extendidos para debug"""
    dut.rst_n.value = 0
    dut.clk.value = 0
    dut.ui_in.value = 0
    await Timer(2, units='ns')
    dut.rst_n.value = 1

    # Simula reloj
    for _ in range(2):  # Pulso inicial
        dut.clk.value = 1
        await Timer(1, units='ns')
        dut.clk.value = 0
        await Timer(1, units='ns')

    # Alta calidad: peso, tamaño y color OK (111)
    await apply_and_check(dut, 0b111, 0b100, "Alta calidad")

    # Media calidad: peso y tamaño OK, color NO (011)
    await apply_and_check(dut, 0b011, 0b010, "Media calidad")

    # Baja calidad: solo peso OK, tamaño NO (001)
    await apply_and_check(dut, 0b001, 0b001, "Baja calidad")

    # Rechazada: peso NO (000)
    await apply_and_check(dut, 0b000, 0b000, "Rechazada")

