This is an automated solver for the generated tasks. It seems to work.

The procedure is:
 - convert .bit to .asc, then to .v, then to .json (after processing by yosys)
 - recover all flag bits and their values (using z3)
 - find shift registers (8x 8bits)
 - find shift register selector bits from bit counter
 - prune down to 3 selector bits
 - attempt to print flag organized by all possible arrangement of selector bits (8 possible flags, one should be correct)

Sample run
----------

(from included challenge.bit)

```
net_ok pin_11
solved flag dff bits:
  n279: 1
  n339: 1
  n271: 1
  n382: 1
  n309: 1
  n422: 1
  n417: 1
  n211: 1
  n393: 1
  n192: 1
  n273: 1
  n374: 1
  n348: 1
  n232: 1
  n343: 1
  n369: 1
  n266: 1
  n68: 1
  n117: 1
  n272: 1
  n388: 1
  n269: 1
  n276: 1
  n383: 1
  n267: 1
  n368: 1
  n377: 1
  n257: 1
  n239: 0
  n178: 0
  n351: 0
  n358: 0
  n440: 0
  n223: 0
  n231: 0
  n438: 0
  n354: 0
  n249: 0
  n258: 0
  n334: 0
  n268: 0
  n238: 0
  n245: 0
  n190: 0
  n301: 0
  n403: 0
  n362: 0
  n219: 0
  n353: 0
  n146: 0
  n274: 0
  n248: 0
  n317: 0
  n327: 0
  n428: 0
  n320: 0
  n224: 0
  n341: 0
  n164: 0
  n370: 0
  n384: 0
  n392: 0
  n373: 0
  n381: 0
connectivity n393 -> n279
connectivity n382 -> n339
connectivity n279 -> n271
connectivity n271 -> n382
connectivity n339 -> n309
connectivity n403 -> n422
connectivity n301 -> n417
connectivity n309 -> n211
connectivity n273 -> n393
connectivity n374 -> n192
connectivity n420 -> n273
connectivity n343 -> n374
connectivity n334 -> n348
connectivity n341 -> n232
connectivity n348 -> n343
connectivity n268 -> n369
connectivity n272 -> n266
connectivity n79 -> n68
connectivity n381 -> n117
connectivity n392 -> n272
connectivity n379 -> n388
connectivity n377 -> n269
connectivity n370 -> n276
connectivity n388 -> n383
connectivity n257 -> n267
connectivity n274 -> n368
connectivity n353 -> n377
connectivity n266 -> n257
connectivity n440 -> n239
connectivity n351 -> n178
connectivity n358 -> n351
connectivity n239 -> n358
connectivity n438 -> n440
connectivity n231 -> n223
connectivity n81 -> n231
connectivity n223 -> n438
connectivity n253 -> n354
connectivity n354 -> n249
connectivity n369 -> n258
connectivity n258 -> n334
connectivity n333 -> n268
connectivity n245 -> n238
connectivity n224 -> n245
connectivity n238 -> n190
connectivity n422 -> n301
connectivity n249 -> n403
connectivity n417 -> n362
connectivity n362 -> n219
connectivity n368 -> n353
connectivity n248 -> n146
connectivity n256 -> n274
connectivity n267 -> n248
connectivity n320 -> n317
connectivity n317 -> n327
connectivity n439 -> n428
connectivity n428 -> n320
connectivity n232 -> n224
connectivity n383 -> n341
connectivity n276 -> n164
connectivity n269 -> n370
connectivity n327 -> n384
connectivity n68 -> n392
connectivity n384 -> n373
connectivity n373 -> n381
chain 0:
    dffs: n273, n393, n279, n271, n382, n339, n309, n211
  values: 1, 1, 1, 1, 1, 1, 1, 1
chain 1:
    dffs: n354, n249, n403, n422, n301, n417, n362, n219
  values: 0, 0, 0, 1, 0, 1, 0, 0
chain 2:
    dffs: n268, n369, n258, n334, n348, n343, n374, n192
  values: 0, 1, 0, 0, 1, 1, 1, 1
chain 3:
    dffs: n388, n383, n341, n232, n224, n245, n238, n190
  values: 1, 1, 0, 1, 0, 0, 0, 0
chain 4:
    dffs: n68, n392, n272, n266, n257, n267, n248, n146
  values: 1, 0, 1, 1, 1, 1, 0, 0
chain 5:
    dffs: n428, n320, n317, n327, n384, n373, n381, n117
  values: 0, 0, 0, 0, 0, 0, 0, 1
chain 6:
    dffs: n274, n368, n353, n377, n269, n370, n276, n164
  values: 0, 1, 0, 1, 1, 0, 1, 0
chain 7:
    dffs: n231, n223, n438, n440, n239, n358, n351, n178
  values: 0, 0, 0, 0, 0, 0, 0, 0
bit counter {n14, n61, n52, n71, n72, n12, n11, n13, n20, n24, n221, n10, n34}
bit counter (pruned) {n14, n71, n34}
attempting bit counter order (n14, n71, n34)
flag: '\x1c\x0eM\x0fk\t.)'

attempting bit counter order (n14, n34, n71)
flag: '\x1a\x0e+\x0fm\tNI'

attempting bit counter order (n71, n14, n34)
flag: '42q3k!:)'

attempting bit counter order (n71, n34, n14)
flag: 'RTqUmA\\I'

attempting bit counter order (n34, n14, n71)
flag: '&2+3y!ra'

attempting bit counter order (n34, n71, n14)
flag: 'FTMUyAta'

```
