module tt_um_JDTL10 (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    // Desactiva IOs no usados
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // Señales internas
    wire led_low, led_med, led_high;

    FSM dut (
        .clk(clk),
        .rst_n(rst_n),
        .weight_ok_i(ui_in[0]),
        .size_ok_i  (ui_in[1]),
        .color_ok_i (ui_in[2]),
        .led_low_o(led_low),
        .led_medium_o(led_med),
        .led_high_o(led_high)
    );

    assign uo_out = {5'b00000, led_high, led_med, led_low};

endmodule
