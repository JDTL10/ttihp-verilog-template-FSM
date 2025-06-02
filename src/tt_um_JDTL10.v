module tt_um_JDTL10 (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire clk,
    input  wire rst_n,
    input  wire ena
);

    // Señales internas de salida
    wire led_low, led_medium, led_high;

    // Instancia del módulo FSM
    FSM fsm_inst (
        .clk(clk),
        .rst_n(rst_n),
        .weight_ok_i(ui_in[0]),
        .size_ok_i(ui_in[1]),
        .color_ok_i(ui_in[2]),
        .led_low_o(led_low),
        .led_medium_o(led_medium),
        .led_high_o(led_high)
    );

    // Salidas asignadas a los bits bajos de uo_out
    assign uo_out[0] = led_low;
    assign uo_out[1] = led_medium;
    assign uo_out[2] = led_high;
    assign uo_out[7:3] = 5'b00000; // No usados

    // Pines bidireccionales no utilizados
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

endmodule

