---
name: research-log
description: Keep the methodology log and task records of a social-science desk-research project complete enough that any phase can be resumed in a fresh conversation with no loss of context. Use whenever working inside a research project directory that contains PROFILE.md or a methodology/ folder; when opening, closing or resuming a research task; when asked to record a methodological decision, log a limitation or caveat, update the plan, capture an observation for the final output, save or snapshot search results from a database, website or tool, check deviations from the brief, check whether outputs have gone stale, or set up a new research project directory or an existing project on another computer. Also use when the user says they are starting a new session, continuing earlier work, or asks what state the project is in, and after the context has been compacted while a research task is open.
---

# Research Log

**Version.** 2026.11.5 — the same number as `__version__` in
`scripts/rlcheck.py`. If this skill is available to you more than once with
different versions (for example in the project and in the user's account), tell
the user which version you are following.

Desk research in the social sciences cannot be handed to an agent end to end. The
searching is theory-laden, inclusion is a judgement call, and synthesis is the
researcher's work. What *can* be systematised is the bookkeeping: if every phase
leaves a complete written trace, the conversation itself stops being the memory,
and a fresh session costs nothing.

That is the whole purpose of this skill. It does not do research. It makes the
project resumable.

It is not project management either. Dates and deadlines in the brief or the
plan are context. Do not count the days to a deadline, schedule or pace the
work around one, or advise the researcher to speed up or slow down, unless the
researcher asks for it or `PROFILE.md` says so.

## Two layers

This skill is the general layer: file classes, record format, closing gate. It
is the same for every project.

`PROFILE.md` in the project root is the project layer: what the source types
are, how they are processed, what counts as a task, what the delivery format is.
It differs for every project. **Always read `PROFILE.md` before acting.** If it
is missing, the project is not set up yet: see *Setting up a project*.

Never put project-specific rules in this skill, and never put general rules in
`PROFILE.md`.

## Where you may look

Read, list and search only in three places: the project directory, the store
the user named, and this skill's own directory. Do not look anywhere else on
the user's computer — not parent folders, not sibling projects, not another
project's configuration — even when a connector would let you, and even to save
the user a question. A value taken from another project (a Python path, a store
location) may belong to a different machine or setup and be wrong here. If you
need something that is not in these three places, ask the user for it.

## Running the checks

Completeness, staleness and the current set of decisions are answered by
`scripts/rlcheck.py`, never by reading and judging. Below, `rlcheck <command>`
means running that script **on the user's computer, with the project root as
the working directory**. The script works on the current directory, so it does
not matter where it is installed. Run anywhere else, it refuses with "not a
research-log project".

First decide where your shell is.

**Claude Code, or any shell that runs on the user's computer in the project**
(the project files are in your working directory): run
`python tools/rlcheck.py <command>` yourself — the project's own copy — and act
on the output. Before `init` has created that copy, use this skill's
`scripts/rlcheck.py`.

**Claude.ai, or any environment where your shell is a sandbox.** Claude.ai's
code execution runs on a separate machine, not the user's. Working through a
Filesystem connector, you can read and write the user's files but you cannot
execute anything on their computer. **Never run rlcheck in your sandbox**: it
would check an empty folder, and its output says nothing about the project.
Instead, give the user the command, ask them to run it and paste the output,
and wait. Until the output is in the conversation, the step has not happened.
Report what you wrote, not the state of the project: say that setup is
finished, a check passed or a task is closed only after the user has pasted
output that shows it.

To give the user a command that works on their computer, read
`research-log.local.ini` in the project root through the connector. Its
`[tools]` section records where Python and `rlcheck.py` are on that machine.
Give both lines, with the paths filled in, in the form for the user's shell:

```
# PowerShell (Windows default)
Set-Location "<project root>"
& "<tools.python>" "<tools.rlcheck>" <command>

# cmd.exe
cd /d "<project root>"
"<tools.python>" "<tools.rlcheck>" <command>

# macOS / Linux
cd "<project root>"
"<tools.python>" "<tools.rlcheck>" <command>
```

In PowerShell the `&` is required: without it a quoted path is printed, not run.
If the paths in `[tools]` are Windows paths, assume PowerShell unless the user
says otherwise.

If there is no `research-log.local.ini`, or it has no `[tools]` section, this
machine has not been set up yet. Do not search the disk for Python or for
another copy of the script. Ask the user which Python to use, or give the
command with `python` and say to replace it with the full path to `python.exe`
if it is not found.

**Getting the script onto the user's computer.** The project needs its own
copy in `tools/rlcheck.py`. In Claude.ai, never retype the script through the
connector: it is long, and one wrong character would surface only later, as a
wrong check. Hand it over as a file:

1. Present this skill's `scripts/rlcheck.py` to the user for download, and
   compute its SHA-256 in your sandbox.
2. Tell the user to leave the downloaded file where the browser put it
   (usually Downloads): not in the project root, not in `tools/`.
3. Give the commands, with the project root as the working directory:

   ```
   Set-Location "<project root>"
   Get-FileHash "$HOME\Downloads\rlcheck.py"     # must be <SHA-256>; if not, stop
   & "<python>" "$HOME\Downloads\rlcheck.py" init <options>
   ```

   For a first setup the options are `--id <id> --store "<path>"` (on a second
   machine only `--store "<path>"`); to update the project's copy, `--update-tool`.
   If the browser renamed the file (`rlcheck (1).py`), use that name.

`init` copies the script it was run from into `tools/rlcheck.py` and records
its location; from then on every command uses `tools/rlcheck.py`, and the
downloaded file can be deleted. In Claude Code, run `init` from this skill's
`scripts/rlcheck.py` directly.

Never say a check passed unless you have seen its output in this session.

**The project's version of rlcheck.** `tools/rlcheck.py` is the version the
project's records are checked with; `rlcheck version`, `doctor` and `status`
print it. Compare it with `__version__` in this skill's `scripts/rlcheck.py`.
If the skill's is newer, tell the user and offer the update, but do not make
it unasked: a new version can change what the project is held to and how
digests are computed. Updating is a decision. Log it in `20-decisions.md`,
replace the file with `rlcheck init --update-tool` run from the newer copy (in
Claude.ai, handed over for download as described above), then run
`rlcheck check` and reseal what `stale` reports.

| Command | What it answers |
|---|---|
| `rlcheck doctor` | is this project set up on this machine, and what to fix if not |
| `rlcheck init ...` | create or complete the setup (see *Setting up a project*) |
| `rlcheck version` | which version of rlcheck this copy is |
| `rlcheck claude-settings` | give Claude Code access to the store and install the session hook |
| `rlcheck where store:<path>` | where a store path is on this machine |
| `rlcheck status` | state of the project, for the start of a session |
| `rlcheck validate` | are records, logs and snapshots complete and consistent? |
| `rlcheck stale` | which records depend on inputs that have changed? |
| `rlcheck check` | `validate` and `stale` together; what a pre-commit hook runs |
| `rlcheck seal tasks/tNNNN-<slug>` | record the current digests of a task's inputs |
| `rlcheck decisions` | regenerate `methodology/25-decisions-in-force.md` |
| `rlcheck retrieval <slug>` | create a dated snapshot directory for tool results |

## When to run what

| When | Run |
|---|---|
| a session starts or resumes, or the context was compacted | `status` (on a machine new to the project: `doctor`) |
| setting up a project, or an existing one on another machine | `doctor`, then what it says: `init`, `claude-settings` |
| a task's inputs are listed, or change while it is open | `seal tasks/tNNNN-<slug>` |
| a tool returns results the work will use | `retrieval <slug>`, then save the results into it |
| an entry was added to `20-decisions.md` | `decisions` |
| before saying a task is closed | `check` |
| before a commit, before a delivery | `check` |
| a source, a snapshot or the brief changed | `stale`; then, per record, after a logged decision: `seal ... --rerun D0NN` or `seal ... --accept D0NN` |
| you need the location of a store file | `where store:<path>` |
| you are about to write a date and have not seen today's in this session | `status` |

In Claude.ai, give the user the commands of one step together, so that a single
run and paste covers them.

**Dates.** Every date you write — `opened`, `closed`, `checkpoint`, decision
headers, `**Updated.**` — is taken from the `today:` line of the latest
`rlcheck` output, never from earlier in the conversation. A conversation can
run past midnight or be continued days later; the date you remember is then
wrong. `validate` warns about dates after today and fails on a task closed
before it was opened.

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
   `init` also copies rlcheck into `tools/rlcheck.py`, adds `.gitattributes` so
   that text files keep the same line endings on every machine, and records
   where Python and the script are on this machine, which is how you can later
   give the user exact commands in Claude.ai.
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
   invent source types or task types. What you propose yourself is handled as
   described in *Decisions are logged wherever they are made*.
5. **The brief.** Ask the user to put the client's original documents into
   `store:sources/brief/`, with the date in the file name, and never move them
   afterwards. Open the first task, `t0001-brief`, with those files as inputs
   and `methodology/00-brief.md` as its output. Transcribe the assignment under
   *As received*, naming each original by its store path: formatting it as
   Markdown is fine, rewording it is not. Leave *Agreed scope* empty until the
   user or the client states it. Because the originals are inputs of a sealed
   task, `stale` reports it when the client sends a revised version.
6. **The README.** Write it from the template in `reference/documents.md`.

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
    brief/               the client's original assignment and its revisions
  work/                  large intermediates of tasks, one folder per task
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

**Large intermediates go to `store:work/<task id>/`.** Text extracted from long
PDFs, documents split into parts for repeated reading, converted formats: when
an analysis step produces something too large for git, it goes there, declared
as an output of the task that made it and as an input of the tasks that use it.
Everything a task produces that is small enough stays as text in the task's
directory. Only final binary exports go to `store:exports/`.

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
research-log.local.ini                  this machine's store and tool paths; not in git
.gitattributes                          keeps text files in LF on every machine
tools/
  rlcheck.py                            the project's copy of the checks, versioned with it
  <other scripts>                       scripts the analysis uses (extraction, conversion, coding)
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

## Decisions are logged wherever they are made

Decisions are not only made inside tasks. Setting up the project, revising
`PROFILE.md`, reordering the plan and agreeing scope with the client are
methodological decisions too, and the decision log is the only place their
reasons survive: git keeps what changed, not why.

- A change to `PROFILE.md`, to the phases or their order in `10-plan.md`, or to
  *Agreed scope* or *Amendments* in `00-brief.md` that changes how the research
  is done gets an entry in `20-decisions.md` at once, then `rlcheck decisions`.
  Updating *Now* and *Next* in the plan to reflect progress is not a decision.
- The choices made during setup — task types, conventions, what is in scope —
  are logged as they are confirmed, not after setup is finished.
- `**Decided by.**` says who decided: the researcher, the client, or "proposed
  by Claude, confirmed by the researcher". A choice you made alone, or one the
  user has not yet confirmed, contains the word "provisional".
- When the user confirms a provisional decision, add a new entry with
  `**Confirms.** D00N`. Do not edit the old entry and do not supersede it: the
  decision has not changed, it has been confirmed, and the in-force view marks
  it so. Supersede only when the decision itself changes. `rlcheck status`
  lists provisional decisions still awaiting confirmation; raise them with the
  user when you resume.
- An entry is final once it is committed. `rlcheck validate` compares the
  decision log and the insights log with the last commit and fails if a
  committed entry was changed. Before the commit you may still fix your own
  draft.
- A revised brief from the client goes into `store:sources/brief/` next to the
  original, under a new date. Open a new brief task for it, add it under
  *Amendments*, and log what it changes.

When you propose content yourself — task types, conventions, definitions, a
scope — say which items are your proposal and which come from the user or the
brief, and have the proposals confirmed one by one, not as a block. Never put
into *Agreed scope* anything the user or the client has not stated. Content that
comes from your own background knowledge, such as a definition of a term or an
assumed list of languages, is marked as such where it is written, or left out.

## What the work was done with

An audit of AI-assisted research has to be able to say not only what was done
but by what, and following which instructions.

- Every complete record says who performed the work in `performed-by:`: the
  researcher, or the model with its name and version as you know them and the
  environment (Claude Code, Claude.ai), and whether the researcher reviewed the
  result. `validate` fails on a complete record without it.
- When a model performs an analytic step from written instructions — a prompt,
  a coding frame, an extraction template, a list of questions for each document
  — those instructions are a file in the task directory or in `tools/`, and an
  input of the task. If the instructions change, `stale` then shows which
  results were produced with the old ones.
- Scripts the analysis uses live in `tools/` and are inputs of the tasks that
  run them, for the same reason.

## Proposals and the edges of a task

Your own ideas for new outputs, comparisons or angles are welcome and often
useful. They are written down, not acted on:

- A proposal for new work goes into the *Proposed* section of `10-plan.md`,
  with one line on why. Nothing in *Proposed* is worked on until the researcher
  turns it into a task.
- An observation about the subject goes into `40-insights.md` as before.

A task works only with its declared inputs. Work done elsewhere — by a
colleague, in another project, in an earlier version of a shared document —
enters the project only as a new frozen input with a date. When two inputs use
different category systems, or come from different stages of someone else's
work, do not harmonise them silently or code them together. Name the mismatch
as a limitation, and ask the researcher how to treat it.

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
- `status: complete` and a `closed:` date are set, and `performed-by:` says who
  did the work.
- Every declared output exists at the declared path.
- Every methodological decision made during the task has an entry in
  `methodology/20-decisions.md`, and its id is listed under `decisions:` in the
  record. A decision that replaces an earlier one names it under `**Supersedes.**`.
- Every gap, doubt or compromise has an entry in `methodology/30-limitations.md`,
  and its id is listed under `limitations:` in the record.
- Every retrieval the result depends on is a snapshot under `sources/retrieved/`,
  listed under both `inputs:` and `retrievals:`, and the record has been resealed.
- `rlcheck decisions` has been run if the decision log changed.
- `methodology/10-plan.md` has been rewritten to reflect the new state, with
  today's date in `**Updated.**`, and the *State* in `README.md` is still true.
  `validate` warns when the plan is older than the last closed task or decision,
  when *Next* names a finished task, or when the README is older than the plan.
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
one, decide with the user, log the decision in `20-decisions.md`, and do one of:

- **Rerun** the task with the new inputs, update its record, and run
  `rlcheck seal tasks/tNNNN-<slug> --rerun D0NN`.
- **Accept** the old result for the new inputs (the added source changes
  nothing, the correction is immaterial) and run
  `rlcheck seal tasks/tNNNN-<slug> --accept D0NN`.
- **Supersede** it: set `status: superseded` and open a replacement task.
- **Extend** it: when sources were only added, open a new task that does the
  same work for the new sources alone, with the earlier task's outputs among its
  inputs, and accept the earlier task for the extended set.

For a finished record, `seal` refuses to change a digest without `--rerun` or
`--accept`, and records every such change under `resealed:` in the record:
which input, old and new digest, the decision and the date. The record thus
never claims that a result was made from inputs it did not see.

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
- Never look outside the project directory, the store the user named and this
  skill's directory, and never reuse values from another project.
- Never present your own proposal or background knowledge as something the user
  or the client decided.
- Never start work on your own proposal before the researcher has made it a
  task, and never merge inputs that use different categories without asking.
- Never take a date from memory; take it from the latest `rlcheck` output.
- Never assess staleness, completeness or coverage by reading files when the
  script can answer it, and never report a check you have not seen run.
