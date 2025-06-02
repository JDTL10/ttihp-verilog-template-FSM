`default_nettype none
module FSM (
    input  logic         clk,
    input  logic         rst_n,          // Asynchronous active-low reset

    input  logic         weight_ok_i,    // Sensor peso
    input  logic         size_ok_i,      // Sensor tamaño
    input  logic         color_ok_i,     // Sensor color

    output logic        led_low_o,      // Led para baja calidad
    output logic        led_medium_o,   // Led para media calidad
    output logic        led_high_o,     // Led para alta calidad

    output logic [1:0]  current_state_o // Para debug en testbench
);

    typedef enum logic [1:0] {
        S_IDLE,
        S_EVALUATE,
        S_OUTPUT_RESULT
    } state_t;

    state_t current_state, next_state;

    logic   is_low_quality;
    logic   is_medium_quality;
    logic   is_high_quality;

    // Estado síncrono
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            current_state <= S_IDLE;
        else
            current_state <= next_state;
    end

    // Lógica siguiente estado
    always_comb begin
        case (current_state)
            S_IDLE:         next_state = S_EVALUATE;
            S_EVALUATE:     next_state = S_OUTPUT_RESULT;
            S_OUTPUT_RESULT:next_state = S_IDLE;
            default:        next_state = S_IDLE;
        endcase
    end

    // Condiciones calidad
    always_comb begin
        is_high_quality   = (weight_ok_i && size_ok_i && color_ok_i);
        is_medium_quality = (weight_ok_i && size_ok_i && !color_ok_i);
        is_low_quality    = (weight_ok_i && !size_ok_i);
    end

    // Salidas registradas (sincronizadas)
    reg led_low_r, led_medium_r, led_high_r;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            led_low_r    <= 1'b0;
            led_medium_r <= 1'b0;
            led_high_r   <= 1'b0;
        end else if (current_state == S_OUTPUT_RESULT) begin
            led_low_r    <= is_low_quality;
            led_medium_r <= is_medium_quality;
            led_high_r   <= is_high_quality;
        end else begin
            led_low_r    <= 1'b0;
            led_medium_r <= 1'b0;
            led_high_r   <= 1'b0;
        end
    end

    assign led_low_o    = led_low_r;
    assign led_medium_o = led_medium_r;
    assign led_high_o   = led_high_r;

    assign current_state_o = current_state;

endmodule

