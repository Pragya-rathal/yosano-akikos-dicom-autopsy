# 🔪 Yosano Akiko's DICOM Autopsy

> *"Thou shalt not die — and neither shall your metadata."*

Yosano doesn't flinch at blood. She doesn't flinch at corrupted DICOM headers either. She walks in, cracks the file open, takes what she needs, and leaves before you even realise she was there. Other tools load the pixels. She doesn't. She was never here for the pixels.

This tool tears open `.dcm` files, extracts every tag worth knowing about, and writes it all to clean JSON — no pixel arrays, no suffering, no mercy.

---

## What it does

Scans a folder of DICOM files and pulls out patient metadata (PatientID, Modality, StudyDate, and more) into structured JSON. Fast, ruthless, and unbothered.

Built as a foundation for medical imaging metadata ingestion pipelines. Yosano would approve.

---

## Quickstart

```bash
git clone https://github.com/yourname/yosano-akikos-dicom-autopsy
cd yosano-akikos-dicom-autopsy
pip install pydicom

# run against your own .dcm files
python dicom_extractor.py --input ./dicoms --output metadata.json

# or let Yosano examine pydicom's own built-in test patients (no files needed)
python demo_with_pydicom_data.py
```

---

## CLI usage

```bash
# basic extraction
python dicom_extractor.py --input ./studies --output metadata.json

# recursive — searches sub-folders too
python dicom_extractor.py --input ./studies --output out.json --recursive

# only extract specific tags
python dicom_extractor.py --input ./studies --output out.json \
  --tags PatientID Modality StudyDate
```

---

## Output shape

One record per file. Yosano writes clean notes.

```json
{
  "generated_at": "2024-03-15T10:42:00Z",
  "total_files": 3,
  "records": [
    {
      "file": "CT_small.dcm",
      "path": "/dicoms/CT_small.dcm",
      "extracted_at": "2024-03-15T10:42:01Z",
      "tags": {
        "PatientID": "1CT1",
        "PatientName": "CompressedSamples^CT1",
        "Modality": "CT",
        "StudyDate": "20040119",
        "Rows": "128",
        "Columns": "128",
        "BitsAllocated": "16"
      },
      "errors": []
    }
  ]
}
```

If a file is broken or not actually DICOM, it goes in `errors[]`. Yosano documents everything — even the ones who didn't make it.

---

## Tags extracted by default

| Key | DICOM tag | What it means |
|-----|-----------|---------------|
| PatientID | (0010,0020) | Unique patient identifier |
| PatientName | (0010,0010) | Patient name |
| PatientBirthDate | (0010,0030) | Date of birth |
| PatientSex | (0010,0040) | Patient sex |
| Modality | (0008,0060) | Scan type — CT, MR, CR, US… |
| StudyDate | (0008,0020) | When the study was performed |
| StudyTime | (0008,0030) | Time of study |
| StudyDescription | (0008,1030) | What they were looking for |
| StudyInstanceUID | (0020,000D) | Globally unique study ID |
| SeriesDescription | (0008,103E) | Series-level description |
| SeriesNumber | (0020,0011) | Series number within study |
| SOPInstanceUID | (0008,0018) | Unique ID for this single image |
| BodyPartExamined | (0018,0015) | Which body part was scanned |
| InstitutionName | (0008,0080) | Where the scan was taken |

---

## The one flag you need to know

```python
pydicom.dcmread(path, stop_before_pixels=True)
```

DICOM files can be 50–200MB of raw pixel data. This flag skips all of it and reads only the header. Metadata extraction becomes near-instant even on large CT series.

Yosano doesn't waste time on things she doesn't need.

---

## Running tests

Uses pydicom's bundled CT, MR, CR, and ultrasound files — zero external downloads needed.

```bash
pip install pytest pydicom
pytest tests/ -v
```

```
tests/test_extractor.py::test_ct_modality                PASSED
tests/test_extractor.py::test_mr_modality                PASSED
tests/test_extractor.py::test_missing_tag_returns_none   PASSED
tests/test_extractor.py::test_invalid_file_returns_error PASSED
tests/test_extractor.py::test_scan_finds_both_files      PASSED
...
```

---

## Project structure

```
yosano-akikos-dicom-autopsy/
├── dicom_extractor.py          ← main CLI — the scalpel
├── demo_with_pydicom_data.py   ← runs on pydicom's built-in test files
├── tests/
│   └── test_extractor.py       ← 10 pytest tests, no external data needed
├── sample_output/
│   └── demo_run.json           ← what real output looks like
├── requirements.txt
└── .github/workflows/ci.yml   ← GitHub Actions on Python 3.10 / 3.11 / 3.12
```

---

## Get test DICOM files

pydicom ships ~100 real `.dcm` files inside the package — `demo_with_pydicom_data.py` uses these automatically.

For larger datasets:
- [TCIA — The Cancer Imaging Archive](https://www.cancerimagingarchive.net) — free, public, massive
- [Kaggle DICOM datasets](https://www.kaggle.com/datasets?search=dicom)
- [RSNA AI Challenge archives](https://www.rsna.org/education/ai-resources-and-training/ai-image-challenge)

---

## What's next

- [ ] Group files into Study → Series → Instance hierarchy
- [ ] Anonymisation mode — strip PatientName, PatientID before saving
- [ ] Export to CSV or SQLite
- [ ] Deduplicate by StudyInstanceUID
- [ ] WADO-RS / DICOMweb support

---

## Requirements

```
pydicom>=2.3.0
```

That's it. One dependency. Yosano travels light.

---

## License

MIT — use it, break it, learn from it.

---

*Inspired by Yosano Akiko from Bungo Stray Dogs. No patients were harmed in the making of this tool.*
