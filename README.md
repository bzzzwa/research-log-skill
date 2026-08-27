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
  - `reference/project-profile.md` — how to write the per-project layer
  - `scripts/rlcheck.py` — validation and staleness checks, zero dependencies

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

**The gate is mechanical.** A task is finished when its record validates, not
when the work feels done. `rlcheck.py validate` exits non-zero on an incomplete
record and can be wired into a pre-commit hook.

## Use

With Claude Code, copy `skills/research-log/` into `~/.claude/skills/` or the
project's `.claude/skills/`.

With Claude.ai, zip the `research-log` folder and upload it under
Settings → Skills (requires code execution enabled). Keep each research
project's `PROFILE.md` either on disk, read through the Filesystem connector at
the start of a session, or as the instructions of a Claude Project.

Run the script locally rather than through the model:

```
python skills/research-log/scripts/rlcheck.py status
python skills/research-log/scripts/rlcheck.py validate
python skills/research-log/scripts/rlcheck.py stale
python skills/research-log/scripts/rlcheck.py seal tasks/t0007-eu-screening
```
