---
name: research-log
description: Keep the methodology log and task records of a social-science desk-research project complete enough that any phase can be resumed in a fresh conversation with no loss of context. Use whenever working inside a research project directory that contains PROFILE.md or a methodology/ folder; when opening, closing or resuming a research task; when asked to record a methodological decision, log a limitation or caveat, update the plan, capture an observation for the final output, save or snapshot search results from a database, website or tool, check deviations from the brief, check whether outputs have gone stale, or set up a new research project directory or an existing project on another computer. Also use when the user says they are starting a new session, continuing earlier work, or asks what state the project is in, and after the context has been compacted while a research task is open.
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
is missing, the project is not set up yet: see *Setting up a project*.

Never put project-specific rules in this skill, and never put general rules in
`PROFILE.md`.

## Running the checks

Completeness, staleness and the current set of decisions are answered by
`scripts/rlcheck.py` in this skill's directory, never by reading and judging.
Below, `rlcheck <command>` stands for

```
python <this skill's directory>/scripts/rlcheck.py <command>
```

run with the **project root** as the working directory. The script works on the
current directory, so it does not matter where the skill itself is installed.

**When you can execute commands in the project** (Claude Code, or any
environment where the project directory is your working directory): run the
command yourself and act on its output.

**When you cannot** — for example in Claude.ai working through a Filesystem
connector, which reads and writes the user's files but cannot execute anything
on their machine — do not skip the step and do not guess its result. Give the
user the exact command, ask them to run it from the project root and paste the
output, and wait. Until the output is in the conversation, the step has not
happened: do not report a task as closed or a project as fresh.

Never say a check passed unless you have seen its output in this session.

| Command | What it answers |
|---|---|
| `rlcheck doctor` | is this project set up on this machine, and what to fix if not |
| `rlcheck init ...` | create or complete the setup (see *Setting up a project*) |
| `rlcheck claude-settings` | give Claude Code access to the store and install the session hook |
| `rlcheck where store:<path>` | where a store path is on this machine |
| `rlcheck status` | state of the project, for the start of a session |
| `rlcheck validate` | are records, logs and snapshots complete and consistent? |
| `rlcheck stale` | which records depend on inputs that have changed? |
| `rlcheck check` | `validate` and `stale` together; what a pre-commit hook runs |
| `rlcheck seal tasks/tNNNN-<slug>` | record the current digests of a task's inputs |
| `rlcheck decisions` | regenerate `methodology/25-decisions-in-force.md` |
| `rlcheck retrieval <slug>` | create a dated snapshot directory for tool results |

## Setting up a project

When this skill is loaded in a directory that is meant to be a research project,
run `rlcheck doctor` before anything else, and again whenever the user starts
work on a machine they have not used for this project. It lists every part of
the setup as `OK`, `FIX` (with the command that fixes it) or `NOTE`. Walk the
user through the `FIX` items one at a time, in the order printed, and run
`doctor` again at the end. Setup is finished when it prints `setup complete.`

The parts, and what you need from the user for each:

1. **Git repository.** If there is none, ask before running `git init`.
2. **Project id and store.** Ask for a short id (lower-case, hyphens) and where
   the shared store is on this computer — the synced OneDrive, SharePoint or
   network folder that holds the large files. Then
   `rlcheck init --id <id> --store "<path>"`. On a second machine the id is
   already in `research-log.ini`; only `rlcheck init --store "<path>"` is needed.
   If the folder already contains files but no store marker, `init` refuses;
   rerun with `--adopt` only after the user confirms it is the right folder.
3. **Access for Claude.** In Claude Code, run `rlcheck claude-settings` after
   the user agrees: it adds the store to Claude Code's allowed directories,
   protects `sources/` in the store from edits, and installs the session hook.
   Tell the user it takes effect in the next Claude Code session. In Claude.ai,
   ask the user to give the Filesystem connector access to both the project
   folder and the store.
4. **PROFILE.md.** Write it with the user, following
   `reference/project-profile.md`. Ask about one section at a time; do not
   invent source types or task types.
5. **The brief and the README.** Put the assignment verbatim into
   `methodology/00-brief.md` and write `README.md` from the template in
   `reference/documents.md`.

Each step changes the user's files or settings: say what the command will do
before running it. Where you cannot run commands, give them to the user as
described in *Running the checks*.

## The store

Large files — full-text PDFs, big exports, final binary exports — live outside
the repository in a shared store, because they do not belong in git and the
project is worked on from several machines. Everything else is text and lives in
the repository.

Records refer to store files as `store:<path>`, never by a machine's own path:
`store:sources/eu/regulation-2024.pdf`. Each machine maps the store to a local
folder in `research-log.local.ini`, which is not in git. To open a store file,
run `rlcheck where store:<path>` to get its location on this machine; where you
cannot run it, read the path from `research-log.local.ini`.

```
<store>/
  .research-store        marker naming the project; never edit
  inbox/                 new documents, not yet catalogued
  sources/               catalogued sources, frozen
  retrieved/             retrieval results too large for the repository (optional)
  exports/               final binary exports of the deliverable
```

**The inbox is outside the record.** Files arrive there from downloads, scripts
or the user. Nothing in `inbox/` may be a task input; `validate` fails if one
is. A file enters the record when a task catalogues it: the task moves it to
`sources/`, lists it among its outputs and records what was done with it.

**Store sources are frozen.** Git cannot protect them; the digests in task
records can. If a store source has to change, treat it like any frozen file:
log the change and run `rlcheck stale`.

**On a machine without the store**, store paths cannot be read. `validate` and
`stale` report them as not checked rather than failing, and `seal` keeps the
previous digest rather than writing a wrong one. Do not close a task whose
inputs could not be sealed.

## File classes

Every file in the project belongs to exactly one class. The class determines how
it may be changed. Getting this wrong is the main source of lost context.

| Class | Rule | Examples |
|---|---|---|
| **frozen** | Written once. Any change is an event that is logged and invalidates downstream work. | `methodology/00-brief.md`, retrieval snapshots, `store:sources/` |
| **living** | Rewritten in place to state what is true *now*. Git holds the history; the file does not. | `README.md`, `methodology/10-plan.md`, `methodology/30-limitations.md` |
| **append-only** | New entries are added at the end. Existing entries are never edited or deleted. | `methodology/20-decisions.md`, `methodology/40-insights.md` |
| **derived** | Regenerated from other files. Never hand-edited. | `methodology/25-decisions-in-force.md`, `methodology/90-deviations.md`, task outputs |

The class also decides what is in git. Living and append-only files must be,
because git is their history. Derived files are kept as text and are in git
too; only final binary exports go to `store:exports/`. Frozen files may be in
the store, because the digest in the record is what fixes their version.

Full layout, contents and templates: `reference/documents.md`.

## Layout

```
README.md                     living    router: what this project is, where things are, current state
PROFILE.md                    living    the project layer (source types, task types, delivery)
research-log.ini                        project id; shared through git
research-log.local.ini                  where the store is on this machine; not in git
methodology/
  00-brief.md                 frozen    the assignment, verbatim, plus agreed scope
  10-plan.md                  living    current plan and what comes next
  20-decisions.md             append    methodological decisions with rationale
  25-decisions-in-force.md    derived   the decisions not superseded, generated by rlcheck
  30-limitations.md           living    open register of gaps and caveats
  40-insights.md              append    observations captured for the final output
  90-deviations.md            derived   current state audited against 00-brief.md
tasks/
  t0001-<slug>/
    record.md                          the task record (schema in reference/task-records.md)
    <outputs>
sources/
  retrieved/                  frozen
    YYYY-MM-DD-<slug>/                 snapshot of one tool retrieval (reference/retrievals.md)
```

The store has its own layout, described under *The store*.

Numbers leave gaps of ten so documents can be inserted without renumbering.

## Nothing the result depends on lives only in the conversation

A task's result may depend only on files on disk. Two kinds of material reach
the work without being files, and both must be turned into files:

**Tool results.** Anything returned by web search, a database interface, an MCP
connector, an API or a page the user pasted, if it shapes the result, is saved
as a retrieval snapshot *at the moment it is retrieved*: `rlcheck retrieval
<slug>`, the raw results into the new directory, the manifest filled in with the
exact query. Databases change and search results cannot be reproduced; a
snapshot taken later is a different retrieval. Format and rules:
`reference/retrievals.md`.

**Your own background knowledge.** A claim that comes from what you know rather
than from a source on disk is not a finding. Either find and snapshot a source
for it, or mark it in the record as unverified background, so the researcher
can decide what to do with it.

## Opening a task

1. Read `PROFILE.md`, then `methodology/10-plan.md`.
2. Create `tasks/tNNNN-<slug>/record.md` from the template in
   `reference/task-records.md` with `status: planned`, the question it answers,
   and every input listed by path.
3. Run `rlcheck seal tasks/tNNNN-<slug>` to record the input digests.
4. Confirm the plan with the user before doing the work. Screening criteria,
   inclusion rules and search vocabulary are the user's decisions, not yours.
5. When the work starts, set `status: in-progress`, set `checkpoint:` to the
   current date-time, and write a first `## Handoff`: what is about to be done
   and what the first step is.

## While a task is open

The closing gate can only check what has been written down. Context is lost
during the work — to compaction, an interrupted session, a closed window —
not at the end of it. So everything is written at the moment it happens, and
the record is never more than one step behind the conversation.

**At the moment it happens:**

- A decision the user confirms goes into `methodology/20-decisions.md` at once,
  and its id into the record's `decisions:`; then run `rlcheck decisions`.
  Not at the end of the task.
- A gap, doubt or compromise goes into `methodology/30-limitations.md` at once,
  and its id into `limitations:`.
- A tool result that will be used becomes a snapshot at once (see above).
- An observation for the deliverable goes into `methodology/40-insights.md`
  at once.

**At every checkpoint**, rewrite `## Method as executed` and `## Handoff` to
state what is true now, and update `checkpoint:` to the current date-time.
Checkpoints are:

- after each substantive step: a search run, a batch screened, a source set
  extracted, a draft section written;
- before starting anything long: a large retrieval, a long batch of reading;
- whenever the user pauses, changes the subject or says they are stopping;
- whenever you notice the conversation has become long.

The test for a good checkpoint: if the conversation ended now, could a fresh
session continue from the record alone, without redoing anything and without
asking the user what was decided? If not, the record is behind.

Write outputs to the task directory as they are produced, not all at the end.
A half-screened table on disk is worth more than a fully screened one in the
conversation.

`rlcheck validate` holds an in-progress record to this: its `## Handoff` must
say where the work stands and it must have a valid `checkpoint:`. It cannot
tell whether the handoff is current; that part is yours.

## Closing a task

A task is not finished when the work is done. It is finished when the record is
complete. Before saying a task is done, all of these must be true:

- `record.md` has every required section filled. A section with nothing to
  report says `None.` and why; it is never empty and never left with template text.
- `status: complete` and a `closed:` date are set.
- Every declared output exists at the declared path.
- Every methodological decision made during the task has an entry in
  `methodology/20-decisions.md`, and its id is listed under `decisions:` in the
  record. A decision that replaces an earlier one names it under `**Supersedes.**`.
- Every gap, doubt or compromise has an entry in `methodology/30-limitations.md`,
  and its id is listed under `limitations:` in the record.
- Every retrieval the result depends on is a snapshot under `sources/retrieved/`,
  listed under both `inputs:` and `retrievals:`, and the record has been resealed.
- `rlcheck decisions` has been run if the decision log changed.
- `methodology/10-plan.md` has been rewritten to reflect the new state.
- `rlcheck check` exits clean.

`decisions:`, `limitations:` and `retrievals:` must be present in a complete
record even when there is nothing to list — write `[]`. An explicit empty list
is a statement; a missing key is an omission, and the script treats it as one.

If a check fails, fix it before reporting completion. Do not report a task as
done and list what is still missing.

## Resuming in a fresh conversation

A compaction is a resume. After the context has been compacted, or when a
session hook has just shown `rlcheck status` output, treat the conversation
summary as a pointer, not as the state: if a task is in progress, read its
`record.md` before doing anything else, and continue from its `## Handoff`.
Where the summary and the record disagree, the record wins; if the record looks
behind the summary, tell the user what seems to be missing rather than filling
it in from the summary.

Read in this order, and stop as soon as you have enough:

1. `README.md` and `PROFILE.md`
2. `methodology/10-plan.md`
3. `methodology/25-decisions-in-force.md` — the decisions that currently apply,
   however old. Read entries of `20-decisions.md` only when you need the context
   or alternatives behind one of them.
4. `methodology/30-limitations.md`
5. the `record.md` of the task named as next in the plan

Do **not** read the whole `tasks/` tree, the whole decision log, or any source
files that the plan does not point at. The read order exists to keep the fresh
session cheap; reading everything defeats the purpose.

Then run `rlcheck status` (or ask the user to, see *Running the checks*) and
report the state to the user before proposing anything. If `status` says the
decisions view is out of date, regenerate it before relying on it.

## Staleness

When a frozen input changes — the brief is revised, a source set is extended,
a primary document is corrected — every task downstream of it may need redoing.
This is a mechanical dependency question and must not be answered by reading and
guessing. Run `rlcheck stale`.

It compares recorded input digests against current ones and names the affected
records: `STALE` when an input changed, `MISSING` when it is gone. Then, for each
one: decide with the user whether to rerun it or accept
it, log that decision in `20-decisions.md`, and either rerun and reseal, or set
`status: superseded` and open a replacement task.

A retrieval is never refreshed in place. Rerunning a search creates a new
snapshot with a new date; the old one stays, because tasks that used it still
point at it.

## Never

- Never rewrite or tidy an entry in an append-only file. Add a new entry that
  corrects or supersedes the old one and says so.
- Never edit a derived file by hand. Regenerate it.
- Never change a frozen file silently. Log the change as an event in
  `20-decisions.md` and run the staleness check.
- Never leave a task record with placeholder text, and never leave a required
  section empty in a complete record. `None.` with a reason is honest; invented
  content is not.
- Never let a result rest on a tool response that was not snapshotted, or on
  your own knowledge presented as a finding.
- Never keep a decision, limitation or partial output only in the conversation
  until the end of a task. Write it when it happens.
- Never assess staleness, completeness or coverage by reading files when the
  script can answer it, and never report a check you have not seen run.
