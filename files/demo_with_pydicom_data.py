"""
demo_with_pydicom_data.py
--------------------------
Run the extractor against pydicom's built-in test files.
These ship with the library — no separate download needed.

    pip install pydicom
    python demo_with_pydicom_data.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime

try:
    import pydicom
    from pydicom.data import get_testfiles_name
    from pydicom.errors import InvalidDicomError
except ImportError:
    sys.exit("Run:  pip install pydicom")

TAGS = {
    "PatientID":        "PatientID",
    "PatientName":      "PatientName",
    "Modality":         "Modality",
    "StudyDate":        "StudyDate",
    "StudyDescription": "StudyDescription",
    "SeriesDescription":"SeriesDescription",
    "SOPInstanceUID":   "SOPInstanceUID",
    "Rows":             "Rows",
    "Columns":          "Columns",
    "BitsAllocated":    "BitsAllocated",
}

def extract(path: Path) -> dict:
    record = {"file": path.name, "tags": {}, "errors": []}
    try:
        ds = pydicom.dcmread(str(path), stop_before_pixels=True)
        for label, keyword in TAGS.items():
            raw = ds.get(keyword)
            record["tags"][label] = str(raw.value) if raw is not None else None
    except InvalidDicomError as e:
        record["errors"].append(str(e))
    return record

def main():
    # pydicom ships ~100 test .dcm files inside the package itself
    test_files = [Path(p) for p in get_testfiles_name() if p.endswith(".dcm")]
    print(f"Found {len(test_files)} built-in test files in pydicom\n")

    results = []
    for i, path in enumerate(test_files[:10], 1):   # first 10 for demo
        r = extract(path)
        status = "OK " if not r["errors"] else "ERR"
        mod  = r["tags"].get("Modality") or "?"
        date = r["tags"].get("StudyDate") or "?"
        pid  = r["tags"].get("PatientID") or "?"
        print(f"  [{i:>2}/10] {status}  {path.name:<30}  mod={mod:<4} date={date}  pid={pid}")
        results.append(r)

    out = Path("sample_output/demo_run.json")
    out.parent.mkdir(exist_ok=True)
    with out.open("w") as f:
        json.dump({"generated_at": datetime.utcnow().isoformat()+"Z",
                   "source": "pydicom built-in test files",
                   "records": results}, f, indent=2)
    print(f"\nSaved → {out}")

if __name__ == "__main__":
    main()
