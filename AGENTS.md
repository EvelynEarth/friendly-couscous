# Agent instructions — Big Data Competition Skill

Current authoritative entrypoint: root SKILL.md (big-data-competition-skill v2.6.0).
Read it before anything else, then load only the references/playbooks needed for the
specific official competition question. Do NOT start from core/bootstrap.yaml:
that is a historical HSK mathematical-modeling bootstrap, not this Skill.

## Competition execution

1. Read the current official problem statement, deliverables, attached data and rules.
   Freeze a Competition Contract; mark unknown items unknown.
2. Per subproblem classify objective and structure; audit data, entity/timestamp boundaries,
   leakage, label availability, and official evaluation protocol.
3. Start from a credible baseline. Choose methods only for the actual data and task.
4. Do not invent model runs, results, figures, sources, runtime, metrics or paper claims.
   Use accepted results and reproducible scripts as evidence. Follow official results
   format when one exists; never assume Kaggle submissions or a fixed task type.
5. Maintain experiment provenance, figure provenance, a claim-to-evidence map and
   an independent paper quality review. Prefer user-executed full-fidelity code where
   that is the competition execution contract.
6. External Agent Skills are optional design references, not implicit dependencies.
   Do not copy third-party code without a license review and attribution.

## Repository maintenance

1. Read root SKILL.md and SKILL_CHANGE_GOVERNANCE.md from current main.
   Confirm latest main SHA, main version, overlapping open PRs and source of truth.
2. Make a change brief, use a dedicated branch and one theme per PR.
   Do not write directly to main or edit generated indexes/hashes by hand.
3. Validate with python scripts/validate_bigdata_skill.py, python -m unittest
   discover -s tests -p test_bigdata_*.py, and
   python scripts/generate_indexes.py --check.
4. Historical HSK core/, modules/, and tests/ remain available but are not active
   Big Data Skill entrypoints and should not be silently re-enabled by unrelated PRs.
5. Merge only after relevant checks pass; report CI, PR, commit SHA and limitations.

## Evidence-based self-tests

The award-paper inventory is file metadata until inspected PDF page evidence exists. Check it with: python skills/big-data-competition-skill/tools/award_paper_audit.py --summary.
Run synthetic adversarial plan checks with: python skills/big-data-competition-skill/tools/competition_benchmark.py.
Neither check implies model runs, official result correctness or award-paper review completion.

## Real-case evidence readiness (v2.3)

Before claiming a 2025 A/B reproduction, load `skills/big-data-competition-skill/references/real-case-replay.md`.
For 2025 A, audit actual train labels but keep `labels/test` sealed for training, validation and hyperparameter tuning. For 2025 B, Git LFS pointer text is not a usable Excel workbook.
Use `tools/paper_evidence_gate.py` for accepted run metric, split and artifact hashes; do not manufacture experiment metrics to satisfy the gate. File hash integrity is not scientific model validation.

## Scientific correctness + argument logic are hard gates (v2.4)

A task is NOT solved just because code ran, a benchmark was green or an attractive metric was reported. Start with the official question, verify modeling assumptions, units and constraints, do independent numeric/theoretical checks, test reliability and stability under declared perturbations, and challenge overclaims. Separate scientific Reviewer from editorial Reviewer.

For awarded papers, learn how authors organize questions, model motivations, transitions, evidence-bearing figures and qualified conclusions; do not copy their algorithms or three-question layouts. Actual paper PDF reading is required before page-backed insights can be attributed to an award paper.

Consult `references/solution-validity.md`, `references/stability-and-uncertainty.md` and `references/paper-argumentation.md`. Quality CLI is a review-coverage tool, not an autonomous mathematical oracle.

## Actual-output falsification and source-of-truth (v2.5)

Before accepting a competition solution, derive necessary invariants directly from the official question and test them against actual result artifacts with `tools/result_invariant_gate.py`. A satisfied invariant is NOT sufficient for correctness; a failed invariant blocks the relevant claim.

Before publishing numerical metrics in the paper, use `tools/paper_evidence_gate.py --require-metric-source` to compare the actual, hash-verified metrics JSON, accepted record and every numerical claim. Do not rely only on self-reported reviewer status or a number copied twice. Read `references/result-falsification.md` and independently audit the scientific evaluation protocol. Do not tailor invariant thresholds after seeing results.

## v2.6 Separate reference oracles

A repeatable program can still be wrong. For relevant tasks, independently recalculate metrics from legal original observations or solve bounded small integer-linear instances using an exhaustive reference. See `references/independent-recomputation.md` and `tools/independent_oracle.py`. Require known-answer, mutation and metamorphic tests. Exact small-case agreement does not prove large-case optimality, prediction generalization or causal validity. The primary research evaluation and independent scientific review remain mandatory.
