# CasterCare explained

## What it does

A caster is the small swivelling wheel at the front of a manual wheelchair. CasterCare is a proposed tool for a repair workshop or rehabilitation centre to test one detached caster at a time. A powered roller turns the wheel while sensors measure how it behaves. The operator sees a useful result: repeat the setup, no significant change from reference, inspect the wheel, or inconclusive.

An inspection prompt is not a safety certificate or a diagnosis of a specific broken part. The tool is meant to support a technician and provide an objective record of change.

## Why operating conditions matter

Vibration depends on speed, loading, mounting and the drive mechanism as well as the wheel itself. A model that ignores these factors may call a perfectly healthy wheel faulty. The first innovation to test is therefore simple: only interpret recordings when the test is comparable with the reference.

The CPU checks speed, normal force, slip and sensor validity. One compact model evaluates vibration features after those checks pass. Drag is measured independently and shown alongside the model result. A suspicious test is repeated once at the same settings. Disagreement remains inconclusive.

This is not a complex autonomous diagnostic planner. It is a small, reproducible decision workflow that can be compared against simpler alternatives.

## Example

1. A technician installs an inspected caster and stores reference recordings after several remounts.
2. A later measurement has unusual vibration but unstable roller speed. CasterCare rejects it instead of blaming the caster.
3. After correcting the setup, the technician gets a valid result showing increased drag and an abnormal vibration score.
4. One confirmation run shows the same change. The system recommends inspection.
5. After appropriate servicing, the technician retests the wheel and compares the measured change.

These steps describe intended behaviour. No result has yet been demonstrated.

## What each measurement means

| Measurement | Meaning | Important limitation |
|---|---|---|
| Caster-fork vibration | Describes repeated motion and impact patterns | Includes fixture and drive noise; does not uniquely identify a bearing fault |
| Horizontal reaction force | Estimates the rolling drag under the calibrated fixture geometry | Guide friction, misalignment and cross-axis forces must be assessed |
| Vertical reaction force | Confirms applied normal load | A load-cell capacity is not a certified fixture load rating |
| Motor encoder speed | Shows driven roller motion through the coupling | Does not show whether the caster is slipping |
| Independent caster speed | Measures rotation of the actual caster | Requires a removable optical target and clean pulse counting |

## Simple hardware scope

One Nordic DK connects to one accelerometer, two load-cell ADC boards, the motor driver, its encoder and one optical caster sensor. The two force channels serve different purposes; they are not a distributed sensor network. A laptop or phone is a display/control client, not a second inference computer.

The proposed fixture starts around a 1 kg added preload, accounting for fixture weight and the measured contact force. It tests a component under a repeatable light load. It does not reproduce a full person's wheelchair loading or establish performance at real service loads. Expansion requires separate mechanical design and validation.

## Edge AI without unnecessary complexity

Collect healthy recordings first. Extract a compact set of time and frequency features, such as RMS vibration and energy in fixed bands. Train a small anomaly model on a computer. Deploy the supported model to the DK; begin on the CPU and evaluate Axon only after the input pipeline works.

Compare the model with a simple drag threshold. Compare both with the full quality-check-and-repeat workflow. The intended benefit is fewer false alerts while preserving useful sensitivity. Neither AI nor NPU deployment is assumed to improve the result automatically.

The reference stays fixed until a technician confirms a suitable maintenance or recalibration event. Keep the old reference in the service history. Do not automatically learn an unexplained deterioration as normal.

## Bluetooth use

Use a small BLE service for selecting a test profile, requesting a run, showing progress, requesting a confirmation and receiving results. Transfer a compact evidence record: test ID, reference version, speed/load validity, slip flag, mean drag, anomaly score and outcome. Raw data exports are an optional development action.

This borrows the useful idea of inference-gated communication: local analysis determines when a richer report or optional recording is worth transferring. A small heartbeat/status update is still sent so silence is not mistaken for a healthy result. Disconnection invokes a local stop timeout.

## Realistic value

Possible first users are wheelchair service centres and refurbishment programmes. The business hypothesis is that repeatable checks can help document component condition and repair outcomes. Interviews must establish whether this is more useful than a quick manual inspection. No selling price, savings or willingness to pay is validated.

## Predictive maintenance boundary

The first deliverable is condition monitoring and repair verification. For an early-warning claim, evaluate staged degradation against an independently defined unacceptable-performance threshold and show the alert happens before it is crossed. A simulated friction change is not proof of future bearing failure. Do not report a failure date or remaining life without longitudinal failure data.

See [research](RESEARCH.md), [BOM](../hardware/BOM.md) and [validation](VALIDATION.md) for evidence and the next steps.
