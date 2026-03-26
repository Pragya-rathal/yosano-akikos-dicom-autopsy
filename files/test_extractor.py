"""
tests/test_extractor.py
Unit tests using pydicom built-in test files.
Run with: pytest tests/
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import pytest
from dicom_extractor import extract_tags, scan_folder, DEFAULT_TAGS

@pytest.fixture(scope="module")
def ct_path():
    from pydicom.data import get_testfiles_name
    m = [p for p in get_testfiles_name() if "CT_small" in p]
    if not m: pytest.skip("CT_small.dcm not in pydicom test files")
    return Path(m[0])

@pytest.fixture(scope="module")
def mr_path():
    from pydicom.data import get_testfiles_name
    m = [p for p in get_testfiles_name() if "MR_small" in p]
    if not m: pytest.skip("MR_small.dcm not in pydicom test files")
    return Path(m[0])

def test_ct_modality(ct_path):
    r = extract_tags(ct_path, {"Modality": "Modality"})
    assert r["tags"]["Modality"] == "CT"
    assert r["errors"] == []

def test_mr_modality(mr_path):
    r = extract_tags(mr_path, {"Modality": "Modality"})
    assert r["tags"]["Modality"] == "MR"

def test_missing_tag_returns_none(ct_path):
    r = extract_tags(ct_path, {"FakeTag": "PixelSpacingCalibrationDescription"})
    assert r["tags"]["FakeTag"] is None
    assert r["errors"] == []

def test_all_default_tags_extracted(ct_path):
    r = extract_tags(ct_path, DEFAULT_TAGS)
    for label in DEFAULT_TAGS:
        assert label in r["tags"]

def test_result_contains_filename(ct_path):
    r = extract_tags(ct_path, DEFAULT_TAGS)
    assert r["file"] == ct_path.name

def test_invalid_file_returns_error(tmp_path):
    bad = tmp_path / "notadicom.dcm"
    bad.write_text("this is not DICOM")
    r = extract_tags(bad, DEFAULT_TAGS)
    assert len(r["errors"]) > 0
    assert r["tags"] == {}

def test_missing_file_returns_error(tmp_path):
    r = extract_tags(tmp_path / "ghost.dcm", DEFAULT_TAGS)
    assert len(r["errors"]) > 0

def test_scan_empty_folder(tmp_path):
    assert scan_folder(tmp_path, DEFAULT_TAGS) == []

def test_scan_finds_both_files(tmp_path, ct_path, mr_path):
    import shutil
    shutil.copy(ct_path, tmp_path / "CT_small.dcm")
    shutil.copy(mr_path, tmp_path / "MR_small.dcm")
    results = scan_folder(tmp_path, DEFAULT_TAGS)
    assert len(results) == 2
    assert {r["tags"]["Modality"] for r in results} == {"CT", "MR"}

def test_json_serialisable(ct_path):
    r = extract_tags(ct_path, DEFAULT_TAGS)
    reloaded = json.loads(json.dumps(r))
    assert reloaded["file"] == ct_path.name
