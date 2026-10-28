# Changelog

ADR+ uses numbered releases (spec S7). Followers record the version they follow, and a check fails when their copy
drifts from it.

## 0.1.0 (prepared, not tagged)

- The first release: the JSON Schema for the YAML header, the reader (`tools/adrplus.py`), the converter and its
  lossless proof (`tools/adr-yaml.py`) with its fixtures, self-test and red arms, `VERSION`, and `MANIFEST.sha256`
  with the tool that writes it.
- Cut from the reference project's schema and converter. The project's folder names, its owner and its drill names
  moved into settings (the decisions README's `Owner` and `Archive folder` rows, and command-line flags); the
  helpers the converter borrowed from the reference project's other tools are now inside it.
- One addition to the converter: a bold label line (`**Owner:**`, `**Consulted:**`) between `**Kind:**` and the
  `**Supersedes:**` line no longer stops the lineage line from moving. The label line stays in the body, where the
  Status line stood, and the proof checks it is still there.
- No tag and no release exist yet; the owner tags `v0.1.0`.

## Unreleased (draft)

- 2026-10-18: repository created; `SPEC.md` moved here from pitmaster's `docs/proposals/adr-plus-spec.md`.
  The spec is a draft: the owner has ruled its open questions (S1–S9) but not yet the spec as a whole.
  No release is tagged until it is ratified.
