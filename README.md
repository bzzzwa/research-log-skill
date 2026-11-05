# Social research generalization rules

Reusable rules for running social-science desk research with an LLM, so that the
conversation stops being the memory of the project.

The premise: the interpretive work — framing, search vocabulary, inclusion
judgements, synthesis — stays with the researcher. The bookkeeping does not.
If every phase leaves a complete written trace on disk, a fresh conversation
costs nothing and context is never silently lost to compaction.

The repository contains one skill, **research-log**, for Claude Code and
Claude.ai. It does not do research. It keeps the methodology documentation of a
research project complete and current, so that any phase can be resumed in a new
conversation, and so that the whole project can be audited afterwards.

## Contents

- `skills/research-log/` — the skill
  - `SKILL.md` — the instructions Claude follows
  - `CHANGELOG.md` — what changed in each version, and what a project has to do
    when it moves to that version
  - `reference/documents.md` — the methodology documents and their templates
  - `reference/task-records.md` — the task record format and its dependency schema
  - `reference/retrievals.md` — snapshots of search and tool results
  - `reference/project-profile.md` — how to write the per-project layer
  - `scripts/rlcheck.py` — setup, checks and derived views; Python standard
    library only

## Requirements

- Python 3.8 or newer on every computer the project is worked on.
- git, and a private remote repository for each research project.
- A shared folder for the large files (OneDrive, SharePoint, Dropbox or a
  network drive), synced or mounted on every computer.
- Claude Code, or Claude.ai with code execution enabled and a Filesystem
  connector that can reach the project folder and the shared folder.

## Design

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
them, and final binary exports live in a shared store outside the repository.
Records refer to them as `store:<path>` with a digest, so the record in git fixes
which version was used even though the file is not in git.

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
derived files up to date, living documents not older than the work they
describe.

**Auditable down to the tool.** Each finished task says who performed it — the
researcher, or which model in which environment — and whether the researcher
reviewed it. Instructions a model followed and scripts it ran are inputs like
any source.

**Bookkeeping, not management.** The model records, checks and proposes. It
does not schedule the work against deadlines, and its own ideas for new work
wait in the plan until the researcher makes them a task.

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
  exports/                     final binary exports
```

## Install the skill

**Claude Code.** Copy `skills/research-log/` into `~/.claude/skills/` (for all
your projects) or into a project's `.claude/skills/` (for that project only).
Start Claude Code in the research project's folder. Claude runs the checks
itself.

**Claude.ai.** Download `research-log-<version>.zip` from the latest release, or
zip the `research-log` folder yourself, and upload it under Settings → Skills.
Give the Filesystem connector access to the project folder and the store, and to
nothing else Claude does not need.

Claude.ai's code execution runs in a sandbox, not on your computer, so there
Claude cannot run the checks on your project. It gives you the exact commands to
run in PowerShell and asks you to paste the output, and it does not treat a step
as done until it has seen that output. It also never retypes the script: it
hands you `rlcheck.py` as a download with its SHA-256 and tells you how to
install it into the project.

## Set up a research project

Ask Claude to set up the project, naming the project folder and the store. It
runs `rlcheck doctor`, which lists every part of the setup as `OK`, `FIX` or
`NOTE`, and walks you through the fixes one at a time until `doctor` reports
`setup complete.` Along the way it asks you for a project id and writes
`PROFILE.md` with you, one section at a time. The client's original brief goes
into `store:sources/brief/`, and the first task records its transcription in
`methodology/00-brief.md`.

By hand, from the project folder, with the script from the skill:

```
python <skill-dir>/scripts/rlcheck.py doctor
python <skill-dir>/scripts/rlcheck.py init --id open-science-2026 --store "C:\Users\me\OneDrive - Org\Research\open-science-2026"
python tools/rlcheck.py claude-settings
python tools/rlcheck.py doctor
```

`<skill-dir>` is wherever `research-log/` is: `~/.claude/skills/research-log`,
a project's `.claude/skills/research-log`, `skills/research-log` in a clone of
this repository, or simply the downloaded `rlcheck.py`.

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

**On another computer**, clone the project and tell it where the store is:

```
python tools/rlcheck.py init --store "D:\Sync\Research\open-science-2026"
```

## Working on a project

**Starting a session.** Ask Claude to continue the project. It reads the
project's documents in a fixed order and starts from `rlcheck status`, which
lists open tasks with their last handoff, decisions awaiting your confirmation,
and today's date. In Claude Code the session hook shows `status` automatically.

**Tasks.** Every unit of work is a task with its own record. Claude opens the
record before the work and confirms the plan with you: screening criteria,
inclusion rules and search vocabulary are your decisions. During the work it
writes decisions, limitations and snapshots as they happen. It reports a task as
finished only after `rlcheck check` passes.

**Your part.** Claude marks its own proposals as provisional; you confirm or
correct them, and `status` keeps listing what is still unconfirmed. Ideas for
new work wait in the plan's *Proposed* section until you make them a task.
Commit after a clean `check`.

**New documents.** Put them into `inbox/` in the store. A cataloguing task moves
them into `sources/` and records what was done with them.

**When something changes.** If a source is added or corrected, or the brief is
revised, `rlcheck stale` names the tasks that depend on it. For each, you decide
whether to rerun it, accept its result as it stands, replace it, or extend it
with a task for the new sources only. The decision is logged and the record
keeps the trace.

## Commands

Throughout this README, `rlcheck <command>` means `python tools/rlcheck.py
<command>`, run in the project folder. The script always works on the current
folder and refuses to run outside a project.

| Command | What it does |
|---|---|
| `doctor` | checks the setup on this computer and says how to fix each gap |
| `init [--id ID] [--store PATH] [--adopt]` | creates or completes the setup |
| `init --update-tool` | replaces `tools/rlcheck.py` with the copy being run (see *Update*) |
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
problem.

## What is in git

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

## Update

The skill (the instructions) and a project's copy of the script (the checks) are
updated separately, on purpose.

**The skill.** Replace the whole `research-log` folder rather than copying files
over it, so that nothing renamed or removed is left behind. If the skill is
installed in more than one place — a project's `.claude/skills/`,
`~/.claude/skills/`, your Claude.ai account — update all of them, or Claude may
follow different instructions in different places. `SKILL.md` states its version
at the top. Start a new conversation afterwards: a running one keeps the version
it loaded.

**A project.** A newer skill does not change a project's `tools/rlcheck.py`.
When you want the project on the new version, ask Claude. It reads
`CHANGELOG.md` for every version in between, logs the update as a decision,
replaces the copy with `init --update-tool`, runs the checks and does what the
changelog lists for the project. In Claude.ai it gives you the new script as a
download and the commands to run.

## Pre-commit hook

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

## Session hook (Claude Code)

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
the result.

## Releases

Versions are numbered `YYYY.MM.N` and tagged `v<version>` in git. The version in
`SKILL.md`, in `scripts/rlcheck.py` and at the top of `CHANGELOG.md` must be the
same. Each GitHub release has release notes and a ready-to-upload
`research-log-<version>.zip` for Claude.ai.
