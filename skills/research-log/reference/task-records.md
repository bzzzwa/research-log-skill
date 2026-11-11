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
checkpoint:
closed:
performed-by:
inputs:
  - path: store:sources/policy/eu
    digest:
  - path: methodology/00-brief.md
    digest:
decisions: []
limitations: []
retrievals: []
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
methodology/30-limitations.md and its id under limitations: above>

## Handoff
<what a fresh session needs to know to continue: state, open threads,
the single next action>
```

The angle-bracket lines are template text. `validate` treats any `<...>` left in
a complete record as a placeholder and fails, so replace every one. If a
section genuinely has nothing to say, write `None.` and the reason — for
example "None. Screening criteria were applied without borderline cases."

Text inside code (fenced blocks or `` `inline` ``) is never scanned, so search
strings with `<` or `>` in them belong in code.

## Front matter

| Field | Meaning |
|---|---|
| `id` | `tNNNN`, unique, never reused |
| `title` | short, human |
| `status` | `planned`, `in-progress`, `complete`, `superseded` |
| `opened` / `closed` | ISO dates; `closed` required when `complete` |
| `checkpoint` | ISO date-time when `## Method as executed` and `## Handoff` were last brought up to date; required when `in-progress` |
| `performed-by` | who did the work: the researcher, or the model (name and version) and environment, and whether the researcher reviewed it; required when `complete` |
| `inputs` | every file or directory the result depends on, each with a `path` and a `digest` |
| `decisions` | ids from `methodology/20-decisions.md` made during this task, e.g. `[D012, D013]` |
| `limitations` | ids from `methodology/30-limitations.md` raised during this task, e.g. `[L004]` |
| `retrievals` | snapshot directories under `sources/retrieved/` this task's result depends on |
| `outputs` | every file this task produced |
| `supersedes` | id of the record this one replaces, or empty |
| `resealed` | written by `rlcheck seal --rerun/--accept`, never by hand: each change of an input digest after the task was finished, with the decision behind it |

The front-matter parser deliberately supports only this shape: scalars, short
inline lists like `[D012, D013]`, and block lists of scalars or of `path:`
mappings. Anything more elaborate, including a repeated key, raises an error
rather than being silently misread.

## Declarations: decisions, limitations, retrievals

These three keys turn "every decision has an entry in the log" from a promise
into something the script can check. For a complete record:

- each key must be present; `[]` when there is nothing to list,
- every listed decision id must exist in `20-decisions.md`,
- every listed limitation id must exist in `30-limitations.md`,
- every listed retrieval must be a snapshot directory with a valid
  `retrieval.md`, and must also be covered by `inputs` (listed itself, or
  inside a listed directory), so that its digest is tracked.

Retrievals may be written as an inline list or a block list:

```yaml
retrievals:
  - sources/retrieved/2026-09-05-wos-open-science
  - sources/retrieved/2026-09-05-cordis-open-science
```

The script can check that the ids exist. It cannot check that every decision
you made is listed; that part is still yours.

## Inputs are the dependency declaration

`inputs` is not documentation. It is what makes staleness detectable. List every
input, including methodology documents when the task depended on them — a
screening task depends on the brief, because a revised brief invalidates the
screening. A task that used a retrieval snapshot lists it here as well as under
`retrievals`.

After creating or editing a record's input list:

```
rlcheck seal tasks/t0007-eu-screening
```

This computes each digest and writes it into the record. A file gets
`sha256:...`; a directory gets `tree:...`, a hash over the sorted relative paths
and contents of everything inside it, so adding one PDF to a source folder is
detected. An input without a `digest:` line gets one. Only the `inputs` block is
touched.

## Paths

A path is either relative to the project root (`methodology/00-brief.md`,
`tasks/t0006-eu-search/results.csv`) or a store path (`store:sources/eu`,
`store:exports/report.pdf`). Never write a machine's own path into a record:
it is wrong on every other computer.

- Inputs may come from the repository or from `store:sources/`, never from
  `store:inbox/`. A file in the inbox enters the record when a cataloguing task
  takes it in: the researcher moves it to `store:sources/` with the command the
  model prepared, the model checks its digest, and the task lists it among its
  outputs.
- Outputs are text in the task directory. The only outputs in the store are
  catalogued sources (`store:sources/`), large intermediates
  (`store:work/<task id>/`) and files for use outside the project
  (`store:exports/<task id>/`).
- When the task's product is a script, the script is an output in git and the
  files it generates are outputs in the store, never in a git-ignored folder of
  the repository. The data it reads are inputs, so `stale` shows when the files
  need generating again.
- Instructions a model followed for an analytic step (a prompt, a coding frame,
  an extraction template) and scripts the task ran are inputs too.

On a machine where the store is not available, `seal` cannot read store inputs.
It keeps their previous digest, says so and exits non-zero. Seal on a machine
that has the store before closing the task.

Once a record is `complete` or `superseded`, `seal` will not change a digest on
its own. When an input changed after the task was finished, decide with the
user, log the decision, and run `seal` with `--rerun D0NN` (the work was redone)
or `--accept D0NN` (the old result stands). The change is then recorded under
`resealed:` in the front matter:

```yaml
resealed:
  - path: store:sources/policy/eu
    kind: accepted
    decision: D014
    date: 2026-11-20
    was: tree:3f2a…
    now: tree:91c0…
```

## Method as executed, not as planned

The section most often written wrong. If the plan said three databases and you
searched two, this section says two. The plan is not evidence of what happened;
this record is. A discrepancy between plan and execution is normal and belongs
in `methodology/20-decisions.md` as a decision, not hidden by rewriting either
document.

The same holds for an approved method. Steps done in another order than the
method says, a step skipped or added, a rule changed or applied differently:
each is written here when it happens, not reconstructed later. If rules for a
judgement (a scale, criteria, a coding frame) were written down only after the
judgements were made, this section says so.

Exact queries do not need to be repeated here; point to the snapshot, whose
manifest holds them verbatim.

## Handoff

Write it for someone who has read nothing else. Three things: where the work
stopped, what is unresolved, what the single next action is. If it takes more
than a short paragraph, the task was too large and should have been split.

While the task is in progress, the handoff is rewritten at every checkpoint
(see *While a task is open* in `SKILL.md`) and `checkpoint:` is updated with
it. `rlcheck status` prints the handoff and checkpoint of every in-progress
task, so a session hook can put them in front of the model after a compaction.
A handoff that is out of date is worse than none, because it is believed.

## What validate checks

| Status | Checked |
|---|---|
| any | front matter parses; required keys present; id unique; dates are ISO dates, not after today, and a task is not closed before it opened; inputs exist and none is in the inbox; store outputs are in `sources/`, `work/` or `exports/`; all six sections present; `## Question` filled with no placeholder |
| `planned`, `in-progress` | missing outputs are warnings |
| `in-progress` | `## Handoff` filled with no placeholder; `checkpoint` set to an ISO date or date-time |
| `complete` | `closed` and `performed-by` set; no section empty; no placeholder anywhere; every output exists; `decisions`, `limitations`, `retrievals` declared and resolvable; every `resealed` entry names a decision in the log |

`superseded` records are checked only for structure.

Store paths that cannot be reached on this machine are reported as not checked,
not as failures. A store that is reachable but is not this project's store (its
marker names another project) is a failure.

## Commands

See *Running the checks* in `SKILL.md` for how `rlcheck` is invoked and what to
do when you cannot run it yourself.

```
rlcheck status               # state for a new session, with handoffs of open tasks
rlcheck validate             # records, logs, snapshots, derived files
rlcheck stale                # inputs that have drifted
rlcheck check                # both of the above
rlcheck seal tasks/t0007-... # record current input digests
```
