# Technical Roadmap Figure Contract

This template governs a **problem-analysis technical roadmap / mind map**, not a numerical result figure.

## 1. Role and placement

Use this artifact only when a compact map materially helps the reader understand how multiple questions, models or evidence stages connect.

Default paper location for Chinese mathematical-modeling papers:

```text
问题分析（逐问）
→ technical roadmap figure
→ 模型假设 / 符号说明 / 问题一模型建立与求解
```

If the competition template or an explicit user presentation lock specifies another location, follow that higher-priority requirement.

## 2. Content compression

Each node should normally contain a short noun/verb phrase rather than a sentence. Prefer problem-specific phrases such as:

```text
宏观极值识别
Fresnel 折射率恢复
双角稳健融合
Airy 模型判别
条件性回查
```

Do not place full derivation formulas, long parameter lists, code names or generic slogans in the roadmap. A decisive final numerical answer may appear only when the user explicitly wants a result-oriented roadmap; otherwise keep the map at the method/logic level.

## 3. Logical structure

The map should expose three things at a glance:

1. what each question receives;
2. what mathematical/modeling operation it adds;
3. what artifact/claim it passes downstream.

For dependent questions, show real inheritance instead of drawing independent boxes that merely happen to be adjacent.

## 4. Layout QA

Hard visual checks:

- connectors must terminate at box boundaries, not through text;
- no connector may cross a text box;
- avoid arrow/arrow crossings; reroute with orthogonal segments or change hierarchy;
- sibling boxes share alignment and spacing;
- group borders never obscure node borders;
- reading order is unambiguous from top-to-bottom or left-to-right;
- the final convergence path is visually unique;
- font size remains legible after insertion at the intended paper width.

If any crossing remains, the figure is not review-ready.

## 5. Style

Use restrained academic colors, thin borders, limited hierarchy and a white/light background. Color encodes question/branch identity; it is not decoration. Avoid gradients, shadows, 3-D effects or icon-heavy infographic styling unless the user explicitly asks for them.

## 6. Editable Draw.io delivery

When the user asks for Draw.io/editable source, deliver both:

1. a rendered preview (PNG/SVG/PDF as requested);
2. valid Draw.io XML (`.drawio` or `.xml`).

Editable XML requirements:

- every text box and connector remains an independent mxCell;
- group containers are editable, not flattened images;
- connector routing uses explicit orthogonal waypoints when needed;
- no base64 screenshot is used as a substitute for editable geometry;
- reopening in Draw.io must preserve all node text and connector anchors.

## 7. Review question

Before acceptance ask only:

> Without reading the surrounding prose, can a reviewer recover the problem order, the key modeling operations, the cross-question inheritance and the final convergence logic within several seconds?

If not, reduce nodes or restructure the hierarchy before polishing colors.