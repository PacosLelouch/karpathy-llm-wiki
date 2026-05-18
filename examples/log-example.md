# Log

## [2026-05-18] ingest | Map Generator Notes
- Raw source: `raw/sources/2026-05-18-map-generator-notes.md`
- Created: `wiki/sources/map-generator-notes.md`, `wiki/concepts/constraint-driven-generation.md`
- Updated: `wiki/entities/mapgen.md`, `wiki/index.md`
- Cascade updates: `wiki/overview.md` needs a short note on constraint explainability
- Conflicts / changes: no direct conflict found
- Follow-up questions: clarify hard vs soft constraints

## [2026-05-18] query | MapGen generation pipeline
- Question: MapGen 当前地图生成流程的核心阶段是什么？
- Read: `wiki/index.md`, `wiki/sources/map-generator-notes.md`, `wiki/entities/mapgen.md`
- Written: none
- Key answer: pipeline can be modeled as constraints, rule layout, post-processing, and explanation

## [2026-05-18] archive | WFC 与 BSP 地图生成比较归档
- Question: WFC 和 BSP 哪种更适合 MapGen？
- Created: `wiki/analyses/wfc-vs-bsp-archive.md`
- Sources: `wiki/concepts/wave-function-collapse.md`, `wiki/concepts/binary-space-partitioning.md`
- Snapshot note: point-in-time archive; not cascade-updated.

## [2026-05-18] lint | wiki health check
- Issues found: 3
- Auto-fixed: added one missing index entry
- Report-only: one possible duplicate concept, one archive may be stale
- Remaining: confirm whether to merge duplicate concepts

## [2026-05-18] repo | llm-wiki skill packaging
- Changed: `SKILL.md`, `references/`, `examples/`, `README.md`
- Validation: Skill is valid
