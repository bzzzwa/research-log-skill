# Retrieval snapshots

A retrieval is anything that reaches the research through a tool rather than as
a file the user supplied: a web search, a query in a database interface, a call
to an MCP connector or API, a page fetched or pasted. Its results are not on
disk, and they cannot be fetched again later: databases are updated, rankings
shift, pages change. A result that rests on an unsaved retrieval cannot be
checked, reproduced or tested for staleness.

So every retrieval that shapes a result becomes a frozen snapshot, at the moment
it is made.

## When to snapshot

Snapshot when the results will be used: screened, counted, cited, compared, or
used to decide what to search next. Do not snapshot exploratory lookups that are
discarded — but if an exploratory search changes the vocabulary, the decision is
logged in `20-decisions.md` and the search that prompted it is snapshotted.

When in doubt, snapshot. A spare directory costs nothing; a missing one cannot
be recreated.

## Layout

```
sources/retrieved/
  2026-09-05-wos-open-science/
    retrieval.md        the manifest
    results.csv         what the tool returned, as raw as possible
    ...
```

One directory per retrieval. The directory name starts with the retrieval date,
so a rerun of the same search on a later day is a new snapshot, never an
overwrite. Create it with

```
rlcheck retrieval wos-open-science
```

which makes the directory and an empty manifest.

## What goes in the directory

The results as the tool returned them: an export file, the JSON of a connector
response, the result list of a web search, a saved page. Prefer the rawest form
available over a summary. If only part could be saved (an export limit, a
truncated response, a paywall), say so in the manifest.

If a search returned nothing, that is a result: set `results: 0` and the
directory may contain only the manifest.

If the results are too large for the repository (a full database export of
hundreds of megabytes), put them in the store under a directory with the same
name, `store:retrieved/2026-09-05-wos-open-science/`, and add
`data: store:retrieved/2026-09-05-wos-open-science` to the manifest. The manifest
stays in the repository. The task then lists both the snapshot directory and the
`data` path among its inputs, so both are digested.

## Manifest: retrieval.md

````markdown
---
tool: Web of Science web UI
source: Web of Science Core Collection
retrieved: 2026-09-05T10:00:00
results: 412
captured: full
task: t0007
---

## Query
```
TS=("open science" OR "open data") AND PY=(2015-2026)
```

## Not captured
<only if captured is partial: what was returned but not saved, and why>

## Notes
<anything a reader needs to interpret the files in this directory>
````

| Field | Meaning |
|---|---|
| `tool` | how the retrieval was made: interface, connector, API |
| `source` | the database, index or site queried |
| `retrieved` | ISO date and time of the retrieval |
| `results` | the number of hits the source reported, or `n/a` if it reports none |
| `captured` | `full` if everything returned was saved, `partial` otherwise |
| `task` | the task that made the retrieval |
| `data` | optional: a store path holding results too large for the repository |

The exact query goes in `## Query`, in a code block, verbatim — with filters,
date limits and any parameters set in the interface. It is not in the front
matter because search strings contain quotes and colons. `## Not captured` is
required when `captured: partial`. Delete the template lines of any section you do not
use; `validate` treats leftover `<...>` text as a placeholder.

## What validate checks

For every directory under `sources/retrieved/`: the manifest exists and parses;
`tool`, `source`, `retrieved`, `results` and `captured` are filled; `captured`
is `full` or `partial`; `## Query` is not empty; a partial snapshot says what is
missing; no template text is left; and there is at least one result file unless
`results: 0` — in the snapshot directory, or in the `data` directory when the
manifest names one and the store is reachable.

For every complete task record: each snapshot listed under `retrievals` exists
and is covered by `inputs`, and so is its `data` path if it has one, so that
`stale` notices if a snapshot is changed.

## Rules

- A snapshot is frozen. Never add to it, trim it or "clean" it. Cleaned or
  deduplicated data is a task output, written to the task's directory.
- Never refresh a snapshot in place. A new run is a new snapshot.
- Personal data in results follows the project's data-handling rules in
  `PROFILE.md`; if none are stated, ask before saving it.
