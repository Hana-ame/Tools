#!/usr/bin/env python3
"""List per-session token usage from the opencode sqlite database.
One row per session, no aggregation, no dedup.

Usage:
  session_usage.py            # all sessions, newest first
  session_usage.py --from 2026-08-01 --to 2026-08-06
  session_usage.py --limit 20
  session_usage.py --json     # raw JSON output
  session_usage.py --db PATH  # override db location
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import date, datetime

PRICE_CACHE_READ_M = 0.02
PRICE_INPUT_M = 1.0
PRICE_OUTPUT_M = 2.0  # output + reasoning combined


def est_price(in_tok: float, out_tok: float, rsn_tok: float, cache_r: float) -> float:
    return (float(cache_r) / 1e6 * PRICE_CACHE_READ_M
            + float(in_tok) / 1e6 * PRICE_INPUT_M
            + (float(out_tok) + float(rsn_tok)) / 1e6 * PRICE_OUTPUT_M)


def default_db() -> str:
    path = os.environ.get("OPENCODE_DB")
    if path:
        return path
    return os.path.expanduser("~/.local/share/opencode/opencode.db")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from", dest="from_day", help="start date YYYY-MM-DD")
    ap.add_argument("--to", dest="to_day", help="end date YYYY-MM-DD (default today)")
    ap.add_argument("--limit", type=int, help="max rows (default: all)")
    ap.add_argument("--json", action="store_true", help="output raw JSON")
    ap.add_argument("--db", default=default_db(), help="sqlite db path")
    args = ap.parse_args()

    lo, hi = 0, float("inf")
    if args.from_day:
        d = datetime.strptime(args.from_day, "%Y-%m-%d")
        lo = int(d.timestamp()) * 1000
    if args.to_day:
        d = datetime.strptime(args.to_day, "%Y-%m-%d")
        hi = int(d.timestamp()) * 1000 + 86400000

    try:
        con = sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)
    except sqlite3.Error as e:
        print(f"error: cannot open db: {e}", file=sys.stderr)
        return 1

    rows = con.execute(
        """SELECT s.time_created, s.time_updated, s.title, s.directory, s.agent, s.model,
                  s.tokens_input, s.tokens_output, s.tokens_reasoning,
                  s.tokens_cache_read, s.tokens_cache_write, s.cost,
                  COALESCE(m.cnt, 0)
           FROM session s
           LEFT JOIN (SELECT session_id, COUNT(*) AS cnt
                        FROM message
                       WHERE json_extract(data, '$.role') = 'assistant'
                       GROUP BY session_id) m
             ON m.session_id = s.id
           WHERE s.time_created >= ? AND s.time_created < ?
           ORDER BY s.time_created DESC
           LIMIT ?""",
        (lo, hi, args.limit or -1),
    ).fetchall()

    if args.json:
        print(json.dumps([
            {"time_created": r[0], "time_updated": r[1], "title": r[2],
             "directory": r[3], "agent": r[4], "model": r[5],
             "tokens_input": r[6], "tokens_output": r[7], "tokens_reasoning": r[8],
             "tokens_cache_read": r[9], "tokens_cache_write": r[10], "cost": r[11],
             "requests": r[12],
             "est_cost": round(est_price(r[6], r[7], r[8], r[9]), 4)}
            for r in rows
        ], indent=2))
        return 0

    if not rows:
        print("no sessions in range")
        return 0

    hdr = (f"{'created':<19}{'updated':<19}{'req':>4}{'in':>12}{'out':>10}{'rsn':>10}"
           f"{'cache_r':>13}{'cache_w':>13}{'est$':>9}  title")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        created = datetime.fromtimestamp(r[0] / 1000).strftime("%Y-%m-%d %H:%M")
        updated = datetime.fromtimestamp(r[1] / 1000).strftime("%Y-%m-%d %H:%M")
        est = est_price(r[6], r[7], r[8], r[9])
        print(f"{created:<19}{updated:<19}{r[12]:>4,}{r[6]:>12,}{r[7]:>10,}{r[8]:>10,}"
              f"{r[9]:>13,}{r[10]:>13,}{est:>9.4f}  {(r[2] or '')[:46]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
