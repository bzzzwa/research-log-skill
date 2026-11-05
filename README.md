# Social research generalization rules

Reusable rules for running social-science desk research with an LLM, so that the
conversation stops being the memory of the project.

The premise: the interpretive work — framing, search vocabulary, inclusion
judgements, synthesis — stays with the researcher. The bookkeeping does not.
If every phase leaves a complete written trace on disk, a fresh conversation
costs nothing and context is never silently lost to compaction.

## Contents

- `skills/research-log/` — the general skill: file classes, document set,
  task-record schema, closing gate, staleness handling, project setup.
  - `SKILL.md` — the skill itself
  - `reference/documents.md` — the methodology documents and their templates
  - `reference/task-records.md` — task record format and the dependency schema
  - `reference/retrievals.md` — snapshots of search and tool results
  - `reference/project-profile.md` — how to write the per-project layer
  - `scripts/rlcheck.py` — setup, validation, staleness and derived views, zero dependencies

## Design

**Two layers.** The skill holds what is true of every project. `PROFILE.md` in
each research project holds what is true of that one: source types, task types,
vocabulary, deliverable. Nothing project-specific ever enters the skill.

**Four file classes.** Every file is frozen, living, append-only or derived, and
the class determines how it may be changed. Most context loss comes from
treating a living document as a historical record, or the reverse.

**The record in git, the large files in a store.** The class also decides what
is versioned. Living and append-only documents must be in git, because git is
their history; derived work is kept as text and is in git too. Large frozen
sources — 200-page PDFs, big exports — and final binary exports live in a shared
store outside the repository. Records refer to them as `store:<path>` with a
digest, so the record in git fixes which version was used even though the file
is not in git. Each machine says where the store is in an uncommitted local
config.

**Staleness is a build problem, not a prompt problem.** Task records declare
their inputs with digests. When a source set grows or the brief is amended,
`rlcheck.py stale` names the affected records. The model is never asked to work
this out by reading. On a machine without the store, store inputs are reported
as not checked, not as changed.

**Nothing lives only in the conversation.** Results from web search, databases
and connectors are saved as dated, frozen snapshots with the exact query, at the
moment they are retrieved, and declared as task inputs. A search that cannot be
rerun can still be checked.

**Write when it happens, not when the task closes.** Context is lost during the
work, before any closing gate runs. Decisions, limitations and outputs are
written as they occur, and an open task's record is brought up to date at every
checkpoint, so the record is never more than one step behind the conversation.
After a compaction the record, not the conversation summary, is the state.

**The log is append-only; the current view is derived.** Decisions are never
edited, only superseded by later ones. `rlcheck.py decisions` derives the set
still in force, so a fresh session reads the rules that apply now without
reading the whole history.

**The gate is mechanical.** A task is finished when its record validates, not
when the work feels done. `rlcheck.py validate` checks substance as well as
form: no empty sections or template text in a complete record, every output
present, every cited decision, limitation and snapshot resolvable, derived files
up to date. It exits non-zero on any failure and can run as a pre-commit hook.

**Setup is guided.** `rlcheck.py doctor` checks every part of the setup on the
current machine and prints the command that fixes each gap. The skill tells the
model to run it first and walk the user through it, so a new project, or an
existing one on a new computer, is set up in the conversation.

## Install the skill

**Claude Code (intended).** Copy `skills/research-log/` into `~/.claude/skills/`
or into the project's `.claude/skills/`. Start Claude Code in the research
project's root; the model runs the checks itself.

**Claude.ai.** Zip the `research-log` folder and upload it under
Settings → Skills (requires code execution enabled). Give the Filesystem
connector access to the project folder and to the store, and nothing else the
model does not need: the skill tells it to stay within the project, the store
and the skill. Claude.ai's code execution runs in a sandbox, not on your
computer, so the model cannot run `rlcheck` against the project; it gives you
the exact command instead and asks you to paste the output. On first setup it
writes the script into the project's `tools/`; after that it takes the paths
from `research-log.local.ini`, where `init` records them. `rlcheck` refuses to
run outside a project folder, so a stray run in the sandbox cannot report a
false clean result.

## Set up a research project

Ask Claude to set the project up; it runs `doctor` and guides you. By hand, from
the research project's root:

```
python <skill-dir>/scripts/rlcheck.py doctor
python <skill-dir>/scripts/rlcheck.py init --id open-science-2026 --store "C:\Users\me\OneDrive - Org\Research\open-science-2026"
python <skill-dir>/scripts/rlcheck.py claude-settings
```

`init` writes `research-log.ini` (the project id, in git), the methodology
skeleton, `.gitignore` and `.gitattributes` entries, a copy of the script in
`tools/rlcheck.py`, the store layout and its marker, and
`research-log.local.ini` (this machine's store path and the location of Python
and `rlcheck.py`, not in git). On another computer, after cloning, only the
store path is needed:

```
python <skill-dir>/scripts/rlcheck.py init --store "D:\Sync\Research\open-science-2026"
```

`init` checks the marker in the store, so it refuses a folder that belongs to a
different project, and refuses a non-empty folder without a marker unless given
`--adopt`.

`claude-settings` writes `.claude/settings.local.json` for Claude Code on this
machine: the store as an additional directory, deny rules against editing
`sources/` in the store, and the session hook described below. Check it in the
next Claude Code session with `/permissions` and `/hooks`. The deny rules are a
guard against accidental edits, not a guarantee — they do not cover shell
commands. The digests in the records are what detects a changed source.

`PROFILE.md`, the brief and the README are written with Claude, following
`reference/project-profile.md` and `reference/documents.md`.

## Commands

Always run from the research project's root; the script works on the current
directory, wherever it is installed.

```
python <skill-dir>/scripts/rlcheck.py doctor
python <skill-dir>/scripts/rlcheck.py init [--id ID] [--store PATH] [--adopt]
python <skill-dir>/scripts/rlcheck.py claude-settings
python <skill-dir>/scripts/rlcheck.py where store:sources/eu/regulation-2024.pdf
python <skill-dir>/scripts/rlcheck.py status
python <skill-dir>/scripts/rlcheck.py validate
python <skill-dir>/scripts/rlcheck.py stale
python <skill-dir>/scripts/rlcheck.py check
python <skill-dir>/scripts/rlcheck.py seal tasks/t0007-eu-screening
python <skill-dir>/scripts/rlcheck.py decisions
python <skill-dir>/scripts/rlcheck.py retrieval wos-open-science
```

`<skill-dir>` is wherever `research-log/` lives: `~/.claude/skills/research-log`,
`.claude/skills/research-log`, or `skills/research-log` in a clone of this
repository.

## What is in git

In a research project, everything in the repository is committed except three
machine-local files, which `init` adds to `.gitignore`:

| File | Why it stays local |
|---|---|
| `research-log.local.ini` | the store's path and where Python and `rlcheck.py` are differ on every computer |
| `.rlcheck-cache.json` | cache of file digests, so cloud-synced files are not re-read on every check |
| `.claude/settings.local.json` | Claude Code access and hook, with this machine's paths |

The store is outside the repository and needs no ignore rule. Its backup and
version history come from the shared storage it lives on (OneDrive, SharePoint,
a network drive), not from git.

Two files are committed on purpose:

| File | Why it is in git |
|---|---|
| `tools/rlcheck.py` | the project keeps the version of the checks its records were validated with; updating it is a logged decision |
| `.gitattributes` | `* text=auto eol=lf` keeps text files identical on every machine. Digests of text files are also computed with line endings normalised, so a checkout with CRLF does not make records look stale |

In a project created before `.gitattributes` was added, run `rlcheck init`, then
`git add --renormalize .` and commit. Digests computed by rlcheck before
version 2026.11.3 did not normalise line endings, so after updating the
project's copy run `rlcheck stale` and reseal what it reports.

## Pre-commit hook

If the research project is a git repository with its root at the project root,
`.git/hooks/pre-commit`:

```sh
#!/bin/sh
python tools/rlcheck.py check
```

A commit is refused while any record is incomplete or stale, a snapshot is
undocumented, or the decisions view is out of date. On a machine without the
store, store inputs are skipped, so the hook does not block commits there.

## Session hook (Claude Code)

A `SessionStart` hook puts `rlcheck status` in front of the model whenever a
session starts, resumes, is cleared or has just been compacted. For an
in-progress task, `status` prints its checkpoint and handoff together with an
instruction to read the record before continuing. `rlcheck claude-settings`
installs it in `.claude/settings.local.json` with this machine's paths. Written
by hand, it looks like this:

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

The hook can only restore what is already on disk. There is deliberately no
`PreCompact` hook: it runs before compaction but cannot make the model write
anything, and its output reaches only the user. Keeping the record current is
the job of the checkpoint rules in `SKILL.md`; the hook makes sure the model
reads the result.
