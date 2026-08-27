# Task records

A task is a unit of work that answers one question and leaves one set of
outputs. It is the smallest thing that should survive a lost conversation.

One directory per task: `tasks/tNNNN-<slug>/`, containing `record.md` and the
outputs themselves. Records are never deleted. A task that turns out to be wrong
is marked `superseded` and replaced by a new one that says what it replaces.

## Template

```markdown
---
id: t0007
title: Screening of EU-level policy documents
status: planned
opened: 2026-08-20
closed:
inputs:
  - path: sources/policy/eu
    digest:
  - path: methodology/00-brief.md
    digest:
outputs:
  - path: tasks/t0007-eu-screening/screening.csv
supersedes:
---

## Question
<the single question this task answers, in one sentence>

## Method as executed
<what was actually done, not what was planned — including search strings,
databases, dates of retrieval, screening criteria applied>

## What was done
<narrative, enough that someone can tell whether to trust the result>

## Findings
<the substantive result; the outputs carry the detail>

## Limitations raised
<what went wrong or stayed uncertain; each item also gets an entry in
methodology/30-limitations.md>

## Handoff
<what a fresh session needs to know to continue: state, open threads,
the single next action>
```

## Front matter

| Field | Meaning |
|---|---|
| `id` | `tNNNN`, unique, never reused |
| `title` | short, human |
| `status` | `planned`, `in-progress`, `complete`, `superseded` |
| `opened` / `closed` | ISO dates; `closed` required when `complete` |
| `inputs` | every file or directory the result depends on, each with a `path` and a `digest` |
| `outputs` | every file this task produced |
| `supersedes` | id of the record this one replaces, or empty |

The front-matter parser deliberately supports only this shape. Anything more
elaborate will raise an error rather than be silently misread.

## Inputs are the dependency declaration

`inputs` is not documentation. It is what makes staleness detectable. List every
input, including methodology documents when the task depended on them — a
screening task depends on the brief, because a revised brief invalidates the
screening.

After creating or editing a record's input list:

```
python skills/research-log/scripts/rlcheck.py seal tasks/t0007-eu-screening
```

This computes each digest and writes it into the record. A file gets
`sha256:...`; a directory gets `tree:...`, a hash over the sorted relative paths
and contents of everything inside it, so adding one PDF to a source folder is
detected.

## Method as executed, not as planned

The section most often written wrong. If the plan said three databases and you
searched two, this section says two. The plan is not evidence of what happened;
this record is. A discrepancy between plan and execution is normal and belongs
in `methodology/20-decisions.md` as a decision, not hidden by rewriting either
document.

## Handoff

Write it for someone who has read nothing else. Three things: where the work
stopped, what is unresolved, what the single next action is. If it takes more
than a short paragraph, the task was too large and should have been split.

## Commands

```
python skills/research-log/scripts/rlcheck.py status               # summary for a new session
python skills/research-log/scripts/rlcheck.py validate             # structure of every record
python skills/research-log/scripts/rlcheck.py stale                # inputs that have drifted
python skills/research-log/scripts/rlcheck.py seal tasks/t0007-... # record current input digests
```

Run from the project root. `validate` and `stale` exit non-zero when they find
something, so they can be wired into a pre-commit hook.
