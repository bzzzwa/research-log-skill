# Methodology documents

One file per job. If two files would answer the same question, merge them. The
commonest failure is a single document that mixes a forward-looking plan with a
backward-looking record: the plan then cannot be rewritten without destroying
history, and the history cannot be trusted because it has been rewritten.

Split by **class** first, by topic second.

---

## README.md — living

The router. Someone who has never seen the project reads this and knows where to
go. Rewritten whenever the structure or the phase changes; `validate` warns when
its `**Last updated.**` is older than the plan's `**Updated.**`.

```markdown
# <Project title>

**Question.** <one or two sentences>
**Client / purpose.** <who this is for and what it feeds into>
**Phase.** <current phase> — see `methodology/10-plan.md`
**Last updated.** YYYY-MM-DD

## Where things are
- `methodology/` — how this research is being done and why
- `tasks/` — one directory per completed unit of work
- `sources/retrieved/` — dated snapshots of search and tool results
- the store (`store:`, located per machine in `research-log.local.ini`) —
  inbox, catalogued sources, large intermediates and files for use outside
  the project; see
  PROFILE.md for what is where
- `tools/` — the project's copy of rlcheck and the scripts the analysis uses
- `PROFILE.md` — source types and conventions specific to this project

## State
<3–5 sentences: what is done, what is running, what is blocked>

## Starting a session
Read `PROFILE.md`, `methodology/10-plan.md` and
`methodology/25-decisions-in-force.md`, then the record named as next.
Run `rlcheck status` from this directory; on a new computer, `rlcheck doctor`.
```

---

## methodology/00-brief.md — frozen

The assignment as received, verbatim, plus the scope agreed with the client.
This is the reference point everything else is audited against, so it must not
drift. The client's original documents live in `store:sources/brief/` and are
the inputs of the brief task (`t0001-brief`) that wrote this file, so a revised
original shows up in `rlcheck stale`. If the brief genuinely changes, put the
new original next to the old one, append a dated amendment section rather than
editing the original text, log the change in `20-decisions.md`, and run the
staleness check.

*Verbatim* means the wording is the client's: headings and lists may be set in
Markdown, nothing may be reworded, shortened or summarised. *Agreed scope* holds
only what the user or the client has stated; leave it empty until they have.

The date in the original's file name is the day the client delivered it, or, if
that is not known, the day it was taken over. A date printed in the document
is not the delivery date.

```markdown
# Brief

## As received (YYYY-MM-DD)
**Original.** `store:sources/brief/YYYY-MM-DD-<name>.<ext>` (transcribed in t0001-brief)

<verbatim>

## Agreed scope
**In scope.** <...>
**Out of scope.** <...>
**Deliverable.** <format, length, audience, deadline>

## Amendments
### YYYY-MM-DD
<what changed, who asked, what it invalidates>
```

---

## methodology/10-plan.md — living

What the work is and what comes next. Rewritten in place at the end of every
task. It states intent, never history — history lives in `20-decisions.md` and
in the task records. `**Updated.**` carries the date of the last rewrite, taken
from `rlcheck`; `validate` warns when it is older than the last closed task or
decision, or when *Next* still names a finished task.

It is not a schedule. Deadlines from the brief may be noted as context, but the
plan does not count down to them or pace the work, unless the researcher asks.

```markdown
# Plan

**Updated.** YYYY-MM-DD

## Phases
1. <phase> — done / running / not started
2. ...

## Now
<the task currently open, or none>

## Next
<the next one or two tasks, with the question each answers>

## Deferred
<things consciously postponed, and until when>

## Proposed
<ideas for new work proposed by Claude or anyone else, one line each with why;
nothing here is worked on until the researcher makes it a task>
```

---

## methodology/20-decisions.md — append-only

Every choice that a reader could reasonably have made differently. This is the
document that makes the research defensible, and the one that is worthless if it
is ever tidied up. Add entries; never edit them. A decision that replaces or
corrects an earlier one is a new entry that names it under `**Supersedes.**`;
that field is what lets `rlcheck decisions` derive which decisions still apply.

Log a decision whenever you: fix or change search vocabulary, set or relax an
inclusion or exclusion criterion, choose a database or stop using one, decide a
borderline source is in or out, change how a source type is processed, stop
searching (saturation), or accept a known weakness rather than fix it.

```markdown
# Decisions

## D012 — YYYY-MM-DD — <short title>
**Context.** <what prompted the choice>
**Decision.** <what was decided>
**Alternatives considered.** <and why not>
**Consequences.** <what this affects downstream; which tasks depend on it>
**Decided by.** <researcher / client / proposed by Claude, confirmed by the researcher / provisional>
**Supersedes.** <D003, or — if it replaces nothing>
```

`**Confirms.** D003` is an optional field for an entry whose purpose is to
confirm an earlier provisional decision. The confirmed decision stays in force
and the in-force view marks it as confirmed; nothing has to be restated. Use
`**Supersedes.**` only when the decision itself changes. A decision is
provisional when its `**Decided by.**` contains the word "provisional", or says
"proposed by Claude" without "confirmed"; `rlcheck status` lists those not yet
confirmed.

The header must keep the form `## D012 — YYYY-MM-DD — title`, and each field
starts its own line with the bold label ending in a full stop; `validate`
parses both. `**Decision.**` must not be empty. Ids are never reused, and a
decision can only supersede or confirm one that comes before it. Once an entry
is committed, `validate` fails if it is changed: correct it with a new entry.

After adding entries, run `rlcheck decisions` to regenerate
`25-decisions-in-force.md`.

---

## methodology/25-decisions-in-force.md — derived

The decisions that currently apply: every entry of `20-decisions.md` that no
later entry supersedes, with its Decision text, plus a table of what was
superseded by what. It is the answer to "what are the rules of this project
now?", however old the decision that set them.

Generated by `rlcheck decisions`, never written by hand. It carries the digest
of the log it was built from, and `validate` fails if it no longer matches a
fresh regeneration, so a stale or hand-edited copy cannot pass unnoticed.

Read this in a fresh session instead of the tail of the log. Go to
`20-decisions.md` only for the context and alternatives behind a decision.

---

## methodology/30-limitations.md — living

The open register of everything that weakens the result. Items are added as they
are discovered and their status is updated as they are handled, so the file is
living rather than append-only — but an item is only ever closed with a reason,
never deleted.

This is the document to read before writing any interpretation.

```markdown
# Limitations and gaps

| ID | Raised | Description | Affects | Status | Resolution |
|----|--------|-------------|---------|--------|------------|
| L004 | 2026-08-21 | No coverage of grey literature before 2015 | RQ2 | open | — |
| L003 | 2026-08-19 | Two workshop notes illegible in places | t0004 | mitigated | reconstructed from audio, see D008 |
```

Status: `open`, `mitigated`, `accepted` (with reason), `resolved`.

---

## methodology/40-insights.md — append-only

Observations that belong in the final output but not in the methodology: a
striking quotation, an unexpected pattern, a tension between two sources, a
question worth putting to the audience. Captured at the moment they occur,
because they are always lost otherwise.

Keep it strictly separate from `30-limitations.md`. A limitation is something
wrong with the research; an insight is something interesting about the subject.

```markdown
# Insights for the output

## I007 — YYYY-MM-DD — <short title>
**Observation.** <...>
**Where it came from.** <task id, source>
**Why it matters for the deliverable.** <...>
```

---

## methodology/90-deviations.md — derived

The current state audited against `00-brief.md`. Regenerated, not maintained:
delete and rewrite it whenever it is needed, from the brief plus the plan plus
the limitations register. Never hand-edit, because a hand-edited audit tells you
what you remembered rather than what is true.

Regenerate it before any delivery, and after any amendment to the brief.

```markdown
# Deviations from brief

**Generated.** YYYY-MM-DD against 00-brief.md as of <date of last amendment>

| Brief requirement | Current state | Deviation | Justified by |
|---|---|---|---|
| Cover EU and national level | EU complete, 3 of 5 countries | Partial | D011, time budget |
| Include grey literature | Post-2015 only | Partial | L004 |
```

---

## Mapping from an organically grown set

If a project already has methodology documents that grew ad hoc, map them like
this rather than starting over:

| Typical organic document | Where it goes |
|---|---|
| plan + running progress in one file | split: intent to `10-plan.md`, history to `20-decisions.md` and task records |
| procedure and decisions | `20-decisions.md`, one entry per decision |
| calibration against the assignment | `90-deviations.md`, and stop maintaining it by hand |
| known gaps and caveats | `30-limitations.md` as a table with status |
| notes for the final output | `40-insights.md` |
| index / router | `README.md` |

The split that matters most is the first one.
