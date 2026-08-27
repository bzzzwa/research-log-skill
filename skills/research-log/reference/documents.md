# Methodology documents

One file per job. If two files would answer the same question, merge them. The
commonest failure is a single document that mixes a forward-looking plan with a
backward-looking record: the plan then cannot be rewritten without destroying
history, and the history cannot be trusted because it has been rewritten.

Split by **class** first, by topic second.

---

## README.md — living

The router. Someone who has never seen the project reads this and knows where to
go. Rewritten whenever the structure or the phase changes.

```markdown
# <Project title>

**Question.** <one or two sentences>
**Client / purpose.** <who this is for and what it feeds into>
**Phase.** <current phase> — see `methodology/10-plan.md`
**Last updated.** YYYY-MM-DD

## Where things are
- `methodology/` — how this research is being done and why
- `tasks/` — one directory per completed unit of work
- `sources/` — <per PROFILE.md>
- `PROFILE.md` — source types and conventions specific to this project

## State
<3–5 sentences: what is done, what is running, what is blocked>

## Starting a session
Read `PROFILE.md`, then `methodology/10-plan.md`, then the record named as next.
Run `python skills/research-log/scripts/rlcheck.py status`.
```

---

## methodology/00-brief.md — frozen

The assignment as received, verbatim, plus the scope agreed with the client.
This is the reference point everything else is audited against, so it must not
drift. If the brief genuinely changes, append a dated amendment section rather
than editing the original text, log the change in `20-decisions.md`, and run the
staleness check.

```markdown
# Brief

## As received (YYYY-MM-DD)
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
in the task records.

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
```

---

## methodology/20-decisions.md — append-only

Every choice that a reader could reasonably have made differently. This is the
document that makes the research defensible, and the one that is worthless if it
is ever tidied up. Add entries; never edit them. A superseded decision gets a new
entry that says which one it replaces.

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
**Decided by.** <researcher / agreed with client / provisional>
```

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
