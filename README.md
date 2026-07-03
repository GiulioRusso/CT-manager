<div align="center">

  <!-- headline -->
  <center><h1><img align="center" src="./doc/images/logo.png" width=150px> CT-Manager</h1></center>

</div>

End-to-end CT dataset pipeline: slice extraction, preprocessing, quality control, registration. Config-driven (`main.py`), built on [nidataset](https://github.com/GiulioRusso/Ni-Dataset).

<br><img src="./doc/images/ct-manager.png" width=100%>

## 📲 Installation and Configuration

1. Install requirements:

```bash
pip3 install -r requirements.txt
```

   Install the FSL library (only required for skull stripping task).

2. Edit configuration files in `configs/` with your parameters and dataset paths:
   - `parameters.yaml`: Set task, dataset, and output folder.
   - `paths.yaml`: Define paths to your data.

## 🛠️ Usage

Configure your dataset and task in `configs/`, then run:

```bash
python3 main.py --dataset=<name> --task=<task> --output_folder=<dir>
```

Edit `configs/parameters.yaml` to set task and dataset, `configs/paths.yaml` for data paths. Available tasks: `extract_slices`, `extract_masks`, `extract_annotations`, `debug_draw`, `skulling` (requires FSL), `registration`, `mip`, `resampling`, `qc_check` (single-volume validation), `qc_dataset` (folder validation + outliers). Full reference in [`configs/parameters.yaml`](configs/parameters.yaml). QC details in [`example/QC_EXAMPLES.md`](example/QC_EXAMPLES.md).

## ⚠️ Troubleshooting

- **Skulling:** Run from terminal (not IDE), no spaces in paths, FSL in PATH.
- **Registration:** Check template paths in `paths.yaml`, verify NIfTI validity, ensure disk space.
- **QC:** Use folder of NIfTI files or CSV manifest (`image,mask[,annotation]`). Reports in `output_folder/qc_*.json`.