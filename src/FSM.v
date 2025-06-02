module FSM (
    input wire clk,
    input wire rst_n,
    input wire weight_ok_i,
    input wire size_ok_i,
    input wire color_ok_i,
    output reg led_low_o,
    output reg led_medium_o,
    output reg led_high_o
);

    reg [1:0] current_state, next_state;

    localparam S_IDLE = 2'b00;
    localparam S_EVALUATE = 2'b01;
    localparam S_OUTPUT_RESULT = 2'b10;

    wire is_high_quality   = weight_ok_i && size_ok_i && color_ok_i;
    wire is_medium_quality = weight_ok_i && size_ok_i && !color_ok_i;
    wire is_low_quality    = weight_ok_i && !size_ok_i;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            current_state <= S_IDLE;
        else
            current_state <= next_state;
    end

    always @(*) begin
        next_state = current_state;
        case (current_state)
            S_IDLE: next_state = S_EVALUATE;
            S_EVALUATE: next_state = S_OUTPUT_RESULT;
            S_OUTPUT_RESULT: next_state = S_IDLE;
            default: next_state = S_IDLE;
        endcase
    end

    always @(*) begin
        led_low_o = 1'b0;
        led_medium_o = 1'b0;
        led_high_o = 1'b0;

        if (current_state == S_OUTPUT_RESULT) begin
            if (is_high_quality)
                led_high_o = 1'b1;
            else if (is_medium_quality)
                led_medium_o = 1'b1;
            else if (is_low_quality)
                led_low_o = 1'b1;
        end
    end

endmodule
