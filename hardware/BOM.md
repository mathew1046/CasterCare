# Initial bill of materials

**CasterCare — Sustain the System hardware application.** Research date: 26 October 2026.

This is the beginning BOM for a single-controller, light-load bench prototype. It explicitly includes the **Nordic nRF54LM20 DK**. The selections are researched reference parts, not a claim that the system has been assembled or tested. Custom items still require dimensions and quotations. No purchases have been made.

## What to buy first

Start with B01–B05 for voltage checks, sensor capture and force calibration. Finalize the caster and load-path design before ordering B20–B27. The motor/driver are a matched reference pair, not an invitation to substitute a higher-current motor. Basic motor tests can proceed separately, guarded and unloaded.

## Required reference parts and fabrication

| ID | Purchase quantity | Reference part or specification | Purpose | Observed USD unit/package price |
|---|---|---|---|---|
| B01 | 1 board | [NRF54LM20-DK](https://www.nordicsemi.com/Products/Development-hardware/nRF54LM20-DK) | Main controller; CPU inference and optional Axon; BLE | Quote required / existing |
| B02 | 1 board | [1231 ADXL345 breakout](https://www.adafruit.com/product/1231) | Caster-fork vibration; SPI | $17.50 |
| B03 | 1 cell | [SEN-14728 TAL221 500 g](https://www.sparkfun.com/mini-load-cell-500g-straight-bar-tal221.html) | Horizontal reaction force under light preload | $15.50 |
| B04 | 1 cell | [SEN-13329 TAL220 10 kg](https://www.sparkfun.com/load-cell-10kg-straight-bar-tal220.html) | Measure applied contact load independently | Quote required / existing |
| B05 | 2 boards | [SEN-13879 HX711 separate VCC and VDD](https://www.sparkfun.com/sparkfun-load-cell-amplifier-hx711.html) | One converter per force channel | Quote required / existing |
| B06 | 1 motor | [4886 75:1 25D LP 12 V with 48 CPR encoder](https://www.pololu.com/product/4886) | Low-speed roller drive and roller RPM | $53.95 |
| B07 | 1 board | [4036 DRV8876 carrier](https://www.pololu.com/product/4036) | PWM speed control and local disable | $8.15 |
| B08 | 1 pair package | [2676 25D bracket pair](https://www.pololu.com/product/2676) | Correct motor mounting | $10.95 |
| B10 | 1 sensor | [TCST2103 photointerrupter](https://www.vishay.com/docs/81147/tcst2103.pdf) | Independent actual wheel rotation and slip check | Quote required / existing |
| B11 | 2 divider sets | 15 kOhm and 22 kOhm 1% resistors | Reduce motor encoder A and B from 5 V to about 2.97 V | Quote required / existing |
| B12 | 1 set | 10 kOhm 1% and 220 Ohm 0.25 W | Optical detector; driver FAULT; optical LED current | Quote required / existing |
| B13 | 1 supply | Enclosed regulated 12 V DC at least 2 A | Separate motor power | Quote required / existing |
| B14 | 1 supply | Regulated 5 V at least 0.5 A | Encoder and HX711 analog rail | Quote required / existing |
| B15 | 1 cable | Connector matched to actual DK | DK power programming and development logs | Quote required / existing |
| B16 | 1 switch | Normally closed emergency stop / latching stop | Interrupt driver motor supply independently of software | Quote required / existing |
| B17 | 1 set | Fuse holder; initial 1.5 A time-delay fuse | Protect tested motor circuit wiring | Quote required / existing |
| B18 | 1 set | Perfboard headers terminals shielded/twisted sensor wire | Secure low-voltage wiring and strain relief | Quote required / existing |
| B19 | 1 set | 100 nF ceramic; 470 uF 25 V electrolytic | Initial local bypass and motor-rail bulk capacitance | Quote required / existing |
| B20 | 1 assembly | One detached manual-wheelchair caster assembly | Selected caster format and healthy reference | Quote required / existing |
| B21 | 1 assembly | About 40 mm roller; 8 mm supported shaft | Drive wheel contact without gearbox radial preload | Quote required / existing |
| B22 | 2 bearings and blocks | 608-2RS nominal 8 x 22 x 7 mm with mounting blocks | Support independent roller shaft | Quote required / existing |
| B23 | 1 coupling | Flexible 4 mm to 8 mm shaft coupling | Connect motor to supported roller shaft | Quote required / existing |
| B24 | 1 fixture set | Rigid base; caster holder; guided reaction carriage | Separate horizontal and vertical load paths | Quote required / existing |
| B25 | 1 set | Guard; overload stops; retainers; fasteners | Protect fingers sensors and moving assemblies | Quote required / existing |
| B26 | 1 disk | Removable thin 12-slot disk with guarded mount | Caster rotation measurement | Quote required / existing |
| B27 | 1 set | Known horizontal forces and vertical masses | Force calibration and light normal preload | Quote required / existing |

## Optional and existing items

| ID | Purchase quantity | Reference part or specification | Purpose | Observed USD unit/package price |
|---|---|---|---|---|
| B09 | 1 pair package | [1997 4 mm shaft M3 hub pair](https://www.pololu.com/product/1997) | Only if chosen roller construction needs a motor hub | $10.95 |
| B28 | 1 device | BLE-capable phone or laptop | Test UI and service records | Quote required / existing |
| B29 | 1 set | Multimeter logic analyzer and soldering tools | Voltage pulse timing and interconnect verification | Quote required / existing |

## Price interpretation

- Known-price **required** purchase packages subtotal: **USD 106.05**.
- Known-price **optional** packages: **USD 10.95**.
- Combined partial reference subtotal: **USD 117.00**.
- This is **not a full build total**: DK, two HX711 boards, 10 kg cell, optics, power, fixture and most consumables remain unpriced. Empty prices are not zero. Taxes, shipping and imports are excluded.
- Pair-package prices include both supplied units even where only one is consumed. B09 is optional and should be omitted when the selected shaft-coupling construction does not use it.
- Prices are observed reference listings, not current checkout quotes. Do not convert them into an assumed Indian landed price. See [India sourcing entry points](../docs/RESEARCH.md#procurement-evidence-and-limits).

## Why these choices

**One DK and one small model.** The Nordic board handles sensing, condition checks, local inference and BLE. CPU inference is the reference; Axon deployment is conditional on the supported model/toolchain. No external AI computer or second radio node is required.

**ADXL345 over SPI.** This is a practical low-cost class of sensor for gross vibration experiments. Use the named breakout and a modest starting sample rate. It cannot establish ultrasonic bearing health. Higher sample rates require checking actual signal quality and SPI throughput.

**Two different force ranges.** A small drag force is poorly matched to using a single large-capacity weighing cell for everything. The 500 g cell is for the horizontal reaction; the 10 kg cell is for applied normal load. Two dedicated HX711 boards avoid multiplexing incompatible timing/gain paths. Mechanical cross-talk and actual resolution must still be measured.

**Low-power motor plus driver.** The 12 V LP motor's published stall estimate is 0.9 A, while the selected driver carrier is around 1.3 A continuous under stated conditions. A stronger 37D motor is not a drop-in substitute. Stall current is not a safe continuous operating current.

**Actual caster speed.** The integrated encoder measures the drive shaft, not the caster. A separate optical disk/sensor is included to detect roller slip. A slotted target is passive; it does not add a second controller.

**Supported roller shaft.** Two external bearings carry the contact load. The coupling transmits torque from the 4 mm motor shaft to the independent 8 mm roller shaft. This avoids assuming the gearbox shaft can carry the caster preload.

## Compatibility gates before purchase or connection

1. Configure and measure DK GPIO supply at 3.3 V. Its default is 1.8 V; a 3.3 V sensor list is not automatically compatible with the default board setting.
2. Feed motor encoder Vcc from 5 V, then reduce A/B outputs using the specified dividers. The encoder is not rated for 3.3 V supply.
3. Use HX711 boards with separate VCC and VDD. Plan analog VCC at 5 V and digital VDD at 3.3 V; verify jumpers and the purchased board revision.
4. Confirm the actual sensor supply-current budget and regulator arrangements. Never parallel two regulated 3.3 V outputs or backfeed USB.
5. Verify the motor current, shaft bores, bracket dimensions and actual caster dimensions before ordering mechanical parts.
6. Protect the 500 g cell with mechanical stops. Begin with a detached caster and light load. Neither the 10 kg sensor nor this documentation certifies the fixture for occupied-chair testing.

Read [interfaces](INTERFACES.md) and [mechanical design](MECHANICAL.md) for the integration assumptions. Source references and research limits are in [RESEARCH.md](../docs/RESEARCH.md). Full procurement readiness is pending mechanical review, quotations and bench checks.
