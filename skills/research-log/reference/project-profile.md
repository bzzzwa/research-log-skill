# The project layer: PROFILE.md

The skill holds what is true of every project. `PROFILE.md` holds what is true
of this one. Keeping them apart is what makes the skill reusable — the moment a
source type or a client convention leaks into the skill, it stops generalising.

Write `PROFILE.md` with the user at the start of a project, before any task is
opened. Rewrite it when the material changes. It is a living document.

## Template

```markdown
# Project profile

**Project.** <short name>
**Started.** YYYY-MM-DD

## Source types
For each kind of material this project draws on:

### <e.g. Peer-reviewed articles>
- **Where they come from.** <databases, search interfaces, access route>
- **Where they live.** `sources/articles/`
- **Intake.** <how a new item is added: filename convention, metadata captured,
  whether full text is extracted and to where>
- **Citable as.** <BibTeX key scheme, or how they are referenced in outputs>
- **Trust level.** <how findings from this type may be used>

### <e.g. Workshop notes>
...

## Task types
The recurring units of work in this project, and what "done" means for each.

| Task type | Question shape | Typical inputs | Outputs | Done when |
|---|---|---|---|---|
| search | which items exist on X? | search protocol, brief | result set + search log | protocol executed and logged |
| screening | which items are in scope? | result set, criteria | decision table | every item has a recorded verdict |
| extraction | what does each item say about Y? | included set | extraction table | every included item has a row |
| synthesis | what is the answer to RQ? | extraction tables | draft section | traceable to extractions |

## Vocabulary
Terms that mean something specific here, and terms that are contested and
therefore searched under several names.

| Term | Definition used here | Also searched as |
|---|---|---|

## Languages
<which languages are searched, which are excluded, and what that costs — this
belongs in 30-limitations.md as well>

## Deliverable
**Format.** <report, slides, workshop input>
**Audience.** <who reads it and what they already know>
**Citation style.** <...>
**Constraints.** <length, deadline, confidentiality>

## Data handling
<whether retrieved material may contain personal data, what may be saved in
sources/retrieved/, and what must be anonymised or left out>

## Conventions specific to this project
<anything the general skill does not cover>
```

## What belongs where

| Belongs in the skill | Belongs in PROFILE.md |
|---|---|
| file classes and the rule for each | which folders hold which source type |
| the record schema | what a task is in this project |
| the closing gate | what "done" means for a screening task here |
| the staleness mechanism | which inputs a typical task depends on |
| read order for a fresh session | the contested vocabulary of this topic |

If unsure: ask whether the rule would still be right for a completely different
research question. If yes, it is skill-level. If no, it is profile-level.

## In Claude.ai rather than Claude Code

Claude Code is the intended environment: the project directory is the working
directory, so the model runs `rlcheck` itself and the closing gate is enforced
in the session.

The same split works in Claude.ai. Upload the skill folder as a zip under
Settings, and keep `PROFILE.md` either on disk (read through the Filesystem
connector at the start of each session) or as the instructions of a Claude
Project, one Project per research project. The Project instructions are the
project layer.

The Filesystem connector reads and writes files but cannot execute anything on
your machine, so in Claude.ai the model cannot run `rlcheck` against the
project. It will give you the command and ask you to run it from the project
root and paste the output. Keep a terminal open in the project for this, or
wire `rlcheck check` into a pre-commit hook so the gate runs regardless.
