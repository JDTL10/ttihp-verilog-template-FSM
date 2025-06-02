import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


@cocotb.test()
async def fsm_test(dut):
    """Prueba funcional de FSM de clasificación de calidad"""

    # Configurar reloj
    clock = Clock(dut.clk, 10, units="ns")  # 100MHz
    cocotb.start_soon(clock.start())

    # Reset
    dut.rst_n.value = 0
    dut.ena.value = 1
    dut.ui_in.value = 0
    await Timer(20, units="ns")
    dut.rst_n.value = 1

    # Esperar ciclo inicial
    await RisingEdge(dut.clk)

    # Test 1: Alta calidad
    dut.ui_in.value = 0b00000111  # peso=1, tamaño=1, color=1
    await Timer(30, units="ns")
    assert dut.uo_out.value[2] == 1, "LED alta calidad debería estar encendido"

    # Test 2: Media calidad
    dut.ui_in.value = 0b00000011  # peso=1, tamaño=1, color=0
    await Timer(30, units="ns")
    assert dut.uo_out.value[1] == 1, "LED media calidad debería estar encendido"

    # Test 3: Baja calidad
    dut.ui_in.value = 0b00000001  # peso=1, tamaño=0, color=0
    await Timer(30, units="ns")
    assert dut.uo_out.value[0] == 1, "LED baja calidad debería estar encendido"

    # Test 4: Rechazado
    dut.ui_in.value = 0b00000000  # peso=0
    await Timer(30, units="ns")
    assert dut.uo_out.value[2:0] == 0, "Ningún LED debería estar encendido para producto rechazado"

