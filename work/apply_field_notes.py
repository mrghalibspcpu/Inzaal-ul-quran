#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append curated «مزید تجزیاتی نکات» blocks to Quran.talighe -- idempotent.

Usage: python3 work/apply_field_notes.py <content.py> [db_path]

The content file defines:
    NOTES = { <ayah ID>: "<Urdu text with '\\n'-separated '• ' bullet lines>", ... }

Rules (same safeguards as the rest of the pipeline):
  * only the talighe column is touched -- Arabic/tr/IDs/schema stay byte-identical;
  * the added block is generic and never names a scholarly field as a "label";
  * re-applying the same file replaces the existing «مزید تجزیاتی نکات:» block
    instead of duplicating it.
"""
import sys, os, sqlite3, importlib.util, re

MARKER = "مزید تجزیاتی نکات:"

def load_notes(path):
    spec = importlib.util.spec_from_file_location("field_notes_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    notes = getattr(mod, "NOTES", None)
    if not isinstance(notes, dict):
        raise SystemExit("content file must define NOTES = {id: text}")
    return notes

def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: apply_field_notes.py <content.py> [db_path]")
    content_path, db_path = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "quran.db")
    notes = load_notes(content_path)
    con = sqlite3.connect(db_path)
    done = missing = 0
    for aid, text in notes.items():
        row = con.execute("SELECT talighe FROM Quran WHERE ID=?", (int(aid),)).fetchone()
        if not row:
            print("MISSING ID", aid); missing += 1; continue
        tal = row[0] or ""
        body = "\n".join(l.rstrip() for l in text.strip().splitlines() if l.strip())
        block = MARKER + "\n" + body
        pos = tal.find(MARKER)
        tal = (tal[:pos].rstrip() + "\n\n" + block) if pos != -1 else (tal.rstrip() + "\n\n" + block)
        con.execute("UPDATE Quran SET talighe=? WHERE ID=?", (tal, int(aid)))
        done += 1
    con.commit(); con.close()
    print(f"applied {done} note(s), missing {missing}")

if __name__ == "__main__":
    main()
