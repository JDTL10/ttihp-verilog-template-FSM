`default_nettype none
module tt_um_JDTL10 (
    input  wire        clk,
    input  wire        rst_n,
    input  wire [7:0]  ui_in,
    output wire [7:0]  uo_out,
    input  wire [7:0]  uio_in,
    output wire [7:0]  uio_out,
    output wire [7:0]  uio_oe,
    input  wire        ena
);

    /* verilator lint_off UNUSEDSIGNAL */
    wire unused = |ui_in[7:3] | |uio_in | ena;
    /* verilator lint_on UNUSEDSIGNAL */

    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    wire led_low, led_medium, led_high;
    wire [1:0] current_state;

    FSM fsm_inst (
        .clk(clk),
        .rst_n(rst_n),
        .weight_ok_i(ui_in[0]),
        .size_ok_i(ui_in[1]),
        .color_ok_i(ui_in[2]),
        .led_low_o(led_low),
        .led_medium_o(led_medium),
        .led_high_o(led_high),
        .current_state_o(current_state)
    );

    assign uo_out = {5'b0, led_high, led_medium, led_low};

endmodule
