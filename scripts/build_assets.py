"""Generate the initial BOM and exact SVG block diagram from maintained records."""
from pathlib import Path
import csv
from decimal import Decimal
from html import escape

ROOT=Path(__file__).resolve().parents[1]
# quantity is the purchase quantity; pack contents are stated explicitly.
ROWS=[
('B01', 'Required', 'Controller', 'Nordic Semiconductor', 'NRF54LM20-DK', 1, 'board', 'Main controller; CPU inference and optional Axon; BLE', 'USB power; configure and measure 3.3 V nRF GPIO supply', '45.00', 'Published USD qty-1 price; checked 2026-10-26; excludes delivery/tax', 'https://www.digikey.com/en/products/detail/nordic-semiconductor-asa/NRF54LM20-DK/27685498'),
('B02', 'Required', 'Vibration sensor', 'Adafruit', '1231 ADXL345 breakout', 1, 'board', 'Caster-fork vibration; SPI', 'Use 3.3 V interface; start 800 samples/s; verify purchased revision', '17.50', 'Published USD qty-1 package price rechecked 2026-10-26; not a landed India price', 'https://www.adafruit.com/product/1231'),
('B03', 'Required', 'Drag force sensor', 'SparkFun', 'SEN-14728 TAL221 500 g', 1, 'cell', 'Horizontal reaction force under light preload', 'Nominal range about 4.90 N; use calibrated linkage and overload stops', '15.50', 'Published USD qty-1 package price rechecked 2026-10-26; not a landed India price', 'https://www.sparkfun.com/mini-load-cell-500g-straight-bar-tal221.html'),
('B04', 'Required', 'Normal force sensor', 'SparkFun', 'SEN-13329 TAL220 10 kg', 1, 'cell', 'Measure applied contact load independently', 'Initial target around 10 N; capacity is not fixture rating', '12.95', 'Published USD qty-1 price; checked 2026-10-26; excludes delivery/tax', 'https://www.sparkfun.com/load-cell-10kg-straight-bar-tal220.html'),
('B05', 'Required', 'Load-cell ADC', 'SparkFun', 'SEN-13879 HX711 separate VCC and VDD', 2, 'boards', 'One converter per force channel', 'VCC 5 V; VDD 3.3 V; separate clocks/data; default 10 samples/s', '4.95', 'Published USD qty-1 price; checked 2026-10-26; excludes delivery/tax', 'https://www.sparkfun.com/sparkfun-load-cell-amplifier-hx711.html'),
('B06', 'Required', 'Drive motor and encoder', 'Pololu', '4886 75:1 25D LP 12 V with 48 CPR encoder', 1, 'motor', 'Low-speed roller drive and roller RPM', '4 mm D shaft; 75 RPM no load; 0.9 A stall estimate; encoder powered 5 V', '53.95', 'Published USD qty-1 package price rechecked 2026-10-26; not a landed India price', 'https://www.pololu.com/product/4886'),
('B07', 'Required', 'Motor driver', 'Pololu', '4036 DRV8876 carrier', 1, 'board', 'PWM speed control and local disable', '12 V motor supply; 3.3 V logic; around 1.3 A continuous under vendor conditions', '8.15', 'Published USD qty-1 package price rechecked 2026-10-26; not a landed India price', 'https://www.pololu.com/product/4036'),
('B08', 'Required', 'Motor bracket', 'Pololu', '2676 25D bracket pair', 1, 'pair package', 'Correct motor mounting', 'Two brackets supplied; use one; verify screw engagement', '10.95', 'Published USD qty-1 package price rechecked 2026-10-26; not a landed India price', 'https://www.pololu.com/product/2676'),
('B09', 'Optional', 'Motor hub', 'Pololu', '1997 4 mm shaft M3 hub pair', 1, 'pair package', 'Only if chosen roller construction needs a motor hub', 'Do not confuse with an 8 mm shaft hub; coupling route may make this unnecessary', '10.95', 'Published USD qty-1 package price rechecked 2026-10-26; not a landed India price', 'https://www.pololu.com/product/1997'),
('B10', 'Required', 'Caster speed sensor', 'Vishay', 'TCST2103 photointerrupter', 1, 'sensor', 'Independent actual wheel rotation and slip check', 'Bare phototransistor output; 3.3 V pull-up; LED resistor required', '1.84', 'Published USD qty-1 price; checked 2026-10-26; excludes delivery/tax', 'https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/TCST2103/2354849'),
('B11', 'Required', 'Encoder level reduction', 'YAGEO', '15 kOhm and 22 kOhm 1% resistors', 2, 'divider sets', 'Reduce motor encoder A and B from 5 V to about 2.97 V', 'Each set contains one resistor of each value; test pulse edges', '0.20', 'Published component prices; one 15k + one 22k per divider at $0.10 each; two sets $0.40', 'https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-15K/13252'),
('B12', 'Required', 'Pull-ups and emitter resistor', 'YAGEO', '10 kOhm 1% and 220 Ohm 0.25 W', 1, 'set', 'Optical detector; driver FAULT; optical LED current', 'Two 10 kOhm pull-ups plus one 220 Ohm LED resistor; verify LED current', '0.30', 'Published component prices; two 10k and one 220R at $0.10 each; set $0.30', 'https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-10K/13219'),
('B13', 'Required', 'Motor supply', 'Adafruit', '352 enclosed 12 V 5 A supply', 1, 'supply', 'Separate motor power', 'Match connector; current limit/fuse sized after startup measurement', '24.95', 'Published USD price; out of stock; local mains plug/adapter extra if required', 'https://www.adafruit.com/product/352'),
('B14', 'Required', 'Auxiliary supply', 'Adafruit', '1994 regulated 5 V 2 A USB-A supply', 1, 'supply', 'Encoder and HX711 analog rail', 'Common low-voltage ground; prevent USB backfeed; never parallel outputs', '7.95', 'Published USD price; out of stock; USB power breakout included in B18 allowance', 'https://www.adafruit.com/product/1994'),
('B15', 'Required', 'DK cable', 'Adafruit', '4473 USB-A to USB-C data cable, 0.3 m', 1, 'cable', 'DK power programming and development logs', 'Check connector on received revision; use a data cable', '3.95', 'Published USD qty-1 price; checked 2026-10-26; excludes delivery/tax', 'https://www.adafruit.com/product/4473'),
('B16', 'Required', 'Hardware stop', 'Fuji Electric / AutomationDirect', 'AR22V0R-01R latching 1NC emergency stop', 1, 'switch', 'Interrupt driver motor supply independently of software', 'Positive-opening NC; published DC-13 rating 4 A at 24 V; confirm purchased revision and suitability for 12 V motor inrush; physical supply interruption', '26.00', 'Published USD catalog price, page 1; 22 mm panel mount; enclosure/mount covered in B25 allowance', 'https://cdn.automationdirect.com/static/specs/fuji22mmestoppb.pdf'),
('B17', 'Required', 'Power protection', 'Locally sourced', 'Fuse holder; initial 1.5 A time-delay fuse', 1, 'set', 'Protect tested motor circuit wiring', 'Provisional fuse size; verify startup and conductor ratings; not stall protection', '', 'Estimate only: Allowance for a matched inline holder and 1.5 A time-delay fuse; no exact SKU selected.', ''),
('B18', 'Required', 'Prototyping interconnect', 'Locally sourced', 'Perfboard headers terminals shielded/twisted sensor wire', 1, 'set', 'Secure low-voltage wiring and strain relief', 'No motor current through solderless breadboard; label signal grounds', '', 'Estimate only: Allowance for perfboard, headers, terminals, twisted sensor leads, USB-A power breakout/cable, DC jack and strain relief.', ''),
('B19', 'Required', 'Decoupling', 'Vishay / Panasonic', '3 x Vishay K104K15X7RF5TL2 100 nF + 1 x Panasonic ECA-1EM471 470 uF 25 V', 1, 'set', 'Initial local bypass and motor-rail bulk capacitance', 'At least three ceramics and one bulk capacitor; validate transients', '1.55', 'Published prices: 3 x $0.31 + $0.62 = $1.55; exact links in pricing evidence', 'https://www.digikey.com/en/products/detail/panasonic-industry/ECA-1EM471/245014'),
('B20', 'Required', 'Reference test article', 'ALCO', 'AL-90535 complete 8 x 1 inch caster assembly', 1, 'assembly', 'Selected caster format and healthy reference', 'Measure dimensions before ordering custom hardware; baseline requires inspection', '52.95', 'Published USD listing; includes wheel, fork, axle/nut, journal bearing, dust cap and locknut; not wheel-only price', 'https://alcosales.com/wheels/wheelchair-wheels/wheelchair-caster-assemblies-forks/'),
('B21', 'Required', 'Roller and shaft', 'Custom fabricated', 'About 40 mm roller; 8 mm supported shaft', 1, 'assembly', 'Drive wheel contact without gearbox radial preload', 'Width and retention sized to caster; dimensions subject to mechanical review', '', 'Estimate only: Allowance for one fabricated 40 mm roller, 8 mm shaft and retention; dimensions and machining not yet quoted.', ''),
('B22', 'Required', 'Roller bearings', 'Locally sourced', '608-2RS nominal 8 x 22 x 7 mm with mounting blocks', 2, 'bearings and blocks', 'Support independent roller shaft', 'Check purchased bearing dimensions; retained shaft; include two suitable mounts', '', 'Estimate only: Allowance per bearing-and-mount unit; two units $30.00. Not a bare-bearing catalog price.', ''),
('B23', 'Required', 'Motor coupling', 'Tinkersphere', 'Flexible 4 mm to 8 mm shaft coupling', 1, 'coupling', 'Connect motor to supported roller shaft', 'Check real bore tolerances; guard coupling; no wheel load on motor shaft', '5.99', 'Published USD qty-1 price; checked 2026-10-26; excludes delivery/tax', 'https://tinkersphere.com/3d-printer-parts/4324-shaft-coupler-4mm-to-8mm.html'),
('B24', 'Required', 'Carriage and load paths', 'Custom fabricated', 'Rigid base; caster holder; guided reaction carriage', 1, 'fixture set', 'Separate horizontal and vertical load paths', 'Includes two force-cell mounts; alignment adjustment; cross-talk calibration', '', 'Estimate only: Allowance for base, guided carriage, caster holder and force-cell brackets; labor, travel and local shop pricing unverified.', ''),
('B25', 'Required', 'Mechanical protection', 'Custom fabricated', 'Guard; overload stops; retainers; fasteners', 1, 'set', 'Protect fingers sensors and moving assemblies', 'Protect 500 g cell from assembly overload and bypass loads', '', 'Estimate only: Allowance for guard, stop-switch mounting, overload stops and fasteners.', ''),
('B26', 'Required', 'Optical target', 'Custom fabricated', 'Removable thin 12-slot disk with guarded mount', 1, 'disk', 'Caster rotation measurement', 'Fits TCST2103 3.1 mm slot; count wheel not roller; do not modify a user chair', '', 'Estimate only: Allowance for thin 12-slot disk and mount; final CAD and fabrication method not yet selected.', ''),
('B27', 'Required', 'Calibration and preload', 'Existing calibrated masses or checked standards', 'Known horizontal forces and vertical masses', 1, 'set', 'Force calibration and light normal preload', 'Include fixture mass in load calculation; initial preload target about 10 N', '', 'Estimate only: Allowance for checked masses/hangers and preload; not a certified calibration-weight quote.', ''),
('B28', 'Existing tool', 'BLE client', 'Existing device', 'BLE-capable phone or laptop', 1, 'device', 'Test UI and service records', 'Confirm client support; browser BLE is not universal', '', 'Reuse assumption: $0 additional cash if available; ownership/access not confirmed; replacement purchase excluded', ''),
('B29', 'Existing tool', 'Bring-up tools', 'Existing lab equipment', 'Multimeter logic analyzer and soldering tools', 1, 'set', 'Voltage pulse timing and interconnect verification', 'Logic analyzer inputs must tolerate observed signals; add calibrated force reference', '', 'Reuse assumption: $0 additional cash if available; ownership/access not confirmed; replacement purchase excluded', ''),
]
ALLOWANCES = {'B17': ('5.00', 'Allowance for a matched inline holder and 1.5 A time-delay fuse; no exact SKU selected.'), 'B18': ('15.00', 'Allowance for perfboard, headers, terminals, twisted sensor leads, USB-A power breakout/cable, DC jack and strain relief.'), 'B21': ('25.00', 'Allowance for one fabricated 40 mm roller, 8 mm shaft and retention; dimensions and machining not yet quoted.'), 'B22': ('15.00', 'Allowance per bearing-and-mount unit; two units $30.00. Not a bare-bearing catalog price.'), 'B24': ('60.00', 'Allowance for base, guided carriage, caster holder and force-cell brackets; labor, travel and local shop pricing unverified.'), 'B25': ('20.00', 'Allowance for guard, stop-switch mounting, overload stops and fasteners.'), 'B26': ('5.00', 'Allowance for thin 12-slot disk and mount; final CAD and fabrication method not yet selected.'), 'B27': ('20.00', 'Allowance for checked masses/hangers and preload; not a certified calibration-weight quote.')}
HEADER=['id','scope','function','manufacturer','reference_part','quantity','purchase_unit','purpose','compatibility_notes','observed_unit_price_usd','price_status','source_url','estimated_unit_budget_usd','budget_line_total_usd']
def amount(r):
    return Decimal(r[9] or ALLOWANCES.get(r[0],('0',''))[0])
with (ROOT/'hardware/BOM.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(HEADER)
    for r in ROWS:
        w.writerow(list(r)+[ALLOWANCES.get(r[0],('',''))[0],f'{amount(r)*r[5]:.2f}'])

def line(r):
    part=f'[{r[4]}]({r[11]})' if r[11] else r[4]
    if r[9]:
        price='$'+r[9];basis='Published listing'
    elif r[0] in ALLOWANCES:
        price='$'+ALLOWANCES[r[0]][0];basis='Estimate; not a supplier price'
    else:
        price='$0.00';basis='Reuse assumption; replacement excluded'
    return f'| {r[0]} | {r[5]} {r[6]} | {part} | {price} | ${amount(r)*r[5]:.2f} | {basis} |'

required=sum(Decimal(r[9])*r[5] for r in ROWS if r[9] and r[1]=='Required')
estimated=sum(amount(r)*r[5] for r in ROWS if r[0] in ALLOWANCES)
optional=sum(Decimal(r[9])*r[5] for r in ROWS if r[9] and r[1]=='Optional')
txt='''# Bill of materials and prototype budget

**CasterCare — Sustain the System hardware application.** Prices researched: 26 October 2026. Currency: **USD**, before shipping, tax, customs and currency conversion.

This BOM covers one controller and a light-load, detached-caster bench prototype. **Published listing** means the named supplier displayed that price for the specified part or package. **Estimate** is a planning allowance, not an observed price or quotation. Custom fabrication has no correct fixed price until dimensions, materials and labor are agreed with a shop. No purchases have been made.

All old “Quote required / existing” cells are replaced with an explicit price or budget basis. Estimates remain visibly separate from verified supplier prices, including in the CSV. Prices do not establish stock availability or compatibility by themselves.

## What to buy first

Start with B01–B05 for voltage checks, sensor capture and force calibration. Finalize the caster and load-path design before ordering the mechanical items. The motor and driver are a matched reference pair. The DK is priced at its normal purchase cost; do not assume free hardware until the contest awards it.

## Required parts and fabrication

Unit prices are per **purchase unit**, including packs. The line total already multiplies by the purchase quantity.

| ID | Purchase quantity | Reference part or specification | Unit/package USD | Line total USD | Price basis |
|---|---|---|---:|---:|---|
'''
txt+='\n'.join(line(r) for r in ROWS if r[1]=='Required')
txt+='''

## Optional and reused equipment

| ID | Purchase quantity | Reference part or specification | Unit/package USD | Line total USD | Price basis |
|---|---|---|---:|---:|---|
'''
txt+='\n'.join(line(r) for r in ROWS if r[1]!='Required')
txt+=f'''

## Totals

| Cost category | USD |
|---|---:|
| Required parts with published prices | {required:.2f} |
| Estimated fabrication and consumable allowances | {estimated:.2f} |
| **Required prototype planning budget** | **{required+estimated:.2f}** |
| Optional B09 hub package | {optional:.2f} |
| Planning budget with optional hub | {required+estimated+optional:.2f} |
| Required budget if the contest supplies B01 free | {required+estimated-Decimal('45'):.2f} |

The planning budget is **not a verified checkout total**. Only the published-price subtotal is backed by listings. No contingency is included; custom work can exceed the allowances. Taxes, delivery, imports, currency conversion, and replacement phone/laptop/lab tools are excluded. $0 for B28/B29 means conditional reuse, not a claim that Mathew owns these items or that they are free to buy. B27 calibration supplies are budgeted separately.

The B13 and B14 reference supplies displayed out of stock when checked; their listed prices are reference prices, not immediately available purchase offers. Pololu motor/driver backorders were allowed. Verify delivery before ordering. A local supply substitute requires the same voltage, adequate current, documented mains safety and correct connectors.

## Price evidence and exact package contents

- **B01:** DigiKey lists the NRF54LM20-DK at $45.00 for one board. Contest supply is a separate conditional scenario, not the normal retail price.
- **B02–B09:** Named Adafruit, SparkFun and Pololu product links above are the price sources. B05 is **2 × $4.95 = $9.90**, not the higher price of some resellers. B08 and optional B09 are pair packages; buy one package each, not two.
- **B10:** DigiKey TCST2103 quantity-one price is $1.84. This is the bare sensor; the resistor circuit is separate.
- **B11:** Two [YAGEO MFR-25FBF52-15K](https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-15K/13252) plus two [MFR-25FBF52-22K](https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-22K/9138098), each $0.10 at quantity one. Four resistors total $0.40. Each divider set costs $0.20.
- **B12:** Two [MFR-25FBF52-10K](https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-10K/13219) and one [MFR-25FBF52-220R](https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-220R/9138097), each $0.10, total $0.30. Resistors are 1%, 0.25 W. Higher-volume discounts were not assumed.
- **B13–B15:** Adafruit 352 is $24.95; 1994 is $7.95; data cable 4473 is $3.95. The 5 V supply needs a USB-A breakout/pigtail, budgeted under B18; never connect mains wiring on perfboard. Local mains plug adaptation is excluded if needed.
- **B16:** AutomationDirect's [Fuji catalog, page 1](https://cdn.automationdirect.com/static/specs/fuji22mmestoppb.pdf) lists the complete AR22V0R-01R at $26.00. Page 4 lists the relevant AR22 V0R-series DC contact rating. This is a panel device; mounting is included in B25's allowance. Review actual motor inrush and contact suitability before use; do not infer a DC motor rating from an AC-only switch listing.
- **B19:** Three [Vishay K104K15X7RF5TL2, 100 nF 50 V](https://www.digikey.com/en/products/detail/vishay-beyschlag-draloric-bc-components/K104K15X7RF5TL2/286538) at $0.31 plus one [Panasonic ECA-1EM471, 470 uF 25 V](https://www.digikey.com/en/products/detail/panasonic-industry/ECA-1EM471/245014) at $0.62 = **$1.55**. These are quantity-one unit prices, not reel prices.
- **B20:** ALCO lists AL-90535 at $52.95 for the complete 8 × 1 inch assembly, including the fork and journal bearing. It is a bench reference option; confirm mounting dimensions before fabrication. A $36 wheel-only listing was not used as an assembly price.
- **B23:** Tinkersphere lists the aluminum flexible 4-to-8 mm coupler at $5.99 each. Confirm bores against the purchased shafts.

These are publicly displayed supplier prices checked on the research date, including some indexed/cached page content. Final regional checkout prices and availability can change. This is a multi-supplier reference BOM, not an Indian landed-cost quote. See [India sourcing entry points](../docs/RESEARCH.md#procurement-evidence-and-limits).

## Explicit estimate and reuse assumptions

The following numbers are author planning assumptions. No supplier price is claimed for them; there is no source URL because no matching finished product or fabrication quote has been selected.

'''
for i,(price,note) in ALLOWANCES.items():
    txt+=f'- **{i}:** ${price} per purchase unit. {note}\n'
txt+='''
- **B28:** $0 additional cash only if a compatible phone/laptop is available. No new device purchase is included.
- **B29:** $0 additional cash only if suitable lab tools can be borrowed or reused. Access is not yet confirmed.

'''
txt+='''## Why these choices

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

Read [interfaces](INTERFACES.md) and [mechanical design](MECHANICAL.md) for the integration assumptions. Source references and research limits are in [RESEARCH.md](../docs/RESEARCH.md). Full procurement readiness is pending mechanical review, confirmation of estimated costs and bench checks.
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
