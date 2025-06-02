module tt_um_JDTL10 (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,   // No usado
    output wire [7:0] uio_out,  // No usado
    output wire [7:0] uio_oe,   // No usado
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);
    wire [3:0] A = ui_in[3:0];
    wire [3:0] B = ui_in[7:4];

    wire [3:0] Result;
    wire CarryOut_ALU, Overflow_ALU, Zero, Negative;

    ALU alu_inst (
        .A(A),
        .B(B),
        .Result(Result),
        .CarryOut_ALU(CarryOut_ALU),
        .Overflow_ALU(Overflow_ALU),
        .Zero(Zero),
        .Negative(Negative)
    );

    assign uo_out[3:0] = Result;
    assign uo_out[4]   = CarryOut_ALU;
    assign uo_out[5]   = Overflow_ALU;
    assign uo_out[6]   = Zero;
    assign uo_out[7]   = Negative;

    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;
endmodule
