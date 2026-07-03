# Quality Control (QC) Examples

This document shows practical examples of using **nidataset.qc** with CT-Manager to catch silent dataset bugs.

## 1. Check a Single Volume

```bash
python3 main.py --task=qc_check --dataset=example
```

Output:
```
QC report saved to output/qc_report.json
Status: ok ({'ok': 13, 'warning': 0, 'error': 0})
```

### Python API (direct use):

```python
import nidataset as nid

# Single file
report = nid.qc.check_volume("ct.nii.gz")
print(report.status)  # "ok", "warning", or "error"
for issue in report.issues():
    print(f"{issue.name}: {issue.message}")
```

## 2. Check Dataset Folder (cross-file coherence)

```bash
python3 main.py --task=qc_dataset --dataset=example --output_folder=qc_results
```

Output:
```
Dataset QC: 42 items
Status: warning
Summary: {'ok': 39, 'warning': 2, 'error': 1}

Distributions:
  orientation: {'RAS': 40, 'LAS': 2}
  dtype: {'uint8': 42}
  orientation outliers: ['scan_005.nii.gz', 'scan_033.nii.gz']
  
Full report saved to qc_results/qc_dataset_report.json
```

### Python API:

```python
import nidataset as nid

ds = nid.qc.check_dataset("scans/")
print(f"Items: {len(ds.items)}")
print(f"Status: {ds.status}")
print(f"Orientation distribution: {ds.distributions['orientation']}")

# Identify outliers
for path in ds.distributions["outliers"]["orientation"]:
    print(f"Orientation mismatch: {path}")
```

## 3. Check Image ↔ Mask Pairs

Silent bug: mask shifted 3mm in world space, shapes match, no crash → poisons training.

```bash
python3 main.py --pair ct.nii.gz brain_mask.nii.gz
```

### Python API:

```python
import nidataset as nid

rep = nid.qc.check_pair("ct.nii.gz", "brain_mask.nii.gz")
if "affine_match_mask" in [r.name for r in rep.issues()]:
    print("ALERT: Mask misaligned in world space!")
```

## 4. Check Image ↔ Mask ↔ Annotation Triples

```bash
python3 main.py --triple ct.nii.gz brain.nii.gz lesion.nii.gz
```

Checks:
- Shape match
- Affine alignment (world space)
- Annotation is contained in mask
- Annotation has valid label values (binary 0/1)

## 5. Catch Common Silent Bugs

### NaN in data (kills training silently)

```python
import numpy as np
import nibabel as nib
import nidataset as nid

data = np.random.rand(64, 64, 64).astype(np.float32)
data[5, 5, 5] = np.nan  # Silent poison

nib.save(nib.Nifti1Image(data, np.eye(4)), "bad.nii.gz")
rep = nid.qc.check_volume("bad.nii.gz")
print(rep.issues())  # ✗ finite_values: Data has 1 NaN and 0 inf voxels.
```

### LAS vs RAS orientation mismatch

```python
# Dataset has 287 RAS, 13 LAS (model trained on mixed orientation)
ds = nid.qc.check_dataset("scans/")
print(ds.distributions["orientation"])  # {'RAS': 287, 'LAS': 13}
print(ds.distributions["outliers"]["orientation"])  # ['scan_042.nii.gz', ...]
```

### Anisotropic spacing (5x on one axis)

```python
rep = nid.qc.check_volume("anisotropic.nii.gz")
# ⚠ spacing_isotropy: Anisotropic spacing (max/min-1=4.000 > 0.05)
```

## 6. JSON Reports for CI/CD

Both `qc_check` and `qc_dataset` tasks output JSON:

```json
{
  "kind": "volume",
  "target": "scan_001.nii.gz",
  "status": "ok",
  "results": [
    {"name": "orientation", "status": "ok", "message": "..."},
    {"name": "affine_nonsingular", "status": "ok", "message": "..."},
    {"name": "finite_values", "status": "ok", "message": "..."}
  ],
  "meta": {
    "orientation": "RAS",
    "spacing": [1.0, 1.0, 2.5],
    "shape": [512, 512, 128]
  }
}
```

Use in CI: `--strict` flag exits with code 1 on any error:

```bash
python3 main.py --task=qc_dataset --dataset=my_dataset --strict
echo $?  # 1 if errors found, 0 otherwise
```

## 7. Custom QC Config

Create `qc_config.json`:

```json
{
  "expected_orientation": "RAS",
  "affine_atol": 0.001,
  "max_empty_slice_fraction": 0.3,
  "isotropy_tol": 0.1
}
```

Then use via Python:

```python
from nidataset.qc import QCConfig, check_dataset

cfg = QCConfig.load("qc_config.json")
ds = check_dataset("scans/", config=cfg)
```

## What Gets Checked

### Geometry
- ✓ Affine matrix non-singular
- ✓ Orientation (RAS/LAS/etc.)
- ✓ Spacing isotropy
- ✓ 4D volumes (flagged as warning)

### Data
- ✓ NaN / Inf values
- ✓ dtype (int64 warned)
- ✓ All-zero volumes
- ✓ All-black slices (excess padding)

### Pairs/Triples
- ✓ Shape match (image ↔ mask)
- ✓ Affine alignment in world space (±tolerance)
- ✓ Annotation non-empty
- ✓ Annotation contained in mask
- ✓ Valid labels (binary only: 0, 1)

## Exit Codes

- `0` — all checks pass, or issues found but `--strict` not used
- `1` — `--strict` mode and error(s) found
- `2` — usage error (bad path, config error)

---

**Reference:** [nidataset QC module](https://github.com/GiulioRusso/Ni-Dataset#quality-control)
