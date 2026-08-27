#!/usr/bin/env python3
"""rlcheck - completeness and freshness checks for a research-log project.

Deterministic bookkeeping that an LLM should never be asked to do by eye:
which task outputs are stale because their inputs changed, and which task
records are incomplete.

Usage, from the project root:
    python rlcheck.py status              # short summary, safe to paste into a new session
    python rlcheck.py validate            # structural check of every task record
    python rlcheck.py stale               # recompute input digests, report drift
    python rlcheck.py seal tasks/t0007    # write current input digests into a record

Zero dependencies, Python 3.8+.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

RECORD_NAME = "record.md"
TASKS_DIR = "tasks"

REQUIRED_KEYS = ["id", "title", "status", "opened", "inputs", "outputs"]
ALLOWED_STATUS = {"planned", "in-progress", "complete", "superseded"}
REQUIRED_HEADINGS = [
    "## Question",
    "## Method as executed",
    "## What was done",
    "## Findings",
    "## Limitations raised",
    "## Handoff",
]

SKIP_NAMES = {".git", ".DS_Store", "__pycache__", ".ipynb_checkpoints"}


# --------------------------------------------------------------------------
# Minimal front-matter reader
# --------------------------------------------------------------------------
# Deliberately supports only the subset the record schema uses:
#   key: scalar
#   key:
#     - scalar
#   key:
#     - subkey: scalar
#       subkey: scalar
# Anything else raises, loudly, rather than being silently misread.


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_front_matter(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("file does not start with a '---' front-matter fence")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise ValueError("front matter is not closed by a second '---'")

    data = {}
    key = None
    i = 1
    while i < end:
        raw = lines[i]
        stripped = raw.strip()
        i += 1
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(raw) - len(raw.lstrip(" "))

        if indent == 0:
            if ":" not in stripped:
                raise ValueError(f"cannot parse front-matter line: {raw!r}")
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = _strip_quotes(value)
            data[key] = value if value not in ("", "null", "~") else None
            continue

        if stripped.startswith("- "):
            if key is None:
                raise ValueError(f"list item before any key: {raw!r}")
            item = stripped[2:].strip()
            if data.get(key) in (None, ""):
                data[key] = []
            if not isinstance(data[key], list):
                raise ValueError(f"key {key!r} has both a scalar and list items")
            if ":" in item:
                k, _, v = item.partition(":")
                data[key].append({k.strip(): _strip_quotes(v)})
            else:
                data[key].append(_strip_quotes(item))
            continue

        # continuation of the last mapping in the current list
        if key is None or not isinstance(data.get(key), list) or not data[key]:
            raise ValueError(f"unexpected indented line: {raw!r}")
        last = data[key][-1]
        if not isinstance(last, dict):
            raise ValueError(f"cannot add a field to a scalar list item: {raw!r}")
        if ":" not in stripped:
            raise ValueError(f"cannot parse front-matter line: {raw!r}")
        k, _, v = stripped.partition(":")
        last[k.strip()] = _strip_quotes(v)

    return data, end


# --------------------------------------------------------------------------
# Digests
# --------------------------------------------------------------------------


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def digest(root: Path, rel: str) -> str:
    """Digest of a file or of a directory tree, as 'sha256:...' or 'tree:...'."""
    target = (root / rel).resolve()
    if not target.exists():
        return "missing"
    if target.is_file():
        return "sha256:" + _hash_file(target)

    entries = []
    for path in sorted(target.rglob("*")):
        if any(part in SKIP_NAMES for part in path.parts):
            continue
        if path.is_file():
            entries.append(
                path.relative_to(target).as_posix() + "\0" + _hash_file(path)
            )
    h = hashlib.sha256("\n".join(entries).encode("utf-8"))
    return "tree:" + h.hexdigest()


# --------------------------------------------------------------------------
# Records
# --------------------------------------------------------------------------


def find_records(root: Path):
    tasks = root / TASKS_DIR
    if not tasks.is_dir():
        return []
    return sorted(p / RECORD_NAME for p in tasks.iterdir() if (p / RECORD_NAME).is_file())


def load_record(path: Path):
    text = path.read_text(encoding="utf-8")
    meta, end = parse_front_matter(text)
    body = "\n".join(text.splitlines()[end + 1 :])
    return meta, body


def validate(root: Path) -> int:
    records = find_records(root)
    if not records:
        print(f"no task records found under {TASKS_DIR}/")
        return 0

    problems = 0
    seen_ids = {}
    for path in records:
        rel = path.relative_to(root).as_posix()
        try:
            meta, body = load_record(path)
        except ValueError as exc:
            print(f"FAIL {rel}: {exc}")
            problems += 1
            continue

        for key in REQUIRED_KEYS:
            if key not in meta or meta[key] in (None, "", []):
                print(f"FAIL {rel}: missing or empty front-matter key '{key}'")
                problems += 1

        status = meta.get("status")
        if status and status not in ALLOWED_STATUS:
            print(f"FAIL {rel}: status '{status}' not one of {sorted(ALLOWED_STATUS)}")
            problems += 1
        if status == "complete" and not meta.get("closed"):
            print(f"FAIL {rel}: status is 'complete' but 'closed' date is missing")
            problems += 1

        rid = meta.get("id")
        if rid:
            if rid in seen_ids:
                print(f"FAIL {rel}: duplicate id '{rid}' (also in {seen_ids[rid]})")
                problems += 1
            seen_ids[rid] = rel

        for heading in REQUIRED_HEADINGS:
            if heading not in body:
                print(f"FAIL {rel}: missing section '{heading}'")
                problems += 1

        for item in meta.get("inputs") or []:
            if not isinstance(item, dict) or "path" not in item:
                print(f"FAIL {rel}: every input needs a 'path' field, got {item!r}")
                problems += 1
                continue
            if not (root / item["path"]).exists():
                print(f"FAIL {rel}: input path does not exist: {item['path']}")
                problems += 1

        for out in meta.get("outputs") or []:
            out_path = out["path"] if isinstance(out, dict) else out
            if not (root / out_path).exists():
                print(f"WARN {rel}: declared output does not exist: {out_path}")

    print(f"\n{len(records)} record(s) checked, {problems} problem(s).")
    return 1 if problems else 0


def stale(root: Path) -> int:
    records = find_records(root)
    drifted = 0
    unsealed = 0

    for path in records:
        rel = path.relative_to(root).as_posix()
        try:
            meta, _ = load_record(path)
        except ValueError as exc:
            print(f"FAIL {rel}: {exc}")
            drifted += 1
            continue

        if meta.get("status") == "superseded":
            continue

        for item in meta.get("inputs") or []:
            if not isinstance(item, dict) or "path" not in item:
                continue
            recorded = item.get("digest")
            if not recorded:
                print(f"UNSEALED {rel}: no digest recorded for {item['path']}")
                unsealed += 1
                continue
            current = digest(root, item["path"])
            if current != recorded:
                print(f"STALE {rel}")
                print(f"       input:    {item['path']}")
                print(f"       recorded: {recorded}")
                print(f"       current:  {current}")
                drifted += 1

    total = len(records)
    print(f"\n{total} record(s) checked, {drifted} stale, {unsealed} unsealed input(s).")
    return 1 if drifted or unsealed else 0


def seal(root: Path, task_dir: str) -> int:
    path = (root / task_dir / RECORD_NAME) if (root / task_dir).is_dir() else (root / task_dir)
    if not path.is_file():
        print(f"no record found at {path}")
        return 1

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    updated = 0
    current_input_path = None
    out = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- path:"):
            current_input_path = _strip_quotes(stripped.split(":", 1)[1])
            out.append(line)
            continue
        if stripped.startswith("digest:") and current_input_path:
            indent = " " * (len(line) - len(line.lstrip(" ")))
            new = digest(root, current_input_path)
            out.append(f"{indent}digest: {new}")
            print(f"  {current_input_path} -> {new}")
            updated += 1
            current_input_path = None
            continue
        out.append(line)

    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"sealed {updated} input digest(s) in {path}")
    return 0


def status(root: Path) -> int:
    records = find_records(root)
    counts = {}
    open_records = []
    for path in records:
        try:
            meta, _ = load_record(path)
        except ValueError:
            counts["unparseable"] = counts.get("unparseable", 0) + 1
            continue
        st = meta.get("status") or "unknown"
        counts[st] = counts.get(st, 0) + 1
        if st in ("planned", "in-progress"):
            open_records.append(f"  {meta.get('id')} {meta.get('title')} [{st}]")

    print(f"project: {root}")
    print(f"records: {len(records)}")
    for key in sorted(counts):
        print(f"  {key}: {counts[key]}")
    if open_records:
        print("open:")
        print("\n".join(open_records))
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    command = argv[1]
    root = Path.cwd()

    if command == "validate":
        return validate(root)
    if command == "stale":
        return stale(root)
    if command == "status":
        return status(root)
    if command == "seal":
        if len(argv) < 3:
            print("usage: rlcheck.py seal <task-dir>")
            return 2
        return seal(root, argv[2])

    print(f"unknown command: {command}")
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
