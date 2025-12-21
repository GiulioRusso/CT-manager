# 🧠 CT-MANAGER

A Python tool for CT data extraction and preprocessing.

## 📲 Installation and Configuration

1. Install requirements:

```bash
pip install -r requirements.txt
```

2. Edit configuration files in `configs/` with your dataset paths:
   - `parameters.yaml` - Set task, dataset, and output folder
   - `paths.yaml` - Define paths to your data

**Note:** The `example/` directory contains sample data and output examples from all tasks for reference.

## 🛠️ Usage

```bash
python3 main.py --dataset=<dataset_name> --task=<task> --output_folder=<folder_name>
```

**Example:**
```bash
python3 main.py --dataset=example --task=extract_slices --output_folder=output
```

**Available tasks:**
- `extract_slices` - Extract 2D slices from 3D images
- `extract_masks` - Extract 2D slices from 3D masks
- `extract_annotations` - Extract 2D annotations
- `debug_draw` - Visualize annotations on images
- `skulling` - Remove skull from brain CT (requires FSL)
- `registration` - Register images to MNI152 template

**Available datasets:** 
- `example`
- `TruetaHospital`
- `CODEC_IV`
- `ISLES24`

The script will:
1. Read task configuration from `configs/parameters.yaml`
2. Load dataset paths from `configs/paths.yaml`
3. Execute the specified task
4. Save results to the output folder

## ▶️ Tasks

### extract_slices
Extracts 2D slices in axial, coronal, and sagittal views from 3D NIfTI images.
- Processes entire dataset automatically
- Generates statistics for each view
- Organizes output by anatomical plane

### extract_masks
Extracts 2D slices from segmentation masks in all three anatomical views.
- Same workflow as `extract_slices` but for masks
- Preserves segmentation label values
- Organizes output by anatomical plane

### extract_annotations
Processes 3D annotations and extracts them to 2D format with spatial information.
- Converts annotations for all three views
- Includes radius and bounding box data
- Saves as CSV files per slice

### debug_draw
Overlays annotations on images for visualization and quality control.
- Draws annotations on corresponding image slices
- Useful for verifying annotation accuracy
- Configure specific files in `paths.yaml` (draw_axial_annotation, draw_axial_image, etc.)

### skulling
Removes skull from brain CT images using FSL's Brain Extraction Tool (BET).
- **Important:** Must be run from terminal (not IDE)
- **Important:** Input paths must not contain spaces
- Includes cleanup and debug options
- Requires FSL installation

### registration
Registers images to MNI152 template and applies transforms to masks and annotations.
- Performs spatial normalization to standard MNI152 space
- Applies computed transforms to masks (preserving segmentations)
- Applies transforms to annotations (preserving spatial coordinates)
- Requires MNI152 template paths configured in `paths.yaml`

## 🗂️ Output Structure

All tasks save results to the specified output folder. The `example/output/` directory contains sample outputs from each task for reference.

```
output/
├── output_slices/              # extract_slices
│   ├── axial/
│   ├── coronal/
│   ├── sagittal/
│   └── *_slices_stats.csv      # Statistics per view
├── output_masks/               # extract_masks
│   ├── axial/
│   ├── coronal/
│   ├── sagittal/
│   └── *_slices_stats.csv
├── output_annotations/         # extract_annotations
│   ├── axial/
│   ├── coronal/
│   ├── sagittal/
│   └── *_annotations_stats.csv
├── output_draw/                # debug_draw
│   └── *_annotated.png         # Visualized annotations
├── output_skulling/            # skulling
│   ├── skulled/                # Skull-stripped images
│   └── masks/                  # Brain masks
├── output_registration/        # registration (images)
│   ├── registered/             # Registered images
│   └── transforms/             # Transform matrices
├── output_registration_mask/   # registration (masks)
│   └── *_registered_mask.nii.gz
└── output_registration_ann/    # registration (annotations)
    └── *_registered_bbox.nii.gz
```

## 📑 Requirements

- Python 3.9+
- FSL (only required for skull stripping task)
- See `requirements.txt` for Python packages

**Repository includes:**
- `example/data/` - Sample CT images, masks, and annotations
- `example/output/` - Example outputs from all tasks
- `template/` - MNI152 template files for registration

## ⚠️ Troubleshooting

**Skulling task issues:**
- Run from terminal instead of IDE
- Ensure input paths contain no spaces
- Verify FSL is installed and accessible in PATH

**Registration failures:**
- Check MNI152 template paths in `paths.yaml`
- Verify input images are valid NIfTI format
- Ensure sufficient disk space for output