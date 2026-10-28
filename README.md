# ADR+

ADR+ is a way of writing architecture decision records (ADRs): short files that each record one decision and why.
It is built for a project where AI agents draft most of the records and one person rules on them.

**Status: draft.** Release 0.1.0 is prepared (see below) and not tagged. The spec's open questions are ruled; the
spec as a whole is not yet ratified.

## Start here

Read [ADR+ in five minutes](SPEC.md#adr-in-five-minutes): one worked example, six rules, and the parts you add only
when a decision needs them. The rest of [SPEC.md](SPEC.md) is reference.

## What is in this repository

| Path | What it is |
|---|---|
| `SPEC.md` | The spec: the five-minute page, then the reference |
| `schema/adr-plus.schema.json` | The JSON Schema for the YAML header (SPEC 1.3) |
| `tools/adrplus.py` | The one reader for an ADR header: the YAML parser, the schema validator and the project settings |
| `tools/adr-yaml.py` | The converter that moves an old header (bold lines, MADR, classic) into the YAML block, and the proof that nothing was lost |
| `tools/fixtures/adr-yaml/` | The fixtures the converter's self-test reads; `EXPECTED.md` names each verdict |
| `tools/make-manifest.py` | Writes and checks `MANIFEST.sha256` |
| `VERSION`, `MANIFEST.sha256` | The release number, and the hash of every file a follower copies |

Python 3.8 or later, standard library only. PyYAML and jsonschema, when installed, act as a second instrument over
the same headers.

```
python3 tools/adr-yaml.py --self-test      # the fixtures, the proof and its red arms
python3 tools/adr-yaml.py --dry-run        # convert every ADR in memory, prove each, write a report
python3 tools/adr-yaml.py --apply          # write the YAML headers, only if every conversion proves lossless
python3 tools/adr-yaml.py --check          # the standing check once the tree is YAML
```

### Settings

A project fills in the decisions folder's `README.md` (SPEC 4.2). The tools read two rows of its settings table, and
the command line wins:

```
| Owner          | Alex               |   --owner NAME      written into every converted ADR
| Archive folder | docs/archive/adrs  |   --archive PATH    `none` (the default) when there is no archive
```

`--root DIR` names the project root (default: the current directory), `--dir PATH` the decisions folder (default: the
first of `docs/decisions`, `docs/adr`, `docs/adrs`, `doc/adr`, `doc/decisions`, `adr`, `decisions` that exists) and
`--schema FILE` a schema other than the shipped one.

### Following a release

A project that follows ADR+ copies the files listed in `MANIFEST.sha256` into its own tree, keeps `VERSION` and the
manifest with them, records the version and the manifest's hash, and adds a check that fails when a copied file
differs from its line in the manifest. Moving to a new release is a deliberate commit (SPEC S7).

## What makes it different

- **Ruled and built are separate.** `status` says what was decided; `built` and `proof` say what exists, and the
  proof is a test or check that would fail if the decision stopped being true. A commit is never proof.
- **Ruled text is never rewritten.** Corrections are dated notes. A change of mind is a new ADR that amends or
  supersedes the old one, and both point at each other.
- **Agents propose; only the owner accepts.**
- **MADR's useful parts, only when needed.** Decision drivers and per-option pros and cons appear when two or more
  options were weighed; a simple decision stays short.

## Where it is used

- [pitmaster](https://github.com/MapleSyrupOS/pitmaster)'s `makeadr` skill writes ADR+ records.
- It was worked out over 232 ADRs in one large solo-owned project, which migrates to this spec first.

## Not to be confused with

**AdrPlus** (`FRACerqueira/AdrPlus`), an unrelated .NET command-line tool for managing ADRs. ADR+ is a format, not
a tool, and the two projects have no connection.

## Licence

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE), which credits MADR for the elements ADR+ takes from it.
