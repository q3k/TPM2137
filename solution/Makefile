solve: challenge.json
	~/CTF/venv-pypy/bin/python solve.py "$<"

challenge.json: challenge.v
	yosys -p 'read_verilog challenge.v; synth -noabc; write_json challenge.json'

challenge.v: challenge.asc
	icebox_vlog -s -S -l -c "$<" > "$@"

challenge.asc: challenge.bit
	iceunpack "$<" > "$@"

.PHONY: solve
