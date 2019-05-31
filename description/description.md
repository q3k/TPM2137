RadomSemi is a new venture that provides hardware secure processing elements. Its flagship product, TPM2137, is supposedly unhackable. We have managed to acquire a sample of the device from the manufacturer, and have since extraced the bitstream from it. The chip itself is an iCE40 UP5K FPGA with original markings ground off and a laser etched 'RadomSemi TPM2137 UNHACKABLE' visible instead.

We have also managed to trace pins of the device to the input UART, clock and LEDs. They are as follows:

| FPGA Pin | Function    |
|----------|-------------|
| 35       | Clock       |
| 6        | UART        |
| 11       | LED Red     |
| 37       | LED Green   |

Please find the password for this device. We also attach the public datasheet from the manufacturer.
