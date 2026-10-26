# Architecture

This is a proposed functional architecture, not a pin-level electrical schematic.

![System block diagram](diagrams/system.svg)

## Data and control paths

```mermaid
flowchart TD
    W["Secured caster on supported roller"] --> A["ADXL345 vibration over SPI"]
    W --> F["Drag and normal load cells"]
    W --> O["Optical caster speed"]
    F --> H["Two HX711 ADC boards"]
    A --> D["nRF54LM20 DK"]
    H --> D
    O --> D
    E["Motor encoder with level reduction"] --> D
    D --> Q["CPU quality checks and one anomaly model"]
    Q --> R["Valid result or one confirmation repeat"]
    R <-->|"BLE commands and compact reports"| P["Nearby phone or laptop"]
    D --> M["DRV8876 motor driver"]
    M --> G["12 V motor and flexible coupling"]
    G --> W
```

## Proposed operating sequence

```mermaid
flowchart TD
    S["Secure caster and choose reference"] --> C["Zero sensors and check load"]
    C --> T["Run controlled speed test"]
    T --> V{"Valid speed load and slip?"}
    V -->|"No"| I["Reject and correct setup"]
    V -->|"Yes"| A["Compute drag and anomaly score"]
    A --> N{"Suspicious change?"}
    N -->|"No"| H["Store valid comparison"]
    N -->|"Yes"| X["One matched confirmation run"]
    X --> Z{"Valid and consistent?"}
    Z -->|"Persistent change"| K["Inspect service and retest"]
    Z -->|"Disagreement or invalid"| U["Inconclusive"]
```

The implementation must stop the motor on a hardware stop, missing sensor input, overload, stalled motion or communication timeout as appropriate. The stop button interrupts motor power as well as informing software. A person must not reach past the guard while motion is possible.

## Acquisition targets

These are starting design targets, not tested specifications:

| Input | Initial target | Use |
|---|---|---|
| Accelerometer | 800 samples/s over SPI, with data-ready or FIFO handling | Vibration features; move to 1600 only after verifying at least 2 MHz SPI and loss-free capture |
| Each HX711 | 10 samples/s initially; average a stable window | Mean drag and normal load, not bearing vibration |
| Motor encoder | Timestamp/counter capture | Roller speed feedback |
| Caster optical disk | 12 slots with one-edge pulse counting | Actual caster RPM and slip check |
| BLE | Periodic status, end-of-test report, raw export on request | Avoid continuous raw streaming in routine mode |

An example 40 mm roller at 60 RPM has a surface speed near 0.126 m/s. A 100 mm caster would rotate near 24 RPM without slip, producing about 4.8 pulses/s from a 12-slot disk. A 20 s measurement spans about eight caster turns. These are geometry calculations for an illustrative fixture, not a guaranteed motor operating point.

## Firmware and model plan

Use the Nordic-supported nRF Connect SDK/Zephyr workflow for the actual board revision. Record the tested SDK version before publishing any build instructions. No firmware is implemented in this repository yet.

1. Bring up each input independently and prove timestamps and units.
2. Implement a fixed speed test with local stop conditions.
3. Add programmed validity limits and save accepted/rejected recordings.
4. Implement feature extraction and a simple threshold reference.
5. Deploy one compact anomaly model and compare it fairly.
6. Evaluate the supported model on Axon if the tooling is practical.
7. Add the BLE client and result history.

Raw 20 s, three-axis, 16-bit data at 800 samples/s is about 96 kB before headers. Use a bounded buffer or incremental features, not an unbounded log. Store small references in nonvolatile memory; select a raw-export transport after measuring actual memory and throughput.

## Proposed BLE interface

| Characteristic | Direction | Payload intent |
|---|---|---|
| Command | Client to DK | Select profile, start, confirm, cancel, export |
| Status | DK to client | State, progress, validity flags, heartbeat |
| Result | DK to client | Test ID, reference version, load, speed, drag, score, outcome |

Assign project UUIDs during firmware implementation. Pair and authorize commands before exposing motor controls. A BLE command is a request; the DK independently validates the fixture and state. Browser Web Bluetooth availability is not assumed; a native BLE client or development application is acceptable initially.
