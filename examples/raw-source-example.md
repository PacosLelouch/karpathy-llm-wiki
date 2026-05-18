---
title: Map Generator Notes
type: raw
source: Internal design note excerpt
original_url: null
author: MapGen Team
published: Unknown
collected: 2026-05-18
topic:
  - map-generation
tags:
  - pcg
  - mapgen
status: active
---

# Map Generator Notes

> [!info] Source Metadata
> - Source: Internal design note excerpt
> - Author: MapGen Team
> - Published: Unknown
> - Collected: 2026-05-18

## 原始内容

The prototype combines rule-based room placement with post-processing passes for connectivity and pacing. Current weaknesses include repetitive room shapes and weak global structure.

Designers want a pipeline where constraints can be edited before generation, and the system can explain why a generated map satisfies or violates those constraints.

## 附件

- `raw/assets/mapgen-pipeline-sketch.png`
