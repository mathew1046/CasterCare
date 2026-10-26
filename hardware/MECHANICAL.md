# Mechanical measurement concept

**Initial design only.** Final dimensions, load paths, force calibration and guarding must be reviewed and tested before operation.

## Fixture arrangement

- Mount a single detached caster assembly with its swivel direction constrained. Do not test an occupied wheelchair.
- Use a rigid base and a guided caster carriage. Permit small displacement along the tangential measurement axis while constraining unwanted motion.
- A 500 g miniature bar cell measures the carriage's horizontal reaction through a properly aligned linkage. Add independent mechanical stops so accidental load cannot continue through the cell.
- A separate 10 kg bar cell in the vertical load path measures normal contact force. Guides must not bypass the intended measured load path.
- Use deadweights or a controlled loading screw, initially targeting a light contact load around 10 N, after accounting for all supported mass. The 10 kg cell capacity does not authorize testing at that load.
- A supported roller turns the caster. Use two external bearings on a separate shaft and a flexible coupling to the motor. Do not place caster preload directly on the small gearbox shaft.
- Attach a removable optical disk to the caster wheel, not just the driven shaft. Keep it inside the guard.
- Attach the accelerometer rigidly to the caster fork in the same orientation for every comparison.

## Proposed starting dimensions

| Item | Starting envelope | What must be checked |
|---|---|---|
| Caster | One measured assembly, approximately 100 mm wheel diameter | Axle bore, fork width, mounting pattern, surface condition |
| Roller | Approximately 40 mm diameter and at least wheel width plus margin | Roundness, grip, balance, retained tread |
| Roller shaft | 8 mm precision shaft with two matching bearings | Bearing fit, retention, stiffness and external support |
| Coupling | 4 mm motor bore to 8 mm roller-shaft bore | Actual shaft diameters and set-screw engagement |
| Drag measuring range | Under 4 N initially, subject to calibration | 500 g cell nominal capacity is about 4.90 N; stops must protect it |
| Normal contact force | Around 10 N initially | Cross-axis loading and guide friction |

These are design choices, not finished CAD dimensions. Purchase custom parts only after measuring the chosen caster and confirming the fixture layout. The optional 4 mm mounting hub is only needed if the selected coupling/roller construction uses it; do not buy it automatically.

## What the force result means

At stable speed and matched load, the calibrated horizontal reaction is a candidate measurement of rolling drag. It is not automatically equal to a pure bearing-friction measurement. Alignment, guide friction, tire deformation, roller shape and contact geometry affect the result.

Calibrate with known horizontal forces and known vertical loads. Check whether a vertical-load change appears in the horizontal channel. Measure the unloaded fixture baseline. Compare a few assembled tests with an independent pull-force measurement. If uncertainty exceeds the difference of interest, redesign the fixture instead of training an AI model on it.

## Drive noise and slip

The gearmotor and roller can create vibration that reaches the fork. Keep the motor mount consistent, consider a flexible coupling, and record fixture-only and healthy-wheel controls. Test several speeds to identify motor-related patterns. No vibration feature should be labelled a bearing defect without supporting evidence.

Use motor encoder RPM and actual wheel RPM with measured diameters to compare surface speeds. Flag excessive disagreement. The exact slip limit must be measured and documented; an illustrative 5% threshold is only a starting experiment, not a validated acceptance rule.

## Essential protection

Include a physical guard, a normally closed stop circuit that cuts motor power, load-cell overload stops, shaft retention, strain relief and a fuse sized for the tested wiring and startup current. The 500 g sensor is especially easy to overload during assembly. Stop before adjusting the caster or optical disk.
