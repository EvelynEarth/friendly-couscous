---
name: data-competition-skill
version: 1.0.0
summary: General-purpose data competition workflow for unknown future competition tasks. Identify the problem before choosing methods, audit data and evaluation, design leakage-safe validation, build strong baselines, run evidence-driven experiments, and produce reproducible submission artifacts across many data modalities.
triggers: [大数据竞赛, 大数据挑战赛, 数据竞赛, data competition, data science competition, datathon, 机器学习竞赛, 赛题分析, 数据分析, baseline, 特征工程, 模型选择, 模型比较, 交叉验证, 数据泄漏, 实验设计, submission]
---

# Data Competition Skill

## Mission

This is a competition-first, modality-agnostic data science workflow.

The governing rule is:

**Do not choose the model before identifying the task, data-generating structure, evaluation protocol, and failure risks.**

A future competition may be tabular, time-series, computer vision, NLP, audio, graph, spatial, multimodal, optimization, simulation, or a hybrid. The workflow must remain useful when the task type is unknown.

Historical competition examples may inform hypotheses, but must never be hard-coded into the current solution.

## Operating principles

1. Evidence before assumptions.
2. Task before model.
3. Validation before tuning.
4. Treat leakage as a first-class threat.
5. Establish a simple, inspectable baseline before adding complexity.
6. Every meaningful experiment must answer a question.
7. Optimize the official competition metric, not a convenient proxy.
8. Reuse external methods only after checking task, data, validation, and implementation similarity.
9. Public leaderboard movement is evidence, not proof of generalization.
10. Reproducibility is part of the solution.
11. Never fabricate scores, rankings, runtimes, robustness results, or hidden-test information.
12. Respect competition rules and external-data restrictions.

## Stage A — Competition triage

Build a competition profile before modeling.

Record:

- objective
- task type
- prediction or decision unit
- target/objective
- input modalities
- train/validation/test availability
- sample size and dimensionality
- group/entity identifiers
- temporal structure
- spatial structure
- class distribution
- missingness and duplicates
- official metric
- secondary diagnostics
- submission schema
- compute/runtime constraints
- external-data rules
- suspected leakage paths

Possible task families include regression, classification, ranking, recommendation, forecasting, anomaly detection, clustering, retrieval, generation, image classification, object detection, segmentation, video, audio, NLP, graph learning, spatial analysis, causal/statistical analysis, optimization, simulation, reinforcement learning, multimodal, and hybrid/custom tasks.

Do not force a single label when the competition contains multiple coupled tasks.

## Stage B — Data forensics

Inspect the real files rather than relying on the statement alone.

Minimum audit:

- file inventory and sizes
- schema and dtypes
- target availability
- identifier uniqueness
- duplicate rows/files
- missingness patterns
- constant and near-constant features
- cardinality
- outliers
- label distribution
- train/test distribution shift
- temporal coverage
- group/entity overlap
- corrupted or unreadable assets
- suspicious columns
- target-encoding features
- submission ID alignment

Modality-specific checks:

- Tabular: categorical semantics, scales, entity history, leakage.
- Time series: chronology, horizon, look-ahead leakage, overlapping windows, regime changes.
- Vision/video: resolution, duplicates, annotation quality, object scale, class imbalance, identity overlap.
- Text: duplicate documents, language, length, entity overlap, temporal leakage.
- Audio: sampling rate, duration, speaker/session overlap, noise.
- Graph: node/edge overlap, temporal leakage, transductive versus inductive setting.
- Spatial: coordinate system, spatial autocorrelation, geographic leakage, spatial holdout.
- Multimodal: sample alignment, synchronization, missing modalities, modality-specific leakage.
- Optimization/simulation: objective, feasibility, constraint semantics, stochasticity, simulator fidelity.

## Stage C — Validation design

Validation is a design problem, not a default library call.

Choose the protocol from the data-generating process:

- IID labeled data: stratified or group-aware K-fold where appropriate.
- Grouped entities: group holdout or GroupKFold.
- Temporal prediction: chronological split or walk-forward.
- Overlapping forecasting windows: purged/embargoed validation.
- Spatial dependence: spatial/block holdout.
- Ranking: group-aware split.
- Rare-event classification: stratified or repeated group-aware evaluation.
- Multimodal entities: entity-level split.
- Optimization/simulation: repeated seeds and scenario holdout.
- Unknown hidden-test mechanism: reconstruct the likely mechanism first.

Document why the split matches the competition, what information is unavailable at prediction time, what must be fitted inside each fold, what constitutes an independent sample, and how local validation relates to leaderboard evidence.

If the correct split is uncertain, test multiple plausible validation schemes and diagnose which assumptions change the conclusion.

## Stage D — Baseline ladder

Use a four-level ladder:

1. Sanity baseline: verifies target direction, metric implementation, pipeline, and submission schema.
2. Strong classical baseline: an appropriate robust model for the modality.
3. Strong single model: competitive architecture only after validation is trustworthy.
4. Ensemble: only when models have complementary errors and gains survive reliable validation.

Do not ensemble merely because more models sound stronger.

## Stage E — Method routing

### Tabular
Consider linear/GLM models, CatBoost, LightGBM, XGBoost, tree ensembles, regularized neural networks, and leakage-safe statistical encodings.

### Time series
Consider naive and seasonal baselines, exponential smoothing, ARIMA-family methods, lag/rolling features with boosting, state-space models, temporal neural networks, and transformers when scale justifies them.

### Vision
Consider pretrained CNN/ViT features, classification backbones, detection, segmentation, multi-scale strategies, augmentation, and class-imbalance methods.

### NLP
Consider TF-IDF plus linear baselines, pretrained encoders, classification/ranking/generation according to the task, and retrieval only when rules permit it.

### Audio
Consider engineered spectral features, classical models, pretrained embeddings, spectrogram models, and sequence models.

### Graph
Consider graph statistics, embeddings, GNNs, and temporal graph methods.

### Spatial
Consider spatial features with classical ML, spatial statistics, graph formulations, raster/image models, and spatially blocked validation.

### Optimization and operations research
Consider exact mathematical programming, dynamic programming, network algorithms, constructive heuristics, local search, metaheuristics, decomposition, and simulation-optimization. Establish feasibility and objective correctness before optimizing performance.

### Simulation
Separate simulator correctness, stochastic variability, scenario generation, policy optimization, and statistical confidence. Never treat one random run as a deterministic answer.

### Multimodal or hybrid
Start with separate modality baselines, then compare early fusion, late fusion, cross-modal interaction, and missing-modality robustness.

## Stage F — Experiment protocol

Every nontrivial experiment records:

experiment_id, hypothesis, baseline, single_change, data_version, feature_version, validation_protocol, model/config, random_seed(s), official_metric, secondary_metrics, result, uncertainty/variance, interpretation, decision, next_experiment.

Rules:

- Change one major factor at a time when attribution matters.
- Keep a stable reference split for fast iteration and a stronger confirmation protocol for finalists.
- Repeat stochastic methods when variance can change conclusions.
- Run ablations for material features, augmentation, losses, data sources, and ensemble components.
- Record failed experiments.
- Never silently overwrite an earlier experiment.

## Stage G — Error analysis

After meaningful improvements, inspect failures using the task-appropriate view:

- residuals and calibration
- confusion matrices and per-class metrics
- subgroup performance
- temporal regimes
- entity/group performance
- spatial regions
- object size and occlusion
- text length/language
- audio quality/speaker
- graph degree/component
- optimization infeasibility and constraint violations

Choose the next experiment from the diagnosed error mechanism.

## Stage H — Robustness and ensembling

Before declaring a finalist:

1. Compare model error correlation.
2. Check ensemble gains across splits and seeds.
3. Test sensitivity to important preprocessing choices.
4. Test reasonable distribution shifts.
5. Check boundary cases and rare groups.
6. Verify submission IDs and row alignment.
7. Re-run the final pipeline from a clean state.

Do not claim robustness from one perturbation.

## Stage I — Competition research

When external research is allowed, search in this order:

1. official rules and data documentation
2. official metric definition
3. organizer clarification
4. high-quality winning solutions
5. strong public implementations
6. relevant papers
7. general tutorials

For every reused method, record source, task similarity, data similarity, validation similarity, method, transfer rationale, non-transferable assumptions, implementation cost, and risk.

Never copy a solution only because it ranked highly elsewhere.

## Stage J — Submission audit

Verify:

- required file names
- exact columns
- row count
- ID preservation
- ordering
- value ranges
- NaN/Inf absence
- duplicate IDs
- prediction type
- probability normalization when required
- class labels
- coordinate/box/segmentation format when relevant
- metric implementation
- seed and reproducibility metadata
- rule compliance
- external-data compliance

Create a final manifest containing code version, data version, feature/model version, validation protocol, final metric, submission path/hash, runtime, environment, and known limitations.

## Stage K — Report and presentation

A competition solution is incomplete if the method cannot be explained.

Separate:

- problem interpretation
- data findings
- validation rationale
- baseline
- final method
- experiment evidence
- ablation
- error analysis
- robustness
- limitations
- submission result

Do not turn empirical leaderboard performance into a causal claim or invent theoretical guarantees.

## Stop conditions

Stop adding complexity when improvements are below practical significance across reliable validation, occur only on one unstable split, increase leakage/reproducibility risk, exceed competition constraints, or cannot be justified by measurable gain.

For finalists, prioritize reliable validation, reproducibility, and submission correctness over speculative last-mile complexity.

## Required final artifacts

For a complete competition run, aim to produce:

1. competition profile
2. data audit
3. leakage audit
4. validation design
5. baseline result
6. experiment ledger
7. final model specification
8. error analysis
9. robustness evidence
10. submission audit
11. reproducibility manifest
12. report/presentation outline

## Explicit non-goals

This skill does not assume the next competition resembles a previous year, hard-code a model family or metric, assume tabular data, assume Kaggle, assume public leaderboard feedback, invent hidden-test information, or treat historical competition answers as permanent truth.
