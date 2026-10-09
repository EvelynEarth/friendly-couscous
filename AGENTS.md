# Agent instructions — Big Data Competition Skill

Current authoritative entrypoint: root SKILL.md (big-data-competition-skill v2.10.0).
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

## v2.7 additional scientific reference checks

See `references/extended-oracles.md`. The `extended_oracles.py` utility supports declared rolling time splits, exact paired sign-flip enumeration, iid Bernoulli Monte Carlo precision, and box-constrained separable strictly convex quadratic analytic solutions. Select a mode ONLY if the current official question and underlying assumptions actually warrant it. Independently verify time-dependent feature generation, paired exchangeability/multiplicity, iid simulation sampling, and original optimization math. A golden synthetic test is not a competition result, and no CI success proves a scientific finding.

## v2.8 Cross-module project-scoped evidence chain

Before paper-level numerical approval, see `skills/big-data-competition-skill/references/project-evidence-chain.md`. Run `tools/project_evidence_chain.py` on real SHA-256-locked inputs. The complete list of official subquestions must agree with the review record. Every paper metric must tie to an independently recomputed oracle value; invariants must use the same underlying oracle data; stability must contain an anchor equal to the accepted metric. Any real failure blocks machine evidence consistency. No automatic result signifies scientific truth or permission to submit. Unsuitable task categories need a task-specific independent reference, not a fabricated passing run.

## v2.9 Universal competition review package (all model families)

The task type must not be distorted to satisfy a numeric-only checker. Start from `references/competition-final-runbook.md`. For any unknown problem, record official outputs, actual result, independent scientific review evidence, reliability, stability, properly scoped claims, paper argumentative functions and current official submission requirements. Use `tools/competition_readiness.py` for SHA-backed *documentation completeness*, not scientific approval. Apply the stricter numeric `project_evidence_chain.py` only to task families actually supported by its oracles. Otherwise design the correct independent task-specific scientific test and preserve human review. No award paper can be reported as reviewed merely because its PDF filename exists.

## Competition Autopilot — v2.10

For any new contest attachment or "continue" request, first read the root SKILL.md and `skills/big-data-competition-skill/references/automatic-competition-workflow.md`. If the agent actually has persistent file access and Python execution, inspect `autopilot-state.json` or initialize from the verified official input folder and execute `competition_autopilot.py run`. Resume at `next`, load only the relevant method playbooks, actually produce results, and save artifacts plus stage review. No fabricated passed status.

The controller routes failures to upstream causes, invalidates stale evidence, requires fresh checks, and escalates after 3 failed rounds. At model-plan and final-delivery stages, STOP for explicit human approval. Do not self-invoke `approve` without the user saying so. No automatic contest submission, no unauthorized compute, no ghost background execution. CI validates only process behavior, not scientific correctness or LLM autonomy. If you cannot run code/read persistent files, disclose constraints and ask for necessary execution/access instead of claiming autopilot is active.

## v2.11 Paper / figure / TeX visual delivery gates

At paper/figures/final/delivery, read `references/paper-visual-quality-gate.md`, `references/paper-writing.md`, `references/figure-evidence.md`, and actual official format announcements. Record academic-language review with concrete paragraphs, figure evidence + intended color semantics, and render **every page** of the current compiled PDF. A PDF that exists, a clean hash, or a filled review JSON is not a visual/scientific pass. Retain failure cases and fix source rather than editing a review status.

When TeX Live + writable workspace is available, supply `main.tex`, any legal class/style assets, actual plot files, a Windows 11 / TeX Live compile recipe, build log and compiled PDF. Never claim a traditional math-modeling template was migrated if its source was not accessible. Read 2023 Big Data official formatting rules instead of the different 2023 standard MathorCup rules. Use deliberate accessible scientific color (not blanket monochrome); check grayscale readability. Award-paper inventory (16 PDFs) is not equivalent to 16 reviewed PDF contents.


## v2.11.1 prevent repeated LaTeX layout failures

Before paper/final/delivery signoff, run `tools/latex_paper_audit.py --tex main.tex --pdf main.pdf --log main.log --profile bigdata2023` **only for the 2023 profile**; use generic profile for other competitions. Reject manual numbering inside `\\caption`, duplicate TOC titles, missing figures, wrong two-character first-line body indent under the declared style, and actual compilation warnings. Re-render all physical pages after fixing code. A green preflight still requires independent editorial page-by-page review, including legends, overlap and typography.
