# Electrical interfaces and compatibility

This is a proposed signal-level connection plan. **GPIO numbers are deliberately unassigned** until the physical DK revision and the Zephyr pin configuration are checked against the board schematic. This document is not a tested wiring schematic.

## Supply plan

1. Power the DK through USB as documented by Nordic. In Board Configurator, set nRF:VDD to **3.3 V**, then measure the relevant VDD:IO header before connecting sensors. The documented factory default is 1.8 V. [Nordic power domains](https://docs.nordicsemi.com/r/bundle/ug_nrf54lm20_dk/page/ug/nrf54lm20_dk/hw_desription/power_supply.html?contentId=QDRMnZ3ju3EJ8KL_fVGSGA).
2. Use a separately regulated 5 V rail for the HX711 analog supplies and motor encoder. Obtain this from a documented auxiliary supply; verify the DK expansion rail's current budget if using its USB 5 V output. Do not backfeed USB or drive the DK's regulated rail from another regulator.
3. Use the verified 3.3 V logic rail for HX711 VDD, accelerometer interface and sensor pull-ups. Check the available peripheral-current budget before assembly; add a separately designed regulator if necessary, not a blindly paralleled supply.
4. Use an enclosed regulated 12 V supply for the motor driver. Tie low-voltage grounds at a suitable common point, keeping motor return current out of sensitive load-cell wiring. No 12 V or 5 V signal may reach a DK GPIO directly.

## Connections

| Device | Proposed connection | Compatibility check |
|---|---|---|
| Adafruit ADXL345 1231 | VIN 3.3 V, GND, four-wire SPI and data-ready if available | Check the purchased revision's level shifting and SPI behaviour. Start at 800 samples/s; verify capture with a logic analyzer |
| HX711 for drag | VCC 5 V, VDD 3.3 V, GND, independent DAT and SCK GPIOs | Use the SparkFun board exposing separate supplies; inspect jumpers before power-up |
| HX711 for normal load | Same supplies, separate DAT and SCK | Do not share clock blindly between the two independent converters |
| Each load cell | E+, E-, A+, A- on its dedicated board | Wire by the individual sensor's datasheet, not a universal colour assumption |
| DRV8876 4036 | VIN 12 V, GND, PH GPIO, EN PWM, SLEEP GPIO | Tie PMODE low before enable; 3.3 V control is supported |
| Driver FAULT | Open-drain input with 10 kOhm pull-up to 3.3 V | Optional but recommended for validity and stopping |
| Motor encoder power | Vcc 5 V, common GND | Manufacturer requires 3.5–20 V; 3.3 V is insufficient |
| Encoder A and B | Each through its own 15 kOhm / 22 kOhm divider | 5 V becomes about 2.97 V; check edges and VIH on the actual setup |
| TCST2103 emitter | 5 V through 220 Ohm resistor; LED return to GND | Starting design around 17 mA for a typical 1.2 V drop; verify actual forward voltage and resistor dissipation |
| TCST2103 detector | Emitter GND, collector pulled to 3.3 V through 10 kOhm | Check output polarity and pulse shape; never use an unknown module with 5 V pull-ups |
| Physical stop | Normally closed DC-rated switch interrupts driver motor supply; auxiliary indication to GPIO if available | Supply interruption is independent of BLE and firmware |

The encoder divider is: encoder output → 15 kOhm → GPIO junction → 22 kOhm → GND. Use 1% resistors. At 5.25 V, the nominal junction is about 3.12 V. Confirm threshold margin and rise time with the actual cable and input capacitance. Use a proper buffer if edges are unreliable; the passive divider is the initial design, not a verified substitute for all speeds.

## Driver and motor matching

The chosen low-power motor has a published 0.9 A stall estimate at 12 V. The chosen Pololu 4036 carrier is rated around 1.3 A continuous under its stated test conditions. This is preferable to selecting a high-power motor whose stall current overwhelms a small driver.

The carrier's default current limit depends on SLEEP/VREF voltage. The approximately 2 A listing assumes 5 V on SLEEP; at 3.3 V it is lower. Do not present the driver's default limit as motor protection: the motor's safe sustained current is well below stall. Add short test durations, motion/stall detection and a fast local stop. Read the actual [driver documentation](https://www.pololu.com/product/4036) before setting VREF or connecting CS to an ADC. Leave CS disconnected initially; motor current is not the drag measurement.

## Load-cell acquisition

Use two genuine/traceable HX711 boards with separate VCC/VDD. The [SparkFun schematic](https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/SparkFun_HX711_Load_Cell_v11.pdf) distinguishes analog supply and digital reference. Start at the documented default 10 samples/s for stable means; 80 samples/s is a later option requiring the correct jumper setting and checks of the exact board revision. Neither rate is suitable for bearing-vibration acquisition.

Generate SCK with a driver that respects HX711 timing even when Bluetooth interrupts occur; avoid a long high pulse that unintentionally powers down the converter. Verify this with a logic analyzer. Do not copy an Arduino example into Zephyr and assume timing is equivalent.

## Before motor power is enabled

- Measure every rail and signal high level with sensors connected and motor disabled.
- Confirm the motor encoder is 5 V powered and both outputs are reduced.
- Prove the physical stop cuts motor power and reset does not auto-start motion.
- Test each force channel with known loads in both directions and verify overload stops.
- Check actual caster pulses independently of the motor encoder.
- Confirm that USB, fixture grounds and external supplies do not create unintended power paths.
- Choose physical GPIOs only after checking reserved pins, peripherals, headers and the board revision schematic.
