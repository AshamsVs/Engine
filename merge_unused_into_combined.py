# merge_unused_into_combined.py
import json
import os
from datetime import datetime

COMBINED = "combined_data_v2.json"
UNUSED = "unused_functions.json"   # the file your unused detector writes
OUT = "combined_data_v3.json"

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def main():
    combined = load_json(COMBINED)
    if combined is None:
        print(f"Error: {COMBINED} not found.")
        return

    unused = load_json(UNUSED)
    if unused is None:
        # try alternate common names
        for alt in ("unused_report.json", "unused_functions_report.json"):
            unused = load_json(alt)
            if unused is not None:
                print(f"Loaded unused list from {alt}")
                break

    if unused is None:
        print("Warning: no unused functions file found. Nothing to merge.")
        # still write combined with updated metadata
        combined["metadata"]["merged_unused_at"] = datetime.now().isoformat()
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2)
        print(f"Wrote {OUT} (unchanged unused_functions).")
        return

    # Merge: replace/insert the unused_functions key
    combined["unused_functions"] = unused

    # update metadata
    meta = combined.get("metadata", {})
    meta["merged_unused_at"] = datetime.now().isoformat()
    meta["unused_source"] = os.path.abspath(UNUSED)
    combined["metadata"] = meta

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)

    print(f"Wrote {OUT} with merged unused functions (from {UNUSED}).")

if __name__ == "__main__":
    main()
