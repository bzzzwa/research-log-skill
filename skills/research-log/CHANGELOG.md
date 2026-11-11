# Changelog

What changed in each version of the research-log skill, and what a project has
to do when it moves to that version. The version is the same in `SKILL.md` and
in `scripts/rlcheck.py` (`__version__`).

A project keeps its own copy of the script in `tools/rlcheck.py`. To move a
project from one version to another, read every entry between the two, log the
update as a decision that supersedes the decision for the previous version, run
`rlcheck init --update-tool` from the newer copy, and then do what each entry
lists under *In a project*, oldest first.

---

## Unreleased

Collected here until the next version is released; the version number in
`SKILL.md` and `scripts/rlcheck.py` changes only then.

**Changed**
- The date in the file name of the client's original brief is the day the
  client delivered it, or, if that is not known, the day it was taken over
  (from `rlcheck`). A date printed in the document is not the delivery date.

**In a project**
- Nothing is required. Originals already named by another date keep their
  names: they are frozen.

## 2026.11.9

**Changed**
- README corrections: setting up by hand starts with `git init` and says which
  copy of the script to use before and after `init`; `claude-settings` is marked
  as Claude Code only, also for a second computer; `init --update-tool` must be
  run from the newer copy; only project commands refuse to run outside a
  project; `status` shows the handoff only of a task in progress; the plan and
  README age checks are warnings and do not fail `check`.
- No change to the checks or to `SKILL.md` beyond the version number.

**In a project**
- Nothing is required.

## 2026.11.8

**Changed**
- The repository README is rewritten: requirements, the layout of a project and
  its store, how day-to-day work on a project goes, a table of commands run from
  the project's own copy (`python tools/rlcheck.py`), what is in git, and how to
  update the skill and a project. Upgrade notes per version now live only in
  this changelog.
- No change to the checks or to `SKILL.md` beyond the version number.

**In a project**
- Nothing is required. Updating `tools/rlcheck.py` changes only its version
  number; it can wait for the next version that changes the checks.

## 2026.11.7

**Changed**
- Every file rlcheck writes is written with LF line endings on every platform.
  Before, `decisions`, `seal`, `retrieval` and `init` wrote CRLF on Windows,
  which `doctor` then reported.
- A decision whose `**Decided by.**` says "proposed by Claude" without
  "confirmed" counts as provisional, like one that says "provisional".
- This changelog is new. When a project's copy of the script is older than the
  skill, `SKILL.md` tells Claude to read the changelog for every version in
  between instead of comparing the scripts, and to do what each entry lists
  under *In a project*.

**In a project**
- Run `rlcheck decisions`. Decisions proposed by Claude and never confirmed now
  show as provisional; confirm them with a new entry (`**Confirms.** D00N`) once
  the researcher has agreed.
- If `doctor` still reports CRLF files written by an earlier version, run
  `rlcheck init --fix-line-endings` once.

## 2026.11.6

**Changed**
- A decision to update rlcheck supersedes the decision for the previous
  version, so the in-force view shows one version. `init --update-tool` says so.
- `performed-by:` records only what is known. Filled in for a record closed
  earlier, it is marked "recorded retrospectively on <date>" and limited to
  what can be confirmed. A check done only by a model is stated as such and
  logged as an open limitation.
- `init` no longer calls the skill's own script disposable; only a downloaded
  copy can be deleted after installing.
- `doctor` reports text files still checked out with CRLF; new
  `init --fix-line-endings` converts them.

**In a project**
- If the decisions for earlier versions are all still in force, add one entry
  that supersedes them.
- Run `doctor`; if it reports CRLF files, run `init --fix-line-endings`.
- Check `performed-by:` in records closed before 2026.11.5 against the new rule.

## 2026.11.5

**Changed**
- `seal` will not change a digest in a complete or superseded record without
  `--rerun D0NN` or `--accept D0NN`, and records each change under `resealed:`
  with the old and new digest, the decision and the date.
- A complete record needs `performed-by:`. Instructions a model followed for an
  analytic step and scripts the analysis runs are task inputs.
- `status`, `validate` and `doctor` print today's date from the computer.
  `validate` checks that dates are ISO dates, not in the future, and that no
  task is closed before it was opened.
- `validate` warns when `10-plan.md` is older than the last closed task or
  decision, when its *Next* names a finished task, or when `README.md` is older
  than the plan.
- The store gains `work/` for large intermediates. Outputs in the store may only
  be in `sources/`, `work/` or `exports/`.
- The plan gains a *Proposed* section for ideas for new work, which are not
  worked on until the researcher makes them a task.
- `SKILL.md`: a table of when to run which command; dates only from rlcheck
  output; the skill is not project management; no silent merging of inputs that
  use different categories; rerun, accept, supersede or extend after `stale`.

**In a project**
- Add `performed-by:` to every complete record.
- Run `init --store "<path>"` to create `store:work/`.
- Add a `## Proposed` section to `methodology/10-plan.md`.
- Run `check`.

## 2026.11.4

**Changed**
- Decisions gain `**Confirms.**`: a confirmed provisional decision stays in
  force and is marked confirmed. `status` lists provisional decisions awaiting
  confirmation.
- `validate` fails when a committed entry of `20-decisions.md` or
  `40-insights.md` has been changed (compared with git `HEAD`).
- `SKILL.md` states its version.
- In Claude.ai the script is handed to the user as a download with its SHA-256,
  and `init` is run from the downloaded copy; it is never retyped through a
  connector.

**In a project**
- Run `rlcheck decisions` once: the in-force view now marks provisional and
  confirmed decisions.

## 2026.11.3

The first numbered version.

**Changed**
- `init` copies the script into the project's `tools/rlcheck.py`, which is
  versioned with the project. New `version` command and `init --update-tool`.
- Digests of text files are computed with line endings normalised to LF, and
  `init` writes `.gitattributes` (`* text=auto eol=lf`). The digest cache is
  versioned.
- The store gains `sources/brief/` for the client's original assignment; the
  first task, `t0001-brief`, takes it as input and writes `00-brief.md`.
- `SKILL.md`: where the model may look; decisions outside tasks are logged as
  they are made, with who decided; proposals are confirmed item by item.
- `doctor` recognises Claude Code by its settings files, not by the `.claude/`
  folder.

**In a project**
- Run `init` (and `init --store "<path>"`): it copies the script into `tools/`,
  writes `.gitattributes` and creates `store:sources/brief/`.
- Digests changed: run `stale` and reseal what it reports.
- Put the original brief into `store:sources/brief/` with its date and record
  `t0001-brief`.

## Before 2026.11.3

Unnumbered development versions. They introduced the shared store with
`store:` paths, `research-log.ini` and `research-log.local.ini`, the commands
`doctor`, `init`, `claude-settings` and `where`, checks that distinguish
changed, missing and unavailable inputs, the digest cache, the refusal to run
outside a project, content checks for complete records, the `decisions`,
`limitations` and `retrievals` declarations, retrieval snapshots, the derived
`25-decisions-in-force.md`, checkpoints for tasks in progress, and the
Claude Code session hook. A project created with one of them is brought up to
date by `init` and the steps above.
