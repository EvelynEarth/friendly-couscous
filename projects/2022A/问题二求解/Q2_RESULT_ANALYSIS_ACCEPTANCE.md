# Q2 Result Analysis Acceptance

## Status

- Q2 main result workbook: **accepted**
- Q2 deep-analysis workbook: **accepted**
- Current next gate: **Figure Evidence / MATLAB Figure QA**
- Approved semantic revision: `1`
- Semantic hash: `513d81ccab68ccea4f5db5df0ff8b87169240d27c55f1d4edef80e67606f7862`
- Data hash: `0cc51ac30576d2c2d3901aaf27dfe26526bd3768035c2685e9a57d4f81551653`

## Accepted Q2 numerical evidence

- Linear optimum: `c*=37193.81188797437 N·s/m`
- Linear steady mean power: `229.3339398384597 W`
- Power-law main candidate: `a=99999.86310981827`, `n=0.4136799318462569`
- Power-law validated steady mean power: `229.992434265901 W`
- Absolute steady gain over optimal linear damping: `0.6584944274412976 W`
- Relative steady gain: `0.2871334386463398%`
- Final validation stop: `170T`
- T/40 vs T/80 relative power difference: `3.492372735455339e-09`
- n=0 cross-model equivalence relative difference: `1.517739854112196e-14`

## Deep-analysis disposition

- `support`: power-law damping improves steady mean power, but only by about `0.287%`; manuscript must not call this a large/significant gain.
- `modify`: `a` is extremely close to the upper bound and the local search diagnostic supports an upper-bound tendency, but the current accepted deep-analysis workbook does **not** claim a formal steady-state proof that `a*=100000`.
- `support`: `n±0.01` both lower the 60T search objective, so the current `n` is near an interior local peak of the search objective.
- `support`: steady-window, step-refinement and n=0 equivalence gates all pass.
- `modify`: DE/Powell `search_power` is a 60T search diagnostic and must not be reported as the final steady mean power.

## Figure Evidence binding

`q2_plot.m` is now bound only to:

1. `问题二求解结果.xlsx`
2. `问题二结果深化分析.xlsx`

It does not rerun the solver/optimizer and does not require the former boundary-refinement workbook.

Planned figures:

- **FQ2-1**: local parameter-structure evidence + steady power gain.
- **FQ2-2**: T/40/T/80 convergence + log-scale 1e-5 stability threshold diagnostics.

Figure status remains `awaiting MATLAB review`; do not mark accepted until the user reviews the rendered MATLAB figures.
