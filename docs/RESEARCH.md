# Research and source register

Checked 26 October 2026. Manufacturer sources support component specifications; research supports the problem and possible methods. None validates this unbuilt fixture. Some papers were assessed from their abstracts rather than full texts.

## Problem and prior work

1. [Wheelchair maintenance and rolling resistance](https://www.resna.org/sites/default/files/conference/2017/wheeled_mobility/Eshraghi.html). Supports investigating objective maintenance outcomes.
2. [Marsh et al., Correlating Wheelchair Usage And Failure Measures For Developing A Wheelchair Maintenance Technology, RESNA 2023](https://www.resna.org/sites/default/files/conference/2023/SeatingandMobility/73_Marsh.html). WheelTrak sensor/app work is relevant prior art; its pilot does not establish our diagnostic performance.
3. [Development, reliability, and piloting of a wheelchair caster failure inspection tool, C-FIT](https://pubmed.ncbi.nlm.nih.gov/30729825/). Useful for understanding inspection criteria and independent condition labels.
4. [Permobil Fleet Management](https://www.permobil.com/en-ca/products/power-wheelchairs/functions/fleet-management). Commercial adjacent work in connected power-wheelchair diagnostics.
5. [Fault detection modeling, EP4681040A1](https://patents.google.com/patent/EP4681040A1/en). Relevant published patent literature. No legal conclusion or novelty claim is made.

## Methods worth reading

6. [Palmer and Bollas, Active fault diagnosis for uncertain systems using optimal test designs and detection through classification, 2019](https://pubmed.ncbi.nlm.nih.gov/30850204/). Supports the principle of designing informative tests under uncertainty. This MVP uses one fixed confirmation repeat, not the paper's full optimization method.
7. [An Adaptable and Unsupervised TinyML Anomaly Detection System for Extreme Industrial Environments, 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9962960/). A reference for constrained-device anomaly detection; it is not a wheelchair model and does not establish Axon compatibility.
8. [Nishida et al., DCASE 2024 Challenge Task 2 description](https://arxiv.org/abs/2406.07250). Useful evaluation principles for normal-data anomaly detection and domain changes. This is an arXiv task-description paper, not direct caster validation.

## Component and integration evidence

| Ref | Source | Decision supported |
|---|---|---|
| N1 | [Nordic DK product](https://www.nordicsemi.com/Products/Development-hardware/nRF54LM20-DK) | Required contest controller |
| N2 | [Nordic power supply](https://docs.nordicsemi.com/r/bundle/ug_nrf54lm20_dk/page/ug/nrf54lm20_dk/hw_desription/power_supply.html?contentId=QDRMnZ3ju3EJ8KL_fVGSGA) | Default 1.8 V; programmable 1.8–3.3 V; VDD:IO follows nRF supply |
| N3 | [Board controller](https://docs.nordicsemi.com/r/bundle/ug_nrf54lm20_dk/page/ug/nrf54lm20_dk/hw_desription/board_control.html) | Board Configurator workflow |
| N4 | [Axon NPU](https://www.nordicsemi.com/Products/Technologies/Edge-AI/Axon-NPU) | Supported-model acceleration to evaluate after CPU reference |
| A1 | [Adafruit 1231](https://www.adafruit.com/product/1231) | Named breakout, SPI interface and 3 V/5 V interfacing |
| A2 | [ADXL345 datasheet, Analog Devices](https://www.analog.com/media/en/technical-documentation/data-sheets/ADXL345.pdf) | Sampling and SPI constraints; high rates need adequate SPI clock |
| F1 | [TAL221 500 g, SparkFun](https://www.sparkfun.com/mini-load-cell-500g-straight-bar-tal221.html) | Low-range horizontal force cell |
| F2 | [TAL220 10 kg, SparkFun](https://www.sparkfun.com/load-cell-10kg-straight-bar-tal220.html) | Separate normal-force measurement |
| F3 | [SparkFun HX711](https://www.sparkfun.com/sparkfun-load-cell-amplifier-hx711.html) | Dedicated bridge converter per force channel |
| F4 | [SparkFun HX711 schematic](https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/SparkFun_HX711_Load_Cell_v11.pdf) | Separate analog/digital supplies and rate jumper |
| M1 | [Pololu 4886](https://www.pololu.com/product/4886) | Low-power motor, 4 mm shaft, encoder supply requirement |
| M2 | [Pololu 4036](https://www.pololu.com/product/4036) | Compatible motor-driver current and logic range; control modes |
| M3 | [Pololu 2676](https://www.pololu.com/product/2676) | Correct 25D motor mounting bracket |
| M4 | [Pololu 1997](https://www.pololu.com/product/1997) | Optional 4 mm hub with M3 holes; not an 8 mm shaft hub |
| O1 | [TCST2103 datasheet, Vishay](https://www.vishay.com/docs/81147/tcst2103.pdf) | Independent optical caster-speed measurement |

## Procurement evidence and limits

The [BOM price evidence](../hardware/BOM.md#price-evidence-and-exact-package-contents) now includes published supplier prices for the DK, sensors, ADCs, motor/driver, supplies, stop switch, passive components, complete caster and coupling. Required listed parts subtotal **USD 299.78**; separately identified fabrication/consumable estimates add **USD 180.00**, making a **USD 479.78 planning budget** before delivery, taxes and import costs. Optional B09 adds USD 10.95. Estimates are not vendor prices. Some product-page content is cached; recheck checkout price and availability. B13 and B14 displayed out of stock.

No unidentified item is assigned a fabricated supplier price. B17, B18, B21, B22 and B24–B27 carry explicit planning allowances; custom dimensions, materials and shop labor still need actual quotations. B28/B29 have zero additional cost only under the documented reuse assumption; access is not confirmed. The CSV separates observed supplier prices from estimated budgets so an estimate cannot be treated as a verified quote.

India sourcing entry points, not verified stock guarantees:

- [Nordic DK on DigiKey India](https://www.digikey.in/en/products/detail/nordic-semiconductor-asa/NRF54LM20-DK/27685498)
- [ADXL345 reference breakout on DigiKey India](https://www.digikey.in/en/products/detail/adafruit-industries-llc/1231/4990764)
- [Motor 4886 on DigiKey India Marketplace](https://www.digikey.in/en/products/detail/pololu/4886/10450266)
- [Pololu 4036 on MG Super Labs](https://mgsl.in/products/pololu-4036)
- [TAL221 on MG Super Labs](https://mgsl.in/products/sfe-sen-14728)
- [TAL220 on MG Super Labs](https://mgsl.in/products/sfe-sen-13329)
- [TCST2103 on element14 India](https://in.element14.com/vishay/tcst2103/optical-sensor-transmissive-3/dp/1470060)

Do not substitute a 37D high-power motor, single-supply HX711 board or unspecified sensor module without rechecking voltage, current, shaft sizes and signal levels. Purchasing nothing has been authorized or performed as part of this documentation task.
