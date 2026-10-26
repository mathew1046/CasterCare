# Build and validation plan

## Milestones

| Stage | Work | Evidence before moving on |
|---|---|---|
| 1 | Measure caster, finalize fixture and order reference parts | Dimensions and reviewed load paths; no unsupported shaft loading |
| 2 | Configure 3.3 V logic and bring up each sensor | Measured rail levels, calibration records and captured pulses |
| 3 | Run roller unloaded, then under light preload | Stable speed, stop response, slip detection and valid force readings |
| 4 | Record repeated healthy and reversible-friction tests | Labelled sessions and quantified remounting variation |
| 5 | Compare threshold and one compact model | Evaluation separated by caster assembly or session as appropriate |
| 6 | Add BLE commands, reports and service history | End-to-end test, confirm, inspect, service and retest demonstration |

No firmware or dataset is currently included. Do not turn the milestones into completed checkmarks until corresponding evidence exists.

## Essential experiments

1. **Force calibration:** zero and known loads; estimate error, hysteresis and vertical-to-horizontal cross-talk. Average only settled readings.
2. **Repeat mounting:** remove and reinstall the same healthy assembly multiple times. Reference variation must include this effect.
3. **Invalid conditions:** unstable speed, optical disk failure, deliberate roller slip, excessive load and missing HX711 input should reject the test.
4. **Drive contamination:** compare unloaded fixture, healthy caster and changed speeds to establish how much vibration comes from the motor and roller.
5. **Controlled degradation:** add clearly labelled reversible friction; use worn assemblies only if their condition is independently inspected. Do not call simulated friction a specific bearing fault.
6. **Repair verification:** compare valid matched tests before/after service or removal of the simulated condition.
7. **Connection loss:** disconnect the BLE client during a test. Measure the local timeout response and confirm the physical stop still works.
8. **Model value:** compare force threshold, vibration model alone, and model plus quality checks and one confirmation. Report false alerts, missed changes, inconclusive rate and time per completed test.
9. **Data transfer:** compare routine compact reports with raw export using measured bytes and time. Claim energy savings only if current is also measured.

## Dataset discipline

Use [the empty session template](../data/session_template.csv). Keep raw recordings and patient information out of the repository. Session labels should identify the test condition and evidence, not an assumed diagnosis.

For a model intended to work across assemblies, reserve entire assemblies for testing. If only one wheel is available, use separate days/sessions and explicitly limit the conclusion to that wheel. Adjacent windows from one recording must not be split randomly across training and testing.

Choose thresholds using development data, then freeze them before evaluation. A healthy reference is explicitly renewed after a documented service event; unexplained drift is not silently absorbed.

## Predictive claim

Initial claims are condition monitoring and repair verification. To claim early warning, first define an independent unacceptable-performance threshold, collect a degradation sequence and show detection before it is crossed. No remaining useful life or clinical safety conclusion follows from the initial bench demonstration.
