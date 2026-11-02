# Social research generalization rules

Reusable rules for running social-science desk research with an LLM, so that the
conversation stops being the memory of the project.

The premise: the interpretive work — framing, search vocabulary, inclusion
judgements, synthesis — stays with the researcher. The bookkeeping does not.
If every phase leaves a complete written trace on disk, a fresh conversation
costs nothing and context is never silently lost to compaction.

## Contents

- `skills/research-log/` — the general skill: file classes, document set,
  task-record schema, closing gate, staleness handling.
  - `SKILL.md` — the skill itself
  - `reference/documents.md` — the methodology documents and their templates
  - `reference/task-records.md` — task record format and the dependency schema
  - `reference/retrievals.md` — snapshots of search and tool results
  - `reference/project-profile.md` — how to write the per-project layer
  - `scripts/rlcheck.py` — validation, staleness and derived views, zero dependencies

## Design

**Two layers.** The skill holds what is true of every project. `PROFILE.md` in
each research project holds what is true of that one: source types, task types,
vocabulary, deliverable. Nothing project-specific ever enters the skill.

**Four file classes.** Every file is frozen, living, append-only or derived, and
the class determines how it may be changed. Most context loss comes from
treating a living document as a historical record, or the reverse.

**Staleness is a build problem, not a prompt problem.** Task records declare
their inputs with digests. When a source set grows or the brief is amended,
`rlcheck.py stale` names the affected records. The model is never asked to work
this out by reading.

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

## Use

**Claude Code (intended).** Copy `skills/research-log/` into `~/.claude/skills/`
or into the project's `.claude/skills/`. Start Claude Code in the research
project's root; the model runs the checks itself.

**Claude.ai.** Zip the `research-log` folder and upload it under
Settings → Skills (requires code execution enabled). Keep each research
project's `PROFILE.md` either on disk, read through the Filesystem connector at
the start of a session, or as the instructions of a Claude Project. The
Filesystem connector cannot execute anything on your machine, so the model will
ask you to run `rlcheck` and paste the output; keep a terminal open in the
project.

## Commands

Always run from the research project's root; the script works on the current
directory, wherever it is installed.

```
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

## Pre-commit hook

If the research project is a git repository with its root at the project root,
`.git/hooks/pre-commit`:

```sh
#!/bin/sh
python "$HOME/.claude/skills/research-log/scripts/rlcheck.py" check
```

A commit is refused while any record is incomplete or stale, a snapshot is
undocumented, or the decisions view is out of date.

## Session hook (Claude Code)

A `SessionStart` hook puts `rlcheck status` in front of the model whenever a
session starts, resumes, is cleared or has just been compacted. For an
in-progress task, `status` prints its checkpoint and handoff together with an
instruction to read the record before continuing. In the research project's
`.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd \"$CLAUDE_PROJECT_DIR\" && python \"$HOME/.claude/skills/research-log/scripts/rlcheck.py\" status"
          }
        ]
      }
    ]
  }
}
```

Adjust the script path if the skill is installed in the project's
`.claude/skills/` instead.

The hook can only restore what is already on disk. There is deliberately no
`PreCompact` hook: it runs before compaction but cannot make the model write
anything, and its output reaches only the user. Keeping the record current is
the job of the checkpoint rules in `SKILL.md`; the hook makes sure the model
reads the result.
