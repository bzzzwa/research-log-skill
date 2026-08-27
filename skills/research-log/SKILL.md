---
name: research-log
description: Keep the methodology log and task records of a social-science desk-research project complete enough that any phase can be resumed in a fresh conversation with no loss of context. Use whenever working inside a research project directory that contains PROFILE.md or a methodology/ folder; when opening, closing or resuming a research task; when asked to record a methodological decision, log a limitation or caveat, update the plan, capture an observation for the final output, check deviations from the brief, check whether outputs have gone stale, or set up a new research project directory. Also use when the user says they are starting a new session, continuing earlier work, or asks what state the project is in.
---

# Research Log

Desk research in the social sciences cannot be handed to an agent end to end. The
searching is theory-laden, inclusion is a judgement call, and synthesis is the
researcher's work. What *can* be systematised is the bookkeeping: if every phase
leaves a complete written trace, the conversation itself stops being the memory,
and a fresh session costs nothing.

That is the whole purpose of this skill. It does not do research. It makes the
project resumable.

## Two layers

This skill is the general layer: file classes, record format, closing gate. It
is the same for every project.

`PROFILE.md` in the project root is the project layer: what the source types
are, how they are processed, what counts as a task, what the delivery format is.
It differs for every project. **Always read `PROFILE.md` before acting.** If it
is missing, create it with the user (see `reference/project-profile.md`).

Never put project-specific rules in this skill, and never put general rules in
`PROFILE.md`.

## File classes

Every file in the project belongs to exactly one class. The class determines how
it may be changed. Getting this wrong is the main source of lost context.

| Class | Rule | Examples |
|---|---|---|
| **frozen** | Written once. Any change is an event that is logged and invalidates downstream work. | `methodology/00-brief.md`, received primary materials, `sources/` |
| **living** | Rewritten in place to state what is true *now*. Git holds the history; the file does not. | `README.md`, `methodology/10-plan.md`, `methodology/30-limitations.md` |
| **append-only** | New entries are added at the end. Existing entries are never edited or deleted. | `methodology/20-decisions.md`, `methodology/40-insights.md` |
| **derived** | Regenerated from other files. Never hand-edited. | `methodology/90-deviations.md`, task outputs |

Full layout, contents and templates: `reference/documents.md`.

## Layout

```
README.md                     living    router: what this project is, where things are, current state
PROFILE.md                    living    the project layer (source types, task types, delivery)
methodology/
  00-brief.md                 frozen    the assignment, verbatim, plus agreed scope
  10-plan.md                  living    current plan and what comes next
  20-decisions.md             append    methodological decisions with rationale
  30-limitations.md           living    open register of gaps and caveats
  40-insights.md              append    observations captured for the final output
  90-deviations.md            derived   current state audited against 00-brief.md
tasks/
  t0001-<slug>/
    record.md                          the task record (schema in reference/task-records.md)
    <outputs>
sources/                      frozen    per PROFILE.md
```

Numbers leave gaps of ten so documents can be inserted without renumbering.

## Opening a task

1. Read `PROFILE.md`, then `methodology/10-plan.md`.
2. Create `tasks/tNNNN-<slug>/record.md` from the template with
   `status: planned`, the question it answers, and every input listed by path.
3. Run `python skills/research-log/scripts/rlcheck.py seal tasks/tNNNN-<slug>`
   to record the input digests.
4. Confirm the plan with the user before doing the work. Screening criteria,
   inclusion rules and search vocabulary are the user's decisions, not yours.

## Closing a task

A task is not finished when the work is done. It is finished when the record is
complete. Before saying a task is done, all of these must be true:

- `record.md` has every required section filled with substance, not placeholders.
- `status: complete` and a `closed:` date are set.
- Every declared output exists at the declared path.
- Every methodological decision made during the task has an entry in
  `methodology/20-decisions.md`.
- Every gap, doubt or compromise has an entry in `methodology/30-limitations.md`.
- `methodology/10-plan.md` has been rewritten to reflect the new state.
- `python skills/research-log/scripts/rlcheck.py validate` exits clean.

If a check fails, fix it before reporting completion. Do not report a task as
done and list what is still missing.

## Resuming in a fresh conversation

Read in this order, and stop as soon as you have enough:

1. `README.md` and `PROFILE.md`
2. `methodology/10-plan.md`
3. the last few entries of `methodology/20-decisions.md`
4. `methodology/30-limitations.md`
5. the `record.md` of the task named as next in the plan

Do **not** read the whole `tasks/` tree, the whole decision log, or any source
files that the plan does not point at. The read order exists to keep the fresh
session cheap; reading everything defeats the purpose.

Then run `python skills/research-log/scripts/rlcheck.py status` and report the
state to the user before proposing anything.

## Staleness

When a frozen input changes — the brief is revised, a source set is extended,
a primary document is corrected — every task downstream of it may need redoing.
This is a mechanical dependency question and must not be answered by reading and
guessing. Run:

```
python skills/research-log/scripts/rlcheck.py stale
```

It compares recorded input digests against current ones and names the affected
records. Then, for each one: decide with the user whether to rerun it or accept
it, log that decision in `20-decisions.md`, and either rerun and reseal, or set
`status: superseded` and open a replacement task.

## Never

- Never rewrite or tidy an entry in an append-only file. Add a new entry that
  corrects the old one and says so.
- Never edit a derived file by hand. Regenerate it.
- Never change a frozen file silently. Log the change as an event in
  `20-decisions.md` and run the staleness check.
- Never leave a task record with placeholder text. An empty section is more
  honest and more useful than an invented one.
- Never assess staleness, completeness or coverage by reading files when the
  script can answer it.
