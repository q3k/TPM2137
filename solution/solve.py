import json
import re
import sys
import itertools
import z3

class Constant:
    def __init__(self, value):
        self.value = value

    def recover_combinatorial(self):
        return self

class Cell:
    TYPE = None
    def __init__(self, name, j):
        self.name = name
        self.j = j
        self.nets = {}
        self.net_directions = {}
        assert j['type'] == self.TYPE

    def connect(self, nets):
        for c, bit in self.j['connections'].items():
            assert len(bit) == 1
            bit = bit[0]
            direction = self.j['port_directions'][c]
            self.net_directions[c] = direction

            if type(bit) == str:
                self.nets[c] = Constant(int(bit))
            else:
                self.nets[c] = nets[bit]
                nets[bit].connect(self, c, direction)

    def recover_combinatorial(self):
        res = {}
        for i in self.INPUTS:
            res[i] = self.nets[i].recover_combinatorial()
        return (self.TYPE, res)

    def __repr__(self):
        return '<{} {}>'.format(self.j['type'], self.name)

class And(Cell):
    TYPE = '$_AND_'
    INPUTS = 'AB'

class Or(Cell):
    TYPE = '$_OR_'
    INPUTS = 'AB'

class Not(Cell):
    TYPE = '$_NOT_'
    INPUTS = 'A'

class Mux(Cell):
    TYPE = '$_MUX_'
    INPUTS = 'ABS'

class Dff(Cell):
    TYPE = '$_DFF_P_'
    def recover_combinatorial(self):
        return self

ctypes = {
    '$_AND_': And,
    '$_OR_': Or,
    '$_NOT_': Not,
    '$_MUX_': Mux,
    '$_DFF_P_': Dff,
}

class Net:
    def __init__(self, name, bit, constant=False):
        self.name = name
        self.bit = bit
        self.ports = set()
        self.constant = constant


    def connect(self, cell, port, direction):
        self.ports.add((cell, port, direction))

    def driver(self):
        drivers = [p for p in list(self.ports) if p[2] == 'output']
        assert len(drivers) == 1
        return drivers[0]

    def recover_combinatorial(self):
        driver, driver_port, driver_dir = self.driver()
        return driver.recover_combinatorial()

    def orig_name(self):
        assert self.name.startswith('$0\\')
        return self.name[3:].split('[')[0]


    def __repr__(self):
        return self.name

def parse_json(f):
    j = json.load(f)
    chip = j['modules']['chip']

    cells = {}

    for name, c in chip['cells'].items():
        t = c['type']
        if t not in ctypes:
            raise Exception("Unknown cell type {}".format(t))
        cells[name] = ctypes[t](name, c)

    nets = {}

    for name, n in chip['netnames'].items():
        assert len(n['bits']) == 1
        bit = n['bits'][0]
        if bit == 'x':
            continue
        elif type(bit) == str:
            nets[bit] = Net(name, bit, constant=True)
        else:
            nets[bit] = Net(name, bit)

    return cells, nets

with open(sys.argv[1], 'r') as f:
    cells, nets = parse_json(f)

netnames = {}
for bit, net in nets.items():
    netnames[net.name] = bit

for _, cell in cells.items():
    cell.connect(nets)

net_ok = nets[netnames['pin_11']]

print('net_ok', net_ok)

comb = net_ok.recover_combinatorial()

def combinatorial_solve(comb, want):
    s = z3.Solver()
    dffs = set()
    def to_z3(expr, s):
        if type(expr) == Dff:
            v = z3.BitVec(expr.name, 1)
            dffs.add(v)
            return v
        if type(expr) == Constant:
            return z3.BitVecVal(expr.value, 1)

        elem, children = expr

        vals = dict([(k, to_z3(child, s)) for k, child in children.items()])

        if elem == '$_AND_':
            return vals['A'] & vals['B']
        elif elem == '$_NOT_':
            return ~vals['A']
        elif elem == '$_MUX_':
            return z3.If(vals['S'] == 0, vals['A'], vals['B'])
        else:
            raise Exception(elem)


    v = to_z3(comb, s)
    s.add(v == 1)
    s.check()
    m = s.model()

    res = {}

    for dff in list(dffs):
        v = m[dff]
        dffc = cells[str(dff)]
        res[dffc] = int(str(v))

    return res

shiftreg_dffs = combinatorial_solve(comb, 1)
print('solved flag dff bits:')
for dff, val in shiftreg_dffs.items():
    print('  {}: {}'.format(dff.nets['Q'], val))

def build_shiftregs(dffs):
    # map of dff -> source dff
    neighbors = {}

    for dff in dffs:
        assert dff.nets['C'].name == 'pin_35' # external clock

        # clock-in mux
        mux, port, _ = dff.nets['D'].driver()
        assert port == 'Y'
        assert mux.TYPE == '$_MUX_'
        #assert mux.nets['S'].name == 'n360' # alias of n1, byte latch?

        # on clock, select next
        b, port, _  = mux.nets['B'].driver()
        assert port == 'Y'
        assert b.TYPE == '$_MUX_'
        #assert b.nets['S'].name == 'n381' # alias of n2, reset?

        assert type(b.nets['B']) == Constant
        assert b.nets['B'].value == 0

        src, port, _ = b.nets['A'].driver()
        assert port == 'Q'
        neighbors[dff] = src
        print('connectivity {} -> {}'.format(src.nets['Q'], dff.nets['Q']))

    seen = set()
    def trace(dst):
        seen.add(dst)
        src = neighbors.get(dst)
        dst.srsrc = src
        if src is not None:
            trace(src)

    for dst, src in neighbors.items():
        trace(dst)

    chains = {}
    for dff in seen:
        if dff.srsrc is not None:
            continue
        chains[dff] = []
        cur = dff
        while True:
            for dff2 in seen:
                if dff2.srsrc == cur:
                    chains[dff].append(dff2)
                    cur = dff2
                    break
            else:
                break

    assert len(chains) == 8

    netchains = []
    valuechains = []
    for _, c in chains.items():
        assert len(c) == 8
        vc = []
        nc = []
        for cc in c:
            nc.append(cc.nets['Q'].name)
            vc.append(dffs[cc])
        valuechains.append(vc)
        netchains.append(nc)

    for i in range(8):
        print('chain {}:'.format(i))
        print('    dffs:', ', '.join(netchains[i]))
        print('  values:', ', '.join(str(c) for c in valuechains[i]))

    selectors = []
    for nc in netchains:
        net = nets[netnames[nc[0]]]
        sr_driver, _, _ = net.driver()

        sr_driver2, _, _ = sr_driver.nets['D'].driver()
        assert sr_driver2.nets['A'].name == net.name
        #assert sr_driver2.nets['S'].name == 'n360' # n1

        sr_driver3, _, _ = sr_driver2.nets['B'].driver()
        #assert sr_driver3.nets['S'].name == 'n381'
        assert sr_driver3.nets['B'].value == 0

        sr_driver4, _, _ = sr_driver3.nets['A'].driver()

        sr_driver5, _, _ = sr_driver4.nets['D'].driver()
        assert sr_driver5.nets['B'].name == 'pin_6' # serial in

        selectors.append(sr_driver5.nets['S'])

    counter_bits = set()
    counter_bit_values = []

    for i, selector in enumerate(selectors):
        comb = selector.recover_combinatorial()
        dffs = combinatorial_solve(comb, 1)
        values = {}
        for dff, val in dffs.items():
            net = dff.nets['Q']
            values[net] = val
            if i == 0:
                counter_bits.add(net)
            else:
                assert net in counter_bits
        counter_bit_values.append(values)

    print('bit counter', counter_bits)

    # eliminate unnecessary bits

    values_per_selector = {}

    for cbv in counter_bit_values:
        for net, value in cbv.items():
            if net not in values_per_selector:
                values_per_selector[net] = []
            values_per_selector[net].append(value)

    important_counter_bits = set()
    for net, values in values_per_selector.items():
        if len(list(set(values))) == 2:
            important_counter_bits.add(net)


    print('bit counter (pruned)', important_counter_bits)

    for bit_counter_order in itertools.permutations(important_counter_bits):
        bitn_to_chainno = {}
        for i in range(8):
            cbv = counter_bit_values[i]
            chain_selector_bits = [cbv[net] for net in bit_counter_order]
            chain_selector_number = int(''.join(str(n) for n in chain_selector_bits), 2)
            bitn_to_chainno[chain_selector_number] = i

        flag = ''
        for byten in range(7, -1, -1):
            val = []
            for bitn in range(8):
                bit = valuechains[bitn_to_chainno[bitn]][byten]
                val.append(str(bit))

            valn = int(''.join(val), 2)
            flag += chr(valn)

        print('attempting bit counter order', bit_counter_order)
        print('flag:', repr(flag))
        print()



build_shiftregs(shiftreg_dffs)
