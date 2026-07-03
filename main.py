import os

from nidataset import draw_2D_annotations, register_mask_dataset, register_annotation_dataset, mip_dataset, resampling_dataset
from nidataset.preprocessing import skull_CTA_dataset, register_CTA_dataset
from nidataset.slices import extract_slices_dataset, extract_annotations_dataset
from nidataset.qc import check_dataset, check_volume, to_json
import json

from net.initialization.get_yaml import get_yaml
from net.parameters.parameters import parameters_parsing


def main():
    """
        ==============
        | CT-MANAGER |
        ==============

        Manage CT data extraction and preprocessing.
    """

    # ============== #
    # INITIALIZATION #
    # ============== #
    # parameters
    parser = parameters_parsing(parameters_path=os.path.join(os.getcwd(), "configs", "parameters.yaml"))

    # paths
    paths = get_yaml(os.path.join(os.getcwd(), "configs", "paths.yaml"))

    # create output folder
    os.makedirs(os.path.join(os.getcwd(), parser.output_folder), exist_ok=True)

    # ==== #
    # TASK #
    # ==== #
    if parser.task == 'extract_slices':

        # axial
        extract_slices_dataset(nii_folder=paths[parser.dataset]['images'],
                               output_path=os.path.join(os.getcwd(), parser.output_folder),
                               view='axial',
                               saving_mode='view',
                               save_stats=True)

        # coronal
        extract_slices_dataset(nii_folder=paths[parser.dataset]['images'],
                               output_path=os.path.join(os.getcwd(), parser.output_folder),
                               view='coronal',
                               saving_mode='view',
                               save_stats=True)

        # sagittal
        extract_slices_dataset(nii_folder=paths[parser.dataset]['images'],
                               output_path=os.path.join(os.getcwd(), parser.output_folder),
                               view='sagittal',
                               saving_mode='view',
                               save_stats=True)

    elif parser.task == 'extract_masks':

        # axial
        extract_slices_dataset(nii_folder=paths[parser.dataset]['masks'],
                               output_path=os.path.join(os.getcwd(), parser.output_folder),
                               view='axial',
                               saving_mode='view',
                               save_stats=True)

        # coronal
        extract_slices_dataset(nii_folder=paths[parser.dataset]['masks'],
                               output_path=os.path.join(os.getcwd(), parser.output_folder),
                               view='coronal',
                               saving_mode='view',
                               save_stats=True)

        # sagittal
        extract_slices_dataset(nii_folder=paths[parser.dataset]['masks'],
                               output_path=os.path.join(os.getcwd(), parser.output_folder),
                               view='sagittal',
                               saving_mode='view',
                               save_stats=True)

    elif parser.task == 'extract_annotations':

        # axial
        extract_annotations_dataset(nii_folder=paths[parser.dataset]['annotations'],
                                    output_path=os.path.join(os.getcwd(), parser.output_folder),
                                    view='axial',
                                    saving_mode='view',
                                    data_mode='radius',
                                    save_stats=True)

        # coronal
        extract_annotations_dataset(nii_folder=paths[parser.dataset]['annotations'],
                                    output_path=os.path.join(os.getcwd(), parser.output_folder),
                                    view='coronal',
                                    saving_mode='view',
                                    data_mode='radius',
                                    save_stats=True)

        # sagittal
        extract_annotations_dataset(nii_folder=paths[parser.dataset]['annotations'],
                                    output_path=os.path.join(os.getcwd(), parser.output_folder),
                                    view='sagittal',
                                    saving_mode='view',
                                    data_mode='radius',
                                    save_stats=True)

    elif parser.task == 'debug_draw':

        # axial
        draw_2D_annotations(annotation_path=paths[parser.dataset]['axial_annotation'],
                            image_path=paths[parser.dataset]['axial_image'],
                            output_path=os.path.join(os.getcwd(), parser.output_folder))

        # coronal
        draw_2D_annotations(annotation_path=paths[parser.dataset]['coronal_annotation'],
                            image_path=paths[parser.dataset]['coronal_image'],
                            output_path=os.path.join(os.getcwd(), parser.output_folder))

        # sagittal
        draw_2D_annotations(annotation_path=paths[parser.dataset]['sagittal_annotation'],
                            image_path=paths[parser.dataset]['sagittal_image'],
                            output_path=os.path.join(os.getcwd(), parser.output_folder))

    elif parser.task == 'skulling':

        print("NOTE: Remember to launch skulling task from terminal, not from IDE.")
        print("NOTE: In case of exist status 1 from bet, consider to check the path to the input image. It has to be without spaces.")

        skull_CTA_dataset(nii_folder=paths[parser.dataset]['images_skulling'],
                          output_path=os.path.join(os.getcwd(), parser.output_folder),
                          saving_mode='folder',
                          cleanup=True,
                          debug=True)

    elif parser.task == 'registration':

        # registration
        register_CTA_dataset(nii_folder=paths[parser.dataset]['images'],
                             mask_folder=paths[parser.dataset]['masks'],
                             template_path=paths['template']['MNI152']['brain'],
                             template_mask_path=paths['template']['MNI152']['mask'],
                             output_path=os.path.join(os.getcwd(), parser.output_folder),
                             saving_mode="folder")

        print("NOTE: define the transforms and registered path after the call of `register_CTA_dataset` and before launching `register_mask_dataset`.")

        # registration applied to masks
        register_mask_dataset(mask_folder=paths[parser.dataset]['masks'],
                              transform_folder=paths[parser.dataset]['transforms'],
                              registered_folder=paths[parser.dataset]['registered'],
                              output_path=os.path.join(os.getcwd(), parser.output_folder),
                              saving_mode="folder")

        print("NOTE: define the transforms and registered path after the call of `register_CTA_dataset` and before launching `register_annotation_dataset`.")

        # registration applied to annotations
        register_annotation_dataset(annotation_folder=paths[parser.dataset]['annotations'],
                                    transform_folder=paths[parser.dataset]['transforms'],
                                    registered_folder=paths[parser.dataset]['registered'],
                                    output_path=os.path.join(os.getcwd(), parser.output_folder),
                                    recalculate_bbox=False,
                                    saving_mode="folder")

    elif parser.task == 'mip':

        mip_dataset(nii_folder=paths[parser.dataset]['images'],
                    output_path=os.path.join(os.getcwd(), parser.output_folder),
                    view="axial",
                    saving_mode='view',
                    window_size=10,
                    debug=True)

    elif parser.task == 'resampling':

        resampling_dataset(nii_folder=paths[parser.dataset]['images'],
                           output_path=os.path.join(os.getcwd(), parser.output_folder),
                           desired_volume=(224, 224, 128),
                           saving_mode='folder',
                           debug=True)

    elif parser.task == 'qc_check':

        # Run QC on a single image volume
        report = check_volume(paths[parser.dataset]['images'])

        # Save JSON report
        report_path = os.path.join(os.getcwd(), parser.output_folder, "qc_report.json")
        with open(report_path, 'w') as f:
            f.write(to_json(report))

        print(f"QC report saved to {report_path}")
        print(f"Status: {report.status} ({report.counts()})")

    elif parser.task == 'qc_dataset':

        # Run QC over entire dataset folder or CSV manifest
        dataset_path = paths[parser.dataset]['images']
        ds_report = check_dataset(dataset_path)

        # Save JSON report
        report_path = os.path.join(os.getcwd(), parser.output_folder, "qc_dataset_report.json")
        with open(report_path, 'w') as f:
            f.write(to_json(ds_report))

        # Print summary
        print(f"\nDataset QC: {len(ds_report.items)} items")
        print(f"Status: {ds_report.status}")
        print(f"Summary: {ds_report.counts()}")

        # Print distributions
        if ds_report.distributions:
            print("\nDistributions:")
            for key in ("orientation", "spacing", "dtype"):
                if key in ds_report.distributions:
                    print(f"  {key}: {ds_report.distributions[key]}")

            outliers = ds_report.distributions.get("outliers", {})
            for key, paths_list in outliers.items():
                if paths_list:
                    print(f"  {key} outliers: {paths_list}")

        print(f"\nFull report saved to {report_path}")

    else:
        raise ValueError('Unknown task {}.'.format(parser.task))


if __name__ == '__main__':
    main()
