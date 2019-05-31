`default_nettype none

module bench;

reg clk_12 = 0;
always #5 clk_12 = !clk_12;

reg uart;
wire open;

top top(
        .uart(uart),
        .clk_12(clk_12),
        .open(open)
);

initial begin
        $dumpfile("bench.vcd");
        $dumpvars(0);
end


initial begin
        uart = 1;
        #1040

        #1040 uart = 0;

        #1040 uart = 1;
        #1040 uart = 0;
        #1040 uart = 1;
        #1040 uart = 0;
        #1040 uart = 1;
        #1040 uart = 0;
        #1040 uart = 1;
        #1040 uart = 0;

        #1040 uart = 1;

        #1040 uart = 0;

        #1040 uart = 1;
        #1040 uart = 1;
        #1040 uart = 1;
        #1040 uart = 1;
        #1040 uart = 1;
        #1040 uart = 1;
        #1040 uart = 0;
        #1040 uart = 0;

        #1040 uart = 1;

        #1040;
        #1040;

        $finish;
end

endmodule
