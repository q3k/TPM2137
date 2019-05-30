default: challenge.bit

want.v: want.py
	python3 want.py hackme12 > want.v

challenge.json: challenge.v want.v
	yosys -p 'synth_ice40; write_json $@' "$<"

challenge.asc: challenge.json challenge.pcf
	nextpnr-ice40 --up5k --json challenge.json --asc "$@" --pcf challenge.pcf

challenge.bit: challenge.asc
	icepack "$<" "$@"

flash: challenge.bit
	sudo iceprog challenge.bit

bench: bench.v challenge.v want.v
	iverilog bench.v challenge.v -o bench

test: bench
	./bench
	

clean:
	rm -f challenge.asc challenge.json challenge.bit bench bench.vcd want.v
