import sys

key = sys.argv[1]

byts = [ord(c.encode()) for c in key]
bits = ['{:08b}'.format(c) for c in byts]

for i in range(8):
    b = ''.join([bits[j][7-i] for j in range(8)])
    print("reg [7:0] want_{} = 8'b{};".format(i, b))
