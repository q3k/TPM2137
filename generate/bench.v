`default_nettype none

module bench;

reg clk_10 = 0;
always #5 clk_10 = !clk_10;

reg uart;
wire open;

top top(
        .uart(uart),
        .clk_10(clk_10),
        .led_green(open)
);

initial begin
        $dumpfile("bench.vcd");
        $dumpvars(0);
end


initial begin
        uart = 1;
        #870

        #870 uart = 0;

        #870 uart = 1;
        #870 uart = 0;
        #870 uart = 1;
        #870 uart = 0;
        #870 uart = 1;
        #870 uart = 0;
        #870 uart = 1;
        #870 uart = 0;

        #870 uart = 1;

        #870 uart = 0;

        #870 uart = 1;
        #870 uart = 1;
        #870 uart = 1;
        #870 uart = 1;
        #870 uart = 1;
        #870 uart = 1;
        #870 uart = 0;
        #870 uart = 0;

        #870 uart = 1;

        #870;
        #870;

        $finish;
end

endmodule
