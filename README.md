# Research Log

A skill for Claude, and experimentally for OpenAI Codex, that keeps the
documentation of a desk-research project complete and current while you work
with an AI assistant. Every decision, source, search and step of the analysis
is written down as it happens. You can pick the project up in a new
conversation at any time, and anyone can later see how its results came about.

It is made for desk research in the social sciences that works with documents
and other text sources: policy analyses, document and literature reviews,
comparative studies. It does not do the research. It keeps the record.

## What it does for you

- **Pick up where you left off.** A new conversation, another computer, a
  context that was compacted in the middle of a task: the assistant reads the
  project's records and continues from the last handoff, not from memory.
- **A complete audit trail.** Every methodological decision with its reason and
  who made it. Every task with the exact sources it used, fixed by a digest.
  Every web or database search saved with its exact query and date. Who
  performed each step: you, or which model in which environment.
- **Awareness of change.** When a source is added or corrected, or the brief is
  revised, you are told which finished work depends on it, and you decide what
  to redo.
- **You stay in charge.** The assistant marks its own proposals as provisional
  until you confirm them, never adds sources to the corpus without you, and does
  not start new work you have not asked for.
- **Checked by a script, not by eye.** A small Python script, `rlcheck`, checks
  that the records are complete and consistent before any task counts as
  finished.

**Status.** An early version. It has been tested on several trial projects and
one complete research project, in Claude Code and Claude.ai on Windows and
Linux. Support for Codex follows the same open skill format but has not been
tested yet. Commands, file formats and rules may still change between versions;
`CHANGELOG.md` in the skill lists every change and what a project has to do
about it.

This is an independent project by TC Praha. It is written for Claude and works
with other assistants that read the same skill format, but it is not made,
endorsed or supported by Anthropic or OpenAI.

## Install

You need Python 3.8 or newer and git on every computer you work on, and a
shared folder for the project's large files: OneDrive, SharePoint, Dropbox or a
network drive, synced or mounted on every computer.

**Claude Code.** Copy the `skills/research-log/` folder into
`~/.claude/skills/` to use it in all your projects, or into a project's
`.claude/skills/` for that project only.

**Claude.ai.** Download `research-log-<version>.zip` from the latest release
and add it as a skill in Claude.ai's settings; code execution must be enabled.
Give the Filesystem connector access to the project folder and the shared
folder, and to nothing else the assistant does not need.

**Codex (experimental, not yet tested).** Copy the `skills/research-log/`
folder into a project's `.agents/skills/` or into `~/.agents/skills/`. Codex
needs the shared folder made writable; see [Codex](#codex) below.

## Start a project

Create an empty folder for the project, and a folder for its large files in
your shared storage. Then open the project folder in your assistant and ask,
for example:

> Set up a research project in this folder with the research-log skill. The
> folder for large files is `C:\Users\me\OneDrive - Org\Research\my-project`.

The assistant checks the setup with `rlcheck doctor` and walks you through it
one step at a time: a git repository, a short project id, the shared folder,
access for the assistant, and the project profile, which it writes with you one
section at a time (sources, task types, vocabulary, deliverable). Then you put
the client's brief into the shared folder, and the assistant records it as the
project's first task. Setup is finished when `doctor` reports
`setup complete.`

In Claude.ai the assistant cannot run anything on your computer. It gives you
the exact commands to run in PowerShell or a terminal and waits for you to
paste the output; it does not treat a step as done until it has seen it. The
first time, it hands you the script as a download with its checksum.

**On another computer**, clone the project and ask the assistant to set it up
there. It only needs to know where the shared folder is on that computer.

## Working on a project

**Starting a session.** Ask the assistant to continue the project. It reads the
project's documents in a fixed order and starts from `rlcheck status`, which
lists open tasks with the handoff of any task in progress, tasks whose inputs
have changed since they were sealed, decisions awaiting your confirmation, and
today's date. In Claude Code a session hook shows `status` automatically; in
Codex a line in `AGENTS.md` does the same.

**Tasks.** Every unit of work is a task with its own record. The assistant opens
the record before the work and confirms the plan with you: screening criteria,
inclusion rules and search vocabulary are your decisions. During the work it
writes down decisions, limitations and saved searches as they happen. It reports
a task as finished only after `rlcheck check` passes.

**Your part.** The assistant marks its own proposals as provisional; you confirm
or correct them, and `status` keeps listing what is still unconfirmed. Ideas for
new work wait in the plan's *Proposed* section until you make them a task.
Commit after a clean `check`.

**New documents.** Put them into `inbox/` in the shared folder. A cataloguing
task takes them in: the assistant prepares one command that moves them into
`sources/` under their catalogued names, you run it, and the assistant checks
that each file arrived unchanged. Nothing enters the frozen corpus without a
step taken by you.

**When something changes.** If a source is added or corrected, or the brief is
revised, the tasks that depend on it become stale. Nothing is redone
automatically: `rlcheck status` reports them at the start of the next session,
and `rlcheck check` before any task is closed or anything committed. For each,
you decide whether to rerun it, accept its result as it stands, replace it, or
extend it with a task for the new sources only. The decision is logged and the
record keeps the trace.

**Charts and other generated files.** When a task produces a script, for
example R code that draws an infographic, the script is kept in git and the
files it generates go to `exports/` in the shared folder, so they are ready on
every computer. If the data behind them change, the task is reported as stale
like any other; when you decide to rerun it, the assistant generates the files
again.

## What a project looks like

```
<project>/                     a private git repository
  README.md, PROFILE.md        router and project layer
  research-log.ini             the project id
  research-log.local.ini       this computer's paths (not in git)
  methodology/                 brief, plan, decisions, limitations, insights
  tasks/tNNNN-<slug>/          one record per unit of work, with its text outputs
  sources/retrieved/           snapshots of searches and tool results
  tools/rlcheck.py             the project's own copy of the checks

<store>/                       the shared folder, outside git
  inbox/                       new documents, not yet catalogued
  sources/                     catalogued sources, frozen
    brief/                     the client's original assignment
  work/                        large intermediates, one folder per task
  exports/                     files for use outside the project, one folder per task
```

In the records, files in the shared folder are written as `store:<path>`, so the
same record is valid on every computer.

## How it works

**Two layers.** The skill holds what is true of every project. `PROFILE.md` in
each research project holds what is true of that one: source types, task types,
vocabulary, deliverable. Nothing project-specific ever enters the skill.

**Four file classes.** Every file is frozen, living, append-only or derived, and
the class determines how it may be changed. Most context loss comes from
treating a living document as a historical record, or the reverse.

**The record in git, the large files in a store.** The class also decides what
is versioned. Living and append-only documents must be in git, because git is
their history, and derived work is kept as text and is in git too. Large
sources such as 200-page PDFs, large intermediates such as text extracted from
them, and files generated for use outside the project, such as charts drawn by
a script, live in a shared store outside the repository. Records refer to them
as `store:<path>` with a digest, so the record in git fixes which version was
used even though the file is not in git.

**Staleness is a build problem, not a prompt problem.** Task records declare
their inputs with digests. When a source set grows or the brief is amended,
`rlcheck stale` names the affected records; the model is never asked to work
this out by reading. A finished record cannot be quietly resealed against new
inputs: the change needs a logged decision and stays visible in the record.

**Nothing lives only in the conversation.** Results from web search, databases
and connectors are saved as dated, frozen snapshots with the exact query at the
moment they are retrieved, and declared as task inputs. A search that cannot be
rerun can still be checked.

**Write when it happens, not when the task closes.** Context is lost during the
work, before any closing check runs. Decisions, limitations and outputs are
written as they occur, and an open task's record is brought up to date at every
checkpoint. After a compaction the record, not the conversation summary, is the
state.

**The log is append-only; the current view is derived.** Decisions are never
edited, only superseded or confirmed by later ones. `rlcheck decisions` derives
the set still in force, so a new session reads the rules that apply now without
reading the whole history.

**The gate is mechanical.** A task is finished when its record passes
`rlcheck check`, not when the work feels done. The check looks at substance as
well as form: no empty sections or template text in a finished record, every
output present, every cited decision, limitation and snapshot resolvable,
derived files up to date. It also warns when the plan or the README look older
than the work they describe.

**Auditable down to the tool.** Each finished task says who performed it — the
researcher, or which model in which environment — and whether the researcher
reviewed it. Instructions a model followed and scripts it ran are inputs like
any source, and rules for a judgement, such as a coding frame or a scale, are
written down before they are applied.

**Bookkeeping, not management.** The model records, checks and proposes. It
does not schedule the work against deadlines, and its own ideas for new work
wait in the plan until the researcher makes them a task.

## Reference

### Commands

Throughout this README, `rlcheck <command>` means `python tools/rlcheck.py
<command>`, run in the project folder. The script works on the current folder.
`doctor`, `init` and `version` run anywhere; every other command refuses to run
outside a project, so a run in the wrong place cannot report a clean result.

| Command | What it does |
|---|---|
| `doctor` | checks the setup on this computer and says how to fix each gap |
| `init [--id ID] [--store PATH] [--adopt]` | creates or completes the setup |
| `init --update-tool` | run from a newer copy (the skill's script or a download): replaces `tools/rlcheck.py` with that copy; see *Updating* |
| `init --fix-line-endings` | converts text files checked out with CRLF to LF |
| `claude-settings` | Claude Code access to the store and the session hook |
| `version` | the version of this copy |
| `status` | the state of the project, for the start of a session |
| `validate` | are records, logs and snapshots complete and consistent? |
| `stale` | which records depend on inputs that have changed? |
| `check` | `validate` and `stale` together |
| `seal tasks/<task>` | records the current digests of a task's inputs |
| `seal tasks/<task> --rerun D012` or `--accept D012` | the same for a finished task, after a logged decision |
| `decisions` | regenerates `methodology/25-decisions-in-force.md` |
| `retrieval <slug>` | creates a dated folder for a search snapshot |
| `where store:<path>` | where a store file is on this computer |

`doctor`, `validate`, `stale` and `check` exit non-zero when they find a
problem; warnings alone do not make them fail.

### Setting up by hand

In the project folder:

```
git init
python <rlcheck> doctor
python <rlcheck> init --id open-science-2026 --store "C:\Users\me\OneDrive - Org\Research\open-science-2026"
python tools/rlcheck.py claude-settings      # Claude Code only
python tools/rlcheck.py doctor
```

`<rlcheck>` is the skill's script, used only until the project has its own
copy: `<skill-dir>/scripts/rlcheck.py`, where `<skill-dir>` is
`~/.claude/skills/research-log`, a project's `.claude/skills/research-log`,
`~/.agents/skills/research-log`, or `skills/research-log` in a clone of this
repository; or a downloaded `rlcheck.py`. From `init` on, every command runs
the project's copy, `tools/rlcheck.py`. The last `doctor` keeps reporting
`PROFILE.md` as missing until you have written it with the assistant.

`init` creates the methodology skeleton, `research-log.ini`, the `.gitignore`
and `.gitattributes` entries, the project's copy of the script in
`tools/rlcheck.py`, the store's folders and its marker file, and
`research-log.local.ini` with this computer's paths. It refuses a store folder
that belongs to another project, and a non-empty folder without a marker unless
given `--adopt`.

`claude-settings` is for Claude Code only. It writes
`.claude/settings.local.json` on this computer: the store as an additional
directory, rules against editing `sources/` in the store, and the session hook
described below. Check it in the next Claude Code session with `/permissions`
and `/hooks`. The rules guard against accidental edits but do not cover shell
commands; the digests in the records are what detect a changed source.

On another computer, after cloning the project:

```
python tools/rlcheck.py init --store "D:\Sync\Research\open-science-2026"
python tools/rlcheck.py claude-settings      # Claude Code only
python tools/rlcheck.py doctor
```

### Codex

Codex reads the same skill format and runs the checks itself, like Claude Code,
with three differences. Support is experimental and not yet tested.

- By default Codex writes only inside the project. Make the store writable by
  starting Codex with `--add-dir "<store path>"`, or permanently in
  `~/.codex/config.toml`:

  ```toml
  [sandbox_workspace_write]
  writable_roots = ["C:\\Users\\me\\OneDrive - Org\\Research\\open-science-2026"]
  ```

- Codex keeps `.git` read-only, so it asks you to approve each commit.
- Codex has no session hook. Instead, the project's `AGENTS.md`, which Codex
  reads at the start of every session, says to begin with `rlcheck status`.
  Codex adds the line during setup with your agreement; `doctor` checks it.

The `agents/openai.yaml` file in the skill sets the name Codex shows and lets
it use the skill whenever a task matches, without being named.

### What is in git

Research project repositories are private. Task records, the decision log and
the extractions quote and summarise the sources and record internal decisions
about the client's assignment; none of that is meant to be public, even when the
sources themselves are.

Everything in a project's repository is committed except three files that
differ on every computer, which `init` adds to `.gitignore`:

| File | Why it stays local |
|---|---|
| `research-log.local.ini` | where the store, Python and `rlcheck.py` are on this computer |
| `.rlcheck-cache.json` | cached digests, so cloud-synced files are not read again on every check |
| `.claude/settings.local.json` | Claude Code access and hook, with this computer's paths |

Two files are committed on purpose:

| File | Why it is in git |
|---|---|
| `tools/rlcheck.py` | the project keeps the version of the checks its records were validated with; changing it is a logged decision |
| `.gitattributes` | `* text=auto eol=lf` keeps text files identical on every computer |

The store is outside the repository. Its backup and version history come from
the shared folder it lives in, not from git.

### Updating

The skill (the instructions) and a project's copy of the script (the checks) are
updated separately, on purpose.

**The skill.** Replace the whole `research-log` folder rather than copying files
over it, so that nothing renamed or removed is left behind. If the skill is
installed in more than one place — a project's `.claude/skills/` or
`.agents/skills/`, your home folder, your Claude.ai account — update all of
them, or the assistant may follow different instructions in different places.
`SKILL.md` states its version at the top. Start a new conversation afterwards: a
running one keeps the version it loaded.

**A project.** A newer skill does not change a project's `tools/rlcheck.py`.
When you want the project on the new version, ask the assistant. It reads
`CHANGELOG.md` for every version in between, logs the update as a decision,
runs `init --update-tool` from the newer copy of the script, runs the checks and
does what the changelog lists for the project. In Claude.ai it gives you the
new script as a download and the commands to run it from there.

### Pre-commit hook

To refuse commits while the project does not pass its checks, create
`.git/hooks/pre-commit` in the project:

```sh
#!/bin/sh
python tools/rlcheck.py check
```

A commit is then refused while a record is incomplete or stale, a snapshot is
undocumented or the decisions view is out of date. On a computer without the
store, store inputs are skipped, so the hook does not block commits there. If
git's shell does not find `python` (common with Conda on Windows), use the full
path to Python recorded under `[tools]` in `research-log.local.ini`. On macOS
and Linux, make the file executable with `chmod +x`.

### Session hook (Claude Code)

A `SessionStart` hook puts `rlcheck status` in front of Claude whenever a session
starts, resumes, is cleared or has just been compacted. For a task in progress,
`status` prints its checkpoint and handoff with an instruction to read the
record before continuing. `rlcheck claude-settings` installs the hook with this
computer's paths. Written by hand, it looks like this:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd \"$CLAUDE_PROJECT_DIR\" && python tools/rlcheck.py status"
          }
        ]
      }
    ]
  }
}
```

The hook can only bring back what is already on disk. There is deliberately no
`PreCompact` hook: it runs before compaction but cannot make Claude write
anything, and its output reaches only the user. Keeping the record current is
the job of the checkpoint rules in `SKILL.md`; the hook makes sure Claude reads
the result. In Codex, which has no such hook, the line in `AGENTS.md` serves the
same purpose.

## Repository contents

- `LICENSE`, `NOTICE` — Apache License 2.0 and the copyright notice
- `CITATION.cff` — how to cite the skill
- `skills/research-log/` — the skill
  - `SKILL.md` — the instructions the assistant follows
  - `LICENSE.txt` — the licence, so that every copy of the skill carries it
  - `CHANGELOG.md` — what changed in each version, and what a project has to do
    when it moves to that version
  - `agents/openai.yaml` — display name and invocation policy for Codex
  - `reference/documents.md` — the methodology documents and their templates
  - `reference/task-records.md` — the task record format and its dependency schema
  - `reference/retrievals.md` — snapshots of search and tool results
  - `reference/project-profile.md` — how to write the per-project layer
  - `scripts/rlcheck.py` — setup, checks and derived views; Python standard
    library only

## Releases

Versions are numbered `YYYY.MM.N` and tagged `v<version>` in git. Changes not
yet released are collected under *Unreleased* at the top of `CHANGELOG.md`;
the version number changes only when they are released. At a release, the
*Unreleased* heading becomes the new version, and the version in `SKILL.md`, in
`scripts/rlcheck.py` and in that heading must be the same. Do not install an
unreleased working copy of the skill into projects: `doctor` compares version
numbers, so it could not tell that the code differs. Each GitHub release has
release notes and a ready-to-upload `research-log-<version>.zip` for Claude.ai.

## License and citation

Copyright 2026 TC Praha. Licensed under the Apache License, Version 2.0; see
`LICENSE` and `NOTICE`. You may use, change and share the skill, also in
commercial work, as long as you keep the licence and copyright notices and say
what you changed.

If the skill contributes to published research, please cite it: GitHub shows
the citation from `CITATION.cff` under *Cite this repository*.
