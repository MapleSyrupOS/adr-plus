# ADR+ — the spec (draft)

**Status:** open — draft for the owner's ruling, 2026-10-18. Nothing here is ruled unless marked agreed.
**Builds on:** pitmaster's `docs/decisions/ADR-PLUS-profile.md` (accepted 2026-10-18). This spec does not edit the profile. If it is ratified, the profile gets a dated amendment pointing here.
**Changed by:** the bbq of 2026-10-18 on MADR features (pitmaster's `docs/bbq/2026-10-18-adr-plus-madr.md`). Rules it set are cited as *bbq Q4*, *bbq Q9* and so on; why ADR+ takes them is recorded in pitmaster's ADR-003 (accepted 2026-10-18).

## ADR+ in five minutes

Start here. Everything after this section is reference: the reasons, the edge cases, and what tools handle for you.

**One decision per file**, in `docs/decisions/ADR-NNN-<title-with-dashes>.md`. Never delete one, never renumber.

```
---
status: accepted
ratified-by: the owner
ratified-on: 2027-04-02
owner: the owner
kind: process
built: landed
proof: tests/test_flags.py::test_small_fixes_skip_flag
supersedes: nothing
amends: ADR-007 §Decision
---
# ADR-012 — Fixes under 20 lines skip the feature flag

## Decision
A fix under 20 lines lands without a flag. Everything else still follows ADR-007.

## Context
Flagging one-line fixes added a removal step to every typo (12 of the last 30 flags).

## Alternatives
- Flag every fix, as before: lost; the removal step costs more than the risk.

## Consequences
- Good: small fixes land in one step
- Bad: a 20-line fix can still change something people see
- Commits us to: counting lines in the landing check

## History
2027-04-02: proposed by an agent; ratified by the owner.
```

**Six rules:**
1. **The title is the decision**, as a sentence, not a topic.
2. **Decision first**, one paragraph. A reader who stops there knows the choice.
3. **status** is what was ruled; **built** is what exists; **proof** is something that would fail if the decision stopped being true.
4. **Agents propose; only the owner accepts.**
5. **Never rewrite ruled text.** Corrections go in History as dated notes. A change of mind is a new ADR that amends or supersedes the old one, and both point at each other.
6. **Keep what lost.** Every option weighed stays in Alternatives; a recommendation the owner overruled is marked (overruled).

**Add only when it's true** (1.7):

| When | Add |
|---|---|
| 2+ options were weighed | a Drivers list in Context; Good/Bad bullets per option; the deciding reason on the chosen option's heading |
| No test can prove it | `confirmed-by:` the human check |
| A known event or date could undo it | `revisit-when:` |
| Anyone besides the owner shaped it | `consulted:` |
| The owner declines a proposed ADR | keep it, `status: rejected`, one line why |

**Leave to the tools:** makeadr runs the question session and writes the file; the checkers keep the index, the header and the triggers honest (Part 5).

---

## What ADR+ is

An ADR (architecture decision record) is a short file that records one decision and why. ADR+ is a way of writing them, worked out over 232 ADRs in a large solo-owned OS project (the *reference project*) and packaged in pitmaster's `makeadr` skill. This spec writes it down in one place for the first time, so it works for any project and any owner, not only the one it grew up in.

It has three parts:
- **The core.** Rules you can follow with nothing but a text editor.
- **Project settings.** The few things each project fills in for itself.
- **The verified layer.** Optional checkers, and what to add as a project grows.

It also takes the useful parts of MADR (Markdown Architectural Decision Records), each written only when the decision needs it (1.7).

Each rule cites where it came from in the reference project. Paths are in that repository.

---

## Part 1 — The core

### 1.1 One decision per file
- File name: `ADR-NNN-<the-title-in-lowercase-with-dashes>.md`, all in one decisions folder.
- A number is never reused, renamed or renumbered, and an ADR is never deleted. (Ref: in 232 ADRs, none has ever been deleted or renumbered.)

### 1.2 The title is the decision
Write the title as the decision in one sentence, not a topic. "A registered count is a property of the file", not "Counts". The index shows the title as its summary of the decision, so a topic title makes an index row that says nothing. (Ref: `tools/adr-index.py`; titles of ADR-140 onwards.)

### 1.3 The header
A YAML block at the top of the file, one field per line, values in plain words. GitHub shows it as a two-column table above the title. It is checked against a JSON Schema (5.1). (bbq Q6, Q21.)
```
---
status: accepted
ratified-by: the owner
ratified-on: 2026-10-18
owner: the owner
kind: process
built: landed
proof: tests/test_flags.py::test_new_flags_default_off
supersedes: nothing
amends: nothing
---
# ADR-007 — New features land switched off until the owner approves the look
```
Always present:
- **status** says what was ruled, in one of seven words: proposed (drafted, waiting for a ruling), provisional (an agent had to land it first), accepted (ruled yes), partially accepted (ruled yes for part of it), superseded (replaced by a newer ADR), withdrawn (no longer in force, and nothing replaced it), rejected (proposed, ruled no). While an ADR is proposed, `ratified-by` and `ratified-on` stay empty. (Owner's ruling S2.)
- **ratified-by / ratified-on** say who ruled and when.
- **owner** is the person answerable for the decision from now on. In a solo project it is the same person who ratified; in a team it may not be. (bbq Q12.)
- **kind** is architecture, design or process, and is required. (Agreed in the ADR+ profile; S3.) A project that groups its index by area lists its areas in its settings and adds an `area` field; it is then required in that project. (S3.)
- **built** says what exists, apart from what was ruled, because a decision can be accepted and not yet built, or replaced and still running: landed, partial, not started or n/a. **proof** names the evidence (1.4); for n/a it names the rule or file the decision became. A partial ADR adds **owed:** with what is still missing. (Ref: ADR-198.)
- **supersedes / amends** are always written, even as "nothing". If the field is missing, a reader can't tell "nothing" from "nobody checked". An amendment names the section: `amends: ADR-004 §Decision`. (Ref: 20 of the 24 ADRs with this line say "nothing"; ADR-198.)

Written only when their trigger is true (1.7):
- **consulted**: the agents, models, lanes or people who shaped it, e.g. `consulted: Fable survey, s35 lane review`. (bbq Q12.)
- **confirmed-by**: the human check, when no test can prove it. (bbq Q13.)
- **revisit-when**: an event or a date that could undo it, e.g. `revisit-when: the first boot on real hardware`. (bbq Q14.)

When a field's value changes, the old value moves into History, word for word. (Ref: fix-board ruling 8, 2026-09-22.) Only the fields named here and in the project settings (Part 4) are allowed; a project adds a field by a rule, not by habit. (Ref grew more than 40 different header fields by habit.)

### 1.4 Proof that something was built
A LANDED or PARTIAL Built line names something that **could fail if the decision stopped being true**: a test, a check, or a file that must exist. Every proof named must actually exist. A green that cannot go red is not evidence. **A commit is never proof:** it shows something was saved, not that it still works. A commit may follow a real proof, for history. (Ref: ADR-198 §3 and §4.6; S1.)

Some decisions can't be tested: a taste rule, a process. Then `built` is n/a or names no automatic check, and **confirmed-by** names the human check instead, e.g. "the owner's veto at preview, every user-visible landing". This is MADR's Confirmation, kept for the cases where ADR+'s proof can't reach. (bbq Q13.)

This is what other people call a *fitness function*: an automatic check that a decision still holds. In the reference project they are called drills and checks.

### 1.5 The sections, in this order
1. **Decision** — one paragraph, in plain words, that fits on the first screen. A reader who stops here knows the choice and its scope.
2. **Context** — the problem and what was true at the time. Cite sources, not memory. When 2+ options were weighed, end with a short **Drivers:** list: the forces that decided between them. A driver may cite the project's doctrine rather than restate it ("Doctrine: function first"). (bbq Q8.)
3. **Alternatives** — every option weighed, its honest trade-off, and why it lost. When 2+ options were weighed, each gets a short heading and Good/Bad bullets. The chosen one comes first, and its heading carries the deciding driver: `### Feature flag, off by default (chosen: merges must not wait)`. A recommendation the owner overruled stays here, marked **(overruled)**; otherwise it will be proposed again. (Ref: CLAUDE.md iron rules; bbq Q9, Q10.)
4. **Consequences** — bullets that start **Good:** or **Bad:**, then one **Commits us to:** line. (bbq Q11.)
5. **Asks left open** — only while the ADR is PROPOSED: the questions still waiting for the owner, numbered.
6. **History** — ratification, amendments, corrections and old Status/Built wording, oldest first.

Keep everything before the Decision section to one short paragraph. Ratification stories go in History. (Ref: in its 2026-09-22 readability review, many ADRs had 264 words of preamble before the decision, and some had grown into 1,000-line work logs.)

### 1.6 Write for a reader who isn't a programmer
Plain words, the decision first, and every term the owner asks about added to the glossary. If the owner can't read an ADR, they can't really ratify it. The YAML header doesn't change this: its values are plain words, one per line, and the body below reads as sentences. (bbq Q20.)

### 1.7 What ADR+ takes from MADR, and when
MADR (https://adr.github.io/madr/) is the most widely used ADR template with options laid out side by side. ADR+ takes its useful parts without making every ADR longer: **each one has a trigger and is written only when the trigger is true.** A decision with one obvious option stays as short as before. (bbq Q4.)

| From MADR | In ADR+ | Trigger |
|---|---|---|
| Decision Drivers | `Drivers:` list at the end of Context | 2+ options weighed |
| Considered Options + Pros and Cons | Options with Good/Bad bullets inside Alternatives | 2+ options weighed |
| "Chosen option: X, because Y" | The reason on the chosen option's heading | 2+ options weighed |
| Consequences (Good / Bad) | Good/Bad bullets plus "Commits us to:" | Always |
| decision-makers, consulted | `owner` (always) and `consulted` | consulted: anyone besides the owner shaped it |
| Confirmation | `confirmed-by` | No test can prove it |
| "when to revisit" (More Information) | `revisit-when`: an event or a date | A known event or date could undo it |
| status: rejected | `status: rejected`, kept in place (Part 2) | The owner declines a proposed ADR |
| YAML front matter | The header (1.3) | Always |

Not taken: More Information (its parts are covered by `revisit-when`, Context's citations and the header links), Neutral bullets, and the informed list.

Section names stay ADR+'s own. For readers and tools that know MADR (bbq Q7):

| ADR+ | MADR |
|---|---|
| Decision | Decision Outcome |
| Context | Context and Problem Statement |
| Alternatives | Considered Options + Pros and Cons of the Options |
| Consequences | Consequences |
| `built` + `proof` | Confirmation (ADR+'s is checked; MADR's is prose) |
| History | (none) |

**The safeguard works both ways.** makeadr follows the triggers during its question rounds, and the checker fails an ADR whose trigger is true but whose feature is missing (options listed without Good/Bad bullets) and one whose feature is present but whose trigger is false (a Drivers list on a one-option decision). (bbq Q4.)

---

## Part 2 — Changing a decision

**Ruled text is never rewritten.** It is annotated. (Ref: the owner's "notes, never repairs" ruling, 2026-08-19; ADR-174.)

There are four kinds of change. Pick by asking two questions: *does any of the old decision still hold?* and *is it still worth reading?*

| What happened | What to do | The old ADR |
|---|---|---|
| A clarification, a correction, a narrower scope | A dated note in its **History** | Text unchanged; the note says what changed and who agreed |
| **Part** of the decision changed | A new ADR with `amends: ADR-N §X` naming the section | A dated note in its `status` (`accepted, amended in part by ADR-M on <date>`) **and** a dated banner at the section that changed |
| **The whole** decision flipped | A new ADR with `supersedes: ADR-N`, saying why | `status` becomes `superseded by ADR-M on <date>`; the old value moves to History; body untouched |
| Still true, but no longer worth reading day to day | **Demote**: move it to the archive folder | Status unchanged; still in the index, marked archived |
| The owner declines a **proposed** ADR | Nothing new | Status becomes rejected, with one line why; it keeps its number and file, so it isn't proposed again (bbq Q15) |

Rules for every change:
- **Write both ends, in the same commit.** The new ADR points back, and the old one points forward, at the head and at the place that changed. A reader who lands in the middle of the old file must not need the top of the file to know the rule changed. (Ref: ADR-159; the ADR-098 → ADR-103 one-way supersession found 2026-08-19; wayfinding check 16.)
- **Credit the ADR that ruled.** When something cites a decision, it names the ADR that made the ruling, not the one that first raised the question. (Ref: local-queue finding 2026-08-17.)
- **Never delete, never renumber.** Demote instead. (Ref: "demote, don't delete", 2026-09-12.)

The reference project has used the first, second and fourth kinds; none of its ADRs was ever fully superseded. Projects whose decisions are checked less carefully up front will need full supersession more often.

---

## Part 3 — Before a decision is ruled (the front door)

These checks happen before an ADR exists. They are why so much of the reference project's change could be handled with notes rather than reversals.

1. **Has it been ruled already?** Search the decisions folder, the index, the decisions queue and earlier question records. A question already ruled is cited, never asked again. (Ref: charter, "before asking, check whether he already ruled"; makeadr §2.)
2. **Check every premise.** Each question rests on facts about the project. Check each one with a search or a file listing, and record it in a premises table. An empty search is a claim about the search pattern, not about the project. (makeadr §2.)
3. **Sort each question before asking it.** Taste (looks, names, wording) is always asked. Strategy is asked. A mechanism question with one plain answer that everyone uses is not asked; it goes in a **Defaulted** table with who does it that way and a `veto:` line, and the owner ratifies the table. (Ref: ADR-180; makeadr §3.)
4. **Price every option** and give a recommendation, first in the list. The currencies are a project setting. (makeadr §3.)
5. **Write each round into the record before asking the next,** and commit the record before the first round. (makeadr §2 and §3.)
6. **A question entry with several parts is closed whole or not at all.** Parts that were answered are noted in place. (Ref: decisions-queue preamble.)

How much these checks prevented reversals is hard to measure. The reference project's change mostly arrived as notes and partial amendments, which the rules above make cheap. Drift between the records and the code was still caught repeatedly, but by checkers after the fact (Part 5), not at the front door.

The owner recalls (2026-10-18) that many of these checks began as their own questions to agents — "how did this happen?", "I've asked this before" — before any of them were written down. Not yet traced to particular conversations; a search of past chats could confirm it.

---

## Part 4 — Who rules, and project settings

### 4.1 The ownership gate
- **Agents propose; the owner ratifies.** An agent writes PROPOSED. An ADR is ACCEPTED only when the owner rules. (Ref: charter §Delegated authority, "ADR ratification … never delegated".)
- **Ratifying and owning are separate fields.** `ratified-by` says who ruled; `owner` says who answers for the decision from now on. (bbq Q12.)
- **Agents fill `consulted`** with their own name, model or lane when they shaped the decision.
- **PROVISIONAL** is for work an agent had to land before a ruling. It is listed in one place until the owner rules, and that list is itself a claim that can go stale. (Ref: PROVISIONAL-index; overnight PROTOCOL §4.)

### 4.2 Settings each project fills in
Kept in the decisions folder's `README.md`.

| Setting | What it is | The reference project's value |
|---|---|---|
| **Ratifier** | Who may rule. Default: one named owner. A project may set a group instead (e.g. "any two of Alex, Sam"); `ratified-by` then lists who ruled (S4) | Its owner |
| **Delegable** | What an unattended agent may decide provisionally | Reversible technical choices; never anything on screen |
| **Proof kinds** | What counts as proof on a Built line | Drill rows, `tools/` paths, wayfinding checks |
| **Areas** | Optional groups beyond Kind, for the index; when set, each ADR stores its `area` (S3) | Kernel, Networking, Apps, Desktop… (today guessed from titles; to be stored) |
| **Option costs** | The currencies options are priced in | Sessions to write, and bytes carried |
| **Decision-first limit** | How long the preamble may be | One paragraph |
| **Folders** | Decisions, archive, question records, decisions queue | `docs/decisions/`, `docs/archive/dev-notes/`, `docs/reviews/`, `docs/overnight/decisions-queue.md` |
| **Extra header fields** | Any fields beyond the core set | `Modern:` and `Ours:` (from ADR-180) |

---

## Part 5 — The verified layer, and what to add as you grow

### 5.1 Checkers (optional, recommended)
`makeadr` already ships two:
- `adr-index.py` builds the index from the ADRs themselves; nobody edits it by hand.
- `adr-check.py` checks Status and Built lines and that every proof exists.

Worth adding, from the reference project:
- **Both ends:** every Supersedes or Amends claim is acknowledged by the old ADR (Ref wayfinding check 16).
- **Claims match verdicts:** when STATUS or the debt list says "ADR-N is accepted", the ADR agrees (Ref check 22).
- **The owed audit:** the `owed:` field of a partial ADR goes stale silently, so it is re-read on a rotation. (Ref: ADR-198 §2.)

Added by the bbq on MADR features:
- **The schema check:** every header is validated against a JSON Schema: field names, allowed words, and an ADR number in every `supersedes` and `amends`. The owner's `.asf.yaml` validator is the model for it. (bbq Q6, Q22.)
- **The trigger check:** both ways, as in 1.7. (bbq Q4.)

### 5.1a Converting to ADR+
One converter takes a MADR file, a classic (Nygard) ADR or an old bold-line ADR+ and writes ADR+. It moves what exists and **never invents a value**; everything still missing (built and proof, kind, owner, drivers for a multi-option decision) is listed as a warning for a person to fill in. A classic ADR will usually come out with a long list. (bbq Q21.)

Migrating a project's ADRs is proven by machine, not by eye (bbq Q22):
1. Every old header value appears in the new YAML.
2. The body below the header is byte-identical.
3. The YAML passes the schema check.
4. A second model from outside the session (Codex or Gemini) reviews the diffs.

The header changes length, so old dated records that cite an ADR by line number will point at the wrong line. Live documents are re-aimed; dated records are left as they were. (bbq Q6.)

### 5.2 Add when you grow

| When | Add | Why (reference project) |
|---|---|---|
| A hand-kept index starts to drift | The generated index | The hand index reached 59,255 words |
| Two people or boards draft ADRs at once | Number reservation: a lead hands out numbers, unused ones are returned, and the history is searched before a number is taken | ADR-250 was numbered 250 to avoid a reserved range |
| About ten or more ADRs await ruling | Batch ratification: tick items apart from judgement items; every "landed" claim checked against the project, not the ADR | `RATIFICATION-BATCH-2026-07-30` |
| Hundreds of ADRs | Demotion to an archive, with every checker widened to include the archive the same day | 13 demoted ADRs fell outside all three checkers until fixed |
| An owner who can't read code | A plain-English digest of each ADR, checked against its source; UNSUPPORTED is the verdict that matters most | `docs/adr-digest/` |

### 5.3 The index
One row per ADR: number, title, Kind, Status word, Built word. Active ADRs first; superseded, withdrawn and rejected below, kept as history; demoted ones marked archived. (Agreed in the ADR+ profile. The reference project's index is one table; with nothing superseded there, the split costs it nothing.)

Below the table, a **Revisit** list: every open `revisit-when`, so a status review can scan them. (bbq Q14.)

---

## Part 6 — Rules for agents

- Follow the active ADR. Superseded ADRs are history only.
- Never edit ruled text. Propose an amendment for the owner to approve.
- Cite an ADR by number and section, and anchor by content, never by line number, in files that change. (Ref: CLAUDE.md iron rule; ADR-044's line-number slip.)
- Dated records keep their old citations; only live documents are re-aimed. (Ref: archive README.)
- Anything that claims an ADR's verdict (STATUS, the debt list, a handoff) must match the ADR.

---

## The owner's rulings on the open questions (2026-10-18)

Asked as S1–S5 in chat, after ADR-003 was ratified.

- **S1 Commits as proof.** Never counts. A commit may follow a real proof for history; alone it never makes an ADR landed. (1.4)
- **S2 Status words.** Seven, lowercase: proposed, provisional, accepted, partially accepted, superseded, withdrawn, rejected. The converter maps older words: ratified, adopted, ruled, landed → accepted; deprecated, retired, closed → withdrawn; nixed → rejected; draft, awaiting → proposed. (1.3)
- **S3 Kind and Area.** Kind is required in every ADR. Area is optional per project; a project that turns it on stores it in each ADR. (1.3, 4.2)
- **S4 Ratifier.** One named owner by default; a group is a project setting. (4.2)
- **S5 Where the spec lives.** Its own repository, as MADR has (adr/madr: own repo, website, versioned releases, changelog, templates folder). The owner added: "we'll need to put safeguards in to ensure it stays updated."
- **S6 Name.** ADR+ (display) and adr-plus (machine), kept after a clash check: `FRACerqueira/AdrPlus` is an unrelated .NET ADR tool (0 stars, marked "being replaced"), and its author's AdrPlus plugin manages ADRs from Claude Code. YADR was considered and dropped: readers would take it for Y-ADR (Y-statements) and the `helsing-ai/yadr` linter. The README says ADR+ is unrelated to the AdrPlus tool.
- **S7 Safeguards.** ADR+ publishes numbered releases. Each follower (pitmaster's makeadr, the reference project) records the version it follows, and a check fails when its copy of the template or schema differs from that release. Moving to a new version is a deliberate commit; a weekly check may flag a newer release.
- **S8 Licence.** Apache-2.0, like pitmaster.
- **S9 The repository.** `writerblockade/adr-plus`, private first, holding the spec, the five-minute page, a README and the licence. The schema and converter arrive after the reference project proves them (bbq Q19). Edits to the spec go there from now on.
- *(Settled earlier)* makeadr changes: by bbq Q19, the reference project goes first; makeadr follows what worked.

## Sources

From the reference project's repository at `origin/main`, 2026-10-18: `docs/decisions/TEMPLATE.md`, `docs/decisions/INDEX.md`, ADR-100, ADR-159, ADR-174, ADR-180, ADR-198, ADR-250, `docs/charter-v10.1-PASTE-READY.md`, `CLAUDE.md`, `.claude/skills/makeadr/SKILL.md`, `docs/overnight/PROTOCOL.md`, `docs/archive/dev-notes/PROVISIONAL-index.md`, `docs/archive/README.md`, `docs/reviews/opus55-readability-2026-09-22/`, `docs/reviews/boiling-down/README.md`, `docs/adr-digest/VERIFICATION-SPEC.md`, `tools/adr-index.py`, `tools/adr-built.py`, `tools/check-wayfinding.py`. Gathered by two read-only agent surveys; individual line citations were not re-checked by hand.
