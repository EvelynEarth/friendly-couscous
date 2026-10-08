# Agent instructions — Big Data Competition Skill

Current authoritative entrypoint: root SKILL.md (big-data-competition-skill v2.1.0).
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
