module ALU (
    input  wire [3:0] A,  // ui_in[0]–ui_in[3]
    input  wire [3:0] B,  // ui_in[4]–ui_in[7]
    output reg  [3:0] Result,
    output reg        CarryOut_ALU,
    output reg        Overflow_ALU,
    output wire       Zero,
    output wire       Negative
);
    wire [4:0] sum_result = A + B;
    wire [4:0] rest_result = A - B;
    wire [3:0] and_result = A & B;
    wire [3:0] or_result  = A | B;

    wire [1:0] OpSel = A[1:0];  // Operación tomada de A[1:0]

    always @(*) begin
        case (OpSel)
            2'b00: begin
                Result = sum_result[3:0];
                CarryOut_ALU = sum_result[4];
                Overflow_ALU = (A[3] == B[3]) && (Result[3] != A[3]);
            end
            2'b01: begin
                Result = rest_result[3:0];
                CarryOut_ALU = rest_result[4];
                Overflow_ALU = (A[3] != B[3]) && (Result[3] != A[3]);
            end
            2'b10: begin
                Result = and_result;
                CarryOut_ALU = 0;
                Overflow_ALU = 0;
            end
            2'b11: begin
                Result = or_result;
                CarryOut_ALU = 0;
                Overflow_ALU = 0;
            end
            default: begin
                Result = 4'b0000;
                CarryOut_ALU = 0;
                Overflow_ALU = 0;
            end
        endcase
    end

    assign Zero     = (Result == 4'b0000);
    assign Negative = Result[3];
endmodule
