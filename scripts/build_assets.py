"""Generate the initial BOM and exact SVG block diagram from maintained records."""
from pathlib import Path
import csv
from decimal import Decimal
from html import escape

ROOT=Path(__file__).resolve().parents[1]
# quantity is the purchase quantity; pack contents are stated explicitly.
ROWS=[
('B01','Required','Controller','Nordic Semiconductor','NRF54LM20-DK',1,'board','Main controller; CPU inference and optional Axon; BLE','USB power; configure and measure 3.3 V nRF GPIO supply','','Quote required; request through contest or distributor','https://www.nordicsemi.com/Products/Development-hardware/nRF54LM20-DK'),
('B02','Required','Vibration sensor','Adafruit','1231 ADXL345 breakout',1,'board','Caster-fork vibration; SPI','Use 3.3 V interface; start 800 samples/s; verify purchased revision','17.50','Observed manufacturer/reference listing USD; recheck','https://www.adafruit.com/product/1231'),
('B03','Required','Drag force sensor','SparkFun','SEN-14728 TAL221 500 g',1,'cell','Horizontal reaction force under light preload','Nominal range about 4.90 N; use calibrated linkage and overload stops','15.50','Observed reference listing USD; recheck','https://www.sparkfun.com/mini-load-cell-500g-straight-bar-tal221.html'),
('B04','Required','Normal force sensor','SparkFun','SEN-13329 TAL220 10 kg',1,'cell','Measure applied contact load independently','Initial target around 10 N; capacity is not fixture rating','','Quote required','https://www.sparkfun.com/load-cell-10kg-straight-bar-tal220.html'),
('B05','Required','Load-cell ADC','SparkFun','SEN-13879 HX711 separate VCC and VDD',2,'boards','One converter per force channel','VCC 5 V; VDD 3.3 V; separate clocks/data; default 10 samples/s','','Quote required','https://www.sparkfun.com/sparkfun-load-cell-amplifier-hx711.html'),
('B06','Required','Drive motor and encoder','Pololu','4886 75:1 25D LP 12 V with 48 CPR encoder',1,'motor','Low-speed roller drive and roller RPM','4 mm D shaft; 75 RPM no load; 0.9 A stall estimate; encoder powered 5 V','53.95','Observed manufacturer listing USD; stock/backorder recheck','https://www.pololu.com/product/4886'),
('B07','Required','Motor driver','Pololu','4036 DRV8876 carrier',1,'board','PWM speed control and local disable','12 V motor supply; 3.3 V logic; around 1.3 A continuous under vendor conditions','8.15','Observed manufacturer listing USD; recheck','https://www.pololu.com/product/4036'),
('B08','Required','Motor bracket','Pololu','2676 25D bracket pair',1,'pair package','Correct motor mounting','Two brackets supplied; use one; verify screw engagement','10.95','Observed manufacturer package price USD; recheck','https://www.pololu.com/product/2676'),
('B09','Optional','Motor hub','Pololu','1997 4 mm shaft M3 hub pair',1,'pair package','Only if chosen roller construction needs a motor hub','Do not confuse with an 8 mm shaft hub; coupling route may make this unnecessary','10.95','Observed manufacturer package price USD; optional','https://www.pololu.com/product/1997'),
('B10','Required','Caster speed sensor','Vishay','TCST2103 photointerrupter',1,'sensor','Independent actual wheel rotation and slip check','Bare phototransistor output; 3.3 V pull-up; LED resistor required','','Quote required','https://www.vishay.com/docs/81147/tcst2103.pdf'),
('B11','Required','Encoder level reduction','Generic specified values','15 kOhm and 22 kOhm 1% resistors',2,'divider sets','Reduce motor encoder A and B from 5 V to about 2.97 V','Each set contains one resistor of each value; test pulse edges','','Local quote; values are design choices',''),
('B12','Required','Pull-ups and emitter resistor','Generic specified values','10 kOhm 1% and 220 Ohm 0.25 W',1,'set','Optical detector; driver FAULT; optical LED current','Two 10 kOhm pull-ups plus one 220 Ohm LED resistor; verify LED current','','Local quote; values are design choices',''),
('B13','Required','Motor supply','Locally sourced certified unit','Enclosed regulated 12 V DC at least 2 A',1,'supply','Separate motor power','Match connector; current limit/fuse sized after startup measurement','','Quote required; not a selected vendor product',''),
('B14','Required','Auxiliary supply','Bench supply or documented regulator','Regulated 5 V at least 0.5 A',1,'supply','Encoder and HX711 analog rail','Common low-voltage ground; prevent USB backfeed; never parallel outputs','','Quote required or reuse existing suitable supply',''),
('B15','Required','DK cable','Suitable USB data cable','Connector matched to actual DK',1,'cable','DK power programming and development logs','Check connector on received revision; use a data cable','','Quote required or reuse',''),
('B16','Required','Hardware stop','Locally sourced DC-rated unit','Normally closed emergency stop / latching stop',1,'switch','Interrupt driver motor supply independently of software','DC voltage and current rating suitable for motor circuit; accessible outside guard','','Quote required',''),
('B17','Required','Power protection','Locally sourced','Fuse holder; initial 1.5 A time-delay fuse',1,'set','Protect tested motor circuit wiring','Provisional fuse size; verify startup and conductor ratings; not stall protection','','Quote required',''),
('B18','Required','Prototyping interconnect','Locally sourced','Perfboard headers terminals shielded/twisted sensor wire',1,'set','Secure low-voltage wiring and strain relief','No motor current through solderless breadboard; label signal grounds','','Quote required',''),
('B19','Required','Decoupling','Generic specified values','100 nF ceramic; 470 uF 25 V electrolytic',1,'set','Initial local bypass and motor-rail bulk capacitance','At least three ceramics and one bulk capacitor; validate transients','','Local quote; starting values not final EMC design',''),
('B20','Required','Reference test article','Reused or locally sourced','One detached manual-wheelchair caster assembly',1,'assembly','Selected caster format and healthy reference','Measure dimensions before ordering custom hardware; baseline requires inspection','','Quote required or reuse with permission',''),
('B21','Required','Roller and shaft','Custom fabricated','About 40 mm roller; 8 mm supported shaft',1,'assembly','Drive wheel contact without gearbox radial preload','Width and retention sized to caster; dimensions subject to mechanical review','','Local fabrication quote required',''),
('B22','Required','Roller bearings','Locally sourced','608-2RS nominal 8 x 22 x 7 mm with mounting blocks',2,'bearings and blocks','Support independent roller shaft','Check purchased bearing dimensions; retained shaft; include two suitable mounts','','Local quote required',''),
('B23','Required','Motor coupling','Locally sourced','Flexible 4 mm to 8 mm shaft coupling',1,'coupling','Connect motor to supported roller shaft','Check real bore tolerances; guard coupling; no wheel load on motor shaft','','Local quote required',''),
('B24','Required','Carriage and load paths','Custom fabricated','Rigid base; caster holder; guided reaction carriage',1,'fixture set','Separate horizontal and vertical load paths','Includes two force-cell mounts; alignment adjustment; cross-talk calibration','','Local fabrication quote required',''),
('B25','Required','Mechanical protection','Custom fabricated','Guard; overload stops; retainers; fasteners',1,'set','Protect fingers sensors and moving assemblies','Protect 500 g cell from assembly overload and bypass loads','','Local quote required',''),
('B26','Required','Optical target','Custom fabricated','Removable thin 12-slot disk with guarded mount',1,'disk','Caster rotation measurement','Fits TCST2103 3.1 mm slot; count wheel not roller; do not modify a user chair','','Local fabrication quote required',''),
('B27','Required','Calibration and preload','Existing calibrated masses or checked standards','Known horizontal forces and vertical masses',1,'set','Force calibration and light normal preload','Include fixture mass in load calculation; initial preload target about 10 N','','Quote required or reuse suitable checked masses',''),
('B28','Existing tool','BLE client','Existing device','BLE-capable phone or laptop',1,'device','Test UI and service records','Confirm client support; browser BLE is not universal','','Existing equipment; no new purchase assumed',''),
('B29','Existing tool','Bring-up tools','Existing lab equipment','Multimeter logic analyzer and soldering tools',1,'set','Voltage pulse timing and interconnect verification','Logic analyzer inputs must tolerate observed signals; add calibrated force reference','','Existing equipment; quote if unavailable',''),
]
HEADER=['id','scope','function','manufacturer','reference_part','quantity','purchase_unit','purpose','compatibility_notes','observed_unit_price_usd','price_status','source_url']
with (ROOT/'hardware/BOM.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(HEADER);w.writerows(ROWS)

def line(r):
    price=('$'+r[9]) if r[9] else 'Quote required / existing'
    part=f'[{r[4]}]({r[11]})' if r[11] else r[4]
    return f'| {r[0]} | {r[5]} {r[6]} | {part} | {r[7]} | {price} |'

required=sum(Decimal(r[9])*r[5] for r in ROWS if r[9] and r[1]=='Required')
optional=sum(Decimal(r[9])*r[5] for r in ROWS if r[9] and r[1]=='Optional')
txt='''# Initial bill of materials

**CasterCare — Sustain the System hardware application.** Research date: 26 October 2026.

This is the beginning BOM for a single-controller, light-load bench prototype. It explicitly includes the **Nordic nRF54LM20 DK**. The selections are researched reference parts, not a claim that the system has been assembled or tested. Custom items still require dimensions and quotations. No purchases have been made.

## What to buy first

Start with B01–B05 for voltage checks, sensor capture and force calibration. Finalize the caster and load-path design before ordering B20–B27. The motor/driver are a matched reference pair, not an invitation to substitute a higher-current motor. Basic motor tests can proceed separately, guarded and unloaded.

## Required reference parts and fabrication

| ID | Purchase quantity | Reference part or specification | Purpose | Observed USD unit/package price |
|---|---|---|---|---|
'''
txt+='\n'.join(line(r) for r in ROWS if r[1]=='Required')
txt+='''

## Optional and existing items

| ID | Purchase quantity | Reference part or specification | Purpose | Observed USD unit/package price |
|---|---|---|---|---|
'''
txt+='\n'.join(line(r) for r in ROWS if r[1]!='Required')
txt+=f'''

## Price interpretation

- Known-price **required** purchase packages subtotal: **USD {required:.2f}**.
- Known-price **optional** packages: **USD {optional:.2f}**.
- Combined partial reference subtotal: **USD {required+optional:.2f}**.
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
'''
(ROOT/'hardware/BOM.md').write_text(txt)

# Exact, code-native diagram; no generated imagery or implied wiring pin assignment.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1120" viewBox="0 0 1200 1120" role="img" aria-labelledby="title desc">',
'<title id="title">CasterCare proposed system architecture</title>',
'<desc id="desc">One Nordic development kit reads vibration, two forces and independent speeds, controls a guarded roller, and communicates results by Bluetooth. This is not a wiring schematic.</desc>',
'<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#476078"/></marker></defs>',
'<rect width="1200" height="1120" fill="#f6f8fb"/>',
'<style>text{font-family:Arial,sans-serif;fill:#172b40}.title{font-size:32px;font-weight:700}.head{font-size:20px;font-weight:700}.body{font-size:17px}.note{font-size:15px;fill:#496077}.wire{fill:none;stroke:#476078;stroke-width:2.5;marker-end:url(#arrow)}</style>',
'<text class="title" x="48" y="55">CasterCare</text><text class="body" x="48" y="87">Proposed bench prototype • one controller • one compact anomaly model</text>']
def box(x,y,w,h,title,lines,fill='#ffffff'):
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="#bdcbd8"/>')
    svg.append(f'<text class="head" x="{x+18}" y="{y+31}">{escape(title)}</text>')
    for i,l in enumerate(lines):svg.append(f'<text class="body" x="{x+18}" y="{y+61+i*25}">{escape(l)}</text>')
def wire(path):svg.append(f'<path class="wire" d="{path}"/>')
box(48,130,340,150,'Vibration',['ADXL345 on caster fork','SPI and data-ready','3.3 V interface'])
box(430,130,340,150,'Two force channels',['500 g drag + 10 kg normal','One HX711 for each cell','5 V analog / 3.3 V logic'])
box(812,130,340,150,'Independent speed',['Drive encoder: 5 V + dividers','Caster: optical disk sensor','Compare motion to detect slip'])
box(300,365,600,205,'Nordic nRF54LM20 DK',['CPU: speed, load, slip and data-quality checks','One compact vibration anomaly model','CPU reference; Axon evaluated if supported','3.3 V GPIO configuration must be verified'],'#e9f1fb')
wire('M218 280 V325 H400 V365');wire('M600 280 V365');wire('M982 280 V325 H800 V365')
box(48,655,340,145,'Nearby phone or laptop',['BLE commands and status','Compact results and history','Raw export only on request'])
box(430,655,340,145,'Motor control',['DRV8876 driver','12 V LP gearmotor','Flexible 4 mm to 8 mm coupling'])
box(812,655,340,145,'Test and report',['Reject invalid conditions','Confirm suspicious test once','Inspect, service and retest'])
wire('M380 570 V610 H218 V655');wire('M600 570 V655');wire('M820 570 V610 H982 V655')
box(240,875,720,140,'Guarded roller fixture',['Separate bearing-supported shaft carries caster preload','Physical stop cuts motor power; overload stops protect cells','Start with one detached caster and light measured load'],'#fff4df')
wire('M600 800 V875')
svg.append('<text class="note" x="48" y="1060">Functional diagram only. See hardware/INTERFACES.md for supply domains and unassigned GPIO mapping.</text>')
svg.append('<text class="note" x="48" y="1086">Research/design stage • no assembled prototype or measured performance claimed • 26 October 2026</text></svg>')
(ROOT/'docs/diagrams/system.svg').write_text('\n'.join(svg))
print(f'Generated {len(ROWS)} BOM rows; required known subtotal USD {required}; optional USD {optional}')
