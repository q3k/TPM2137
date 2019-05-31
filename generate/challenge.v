`default_nettype none

module top(
        input uart,
        input clk_12,
        output led_green,
        output led_red
);

reg [3:0] rst_counter = 4'b1111;
always @(posedge clk_12) begin
        if (rst_counter != 3'b0) begin
                rst_counter <= rst_counter - 1;
        end
end
wire rst = (rst_counter != 3'b0);

// 12Mhz / 115200 baud == 104 clocks per baud
localparam bauds_per_clock = 104;


`define STATE_IDLE 32'd0
`define STATE_START 32'd1
`define STATE_DATA 32'd2
`define STATE_STOP 32'd3

reg [31:0] state = `STATE_IDLE;
wire downcounter_start;
reg [$clog2(bauds_per_clock)-1:0] downcounter;

reg [3:0] bitn;

always @(posedge clk_12) begin
        if (rst) begin
                bitn <= 0;
                state <= `STATE_IDLE;
        end else begin
                case (state)
                        `STATE_IDLE: begin
                                if (uart == 0) begin
                                        state <= `STATE_START;
                                end
                        end
                        `STATE_START: begin
                                if (downcounter == 0) begin
                                        state <= `STATE_DATA;
                                        bitn <= 7;
                                end
                        end
                        `STATE_DATA: begin
                                if (downcounter == 0) begin
                                        if (bitn == 0) begin
                                                state <= `STATE_STOP;
                                        end else begin
                                                bitn <= bitn - 1;
                                        end
                                end
                        end
                        `STATE_STOP: begin
                                if (downcounter == 0) begin
                                        state <= `STATE_IDLE;
                                end
                        end
                endcase
        end
end

assign downcounter_start =      (state == `STATE_IDLE && uart == 0) ? 1 : 
                                (state == `STATE_START && downcounter == 0) ? 1 :
                                (state == `STATE_DATA && downcounter == 0) ? 1 : 0;


always @(posedge clk_12) begin
        if (rst) begin
                downcounter <= 0;
        end else begin
                if (downcounter_start) begin
                        downcounter <= bauds_per_clock - 1;
                end else begin
                        if (downcounter != 0) begin
                                downcounter <= downcounter - 1;
                        end
                end
        end
end

wire sample_bit = (state == `STATE_DATA && downcounter == bauds_per_clock / 2);

reg [7:0] cur_byte = 0;

always @(posedge clk_12) begin
        if (sample_bit) begin
                cur_byte[7-bitn] <= uart;
        end
end

wire byte_strobe = (state == `STATE_STOP && downcounter == bauds_per_clock / 2);

localparam key_length = 8;
// Hack hack, lovely hack.
reg [key_length-1:0] given_0;
reg [key_length-1:0] given_1;
reg [key_length-1:0] given_2;
reg [key_length-1:0] given_3;
reg [key_length-1:0] given_4;
reg [key_length-1:0] given_5;
reg [key_length-1:0] given_6;
reg [key_length-1:0] given_7;

always @(posedge clk_12) begin
        if (rst) begin
                given_0 <= 0;
                given_1 <= 0;
                given_2 <= 0;
                given_3 <= 0;
                given_4 <= 0;
                given_5 <= 0;
                given_6 <= 0;
                given_7 <= 0;
        end else begin
                if (byte_strobe) begin
                        given_0 <= {given_0[6:0], cur_byte[0]};
                        given_1 <= {given_1[6:0], cur_byte[1]};
                        given_2 <= {given_2[6:0], cur_byte[2]};
                        given_3 <= {given_3[6:0], cur_byte[3]};
                        given_4 <= {given_4[6:0], cur_byte[4]};
                        given_5 <= {given_5[6:0], cur_byte[5]};
                        given_6 <= {given_6[6:0], cur_byte[6]};
                        given_7 <= {given_7[6:0], cur_byte[7]};
                end
        end
end

`include "want.v"

wire open =   (want_0 == given_0) &&
                (want_1 == given_1) &&
                (want_2 == given_2) &&
                (want_3 == given_3) &&
                (want_4 == given_4) &&
                (want_5 == given_5) &&
                (want_6 == given_6) &&
                (want_7 == given_7);

assign led_green = !open;
assign led_red = open;

endmodule
