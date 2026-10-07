# Data Competition Skill

A standalone, general-purpose skill for unknown future data competitions.

It is intentionally modality-agnostic. It first identifies the task, data structure, evaluation mechanism, leakage risks, and constraints, then routes to appropriate methods.

## Scope

It can handle:

- tabular data
- time series and forecasting
- computer vision
- NLP
- audio
- graph data
- spatial data
- multimodal data
- optimization and operations research
- simulation
- hybrid/custom tasks

## Core loop

Competition triage -> data forensics -> leakage audit -> validation design -> baseline -> method routing -> experiments -> error analysis -> robustness -> submission audit -> reproducible delivery.

## Independence

This is a new skill. It does not modify, replace, or depend on the existing mathmodel-skill workflow.

Past competition questions are treated only as examples. They are not encoded as future assumptions.

## Location

skills/data-competition-skill/SKILL.md
