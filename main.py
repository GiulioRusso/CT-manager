import os

from nidataset import draw_2D_annotations, register_mask_dataset, register_annotation_dataset, mip_dataset, resampling_dataset
from nidataset.preprocessing import skull_CTA_dataset, register_CTA_dataset
from nidataset.slices import extract_slices_dataset, extract_annotations_dataset

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
        draw_2D_annotations(annotation_path=paths[parser.dataset]['draw_axial_annotation'],
                            image_path=paths[parser.dataset]['draw_axial_image'],
                            output_path=os.path.join(os.getcwd(), parser.output_folder))

        # coronal
        draw_2D_annotations(annotation_path=paths[parser.dataset]['draw_coronal_annotation'],
                            image_path=paths[parser.dataset]['draw_coronal_image'],
                            output_path=os.path.join(os.getcwd(), parser.output_folder))

        # sagittal
        draw_2D_annotations(annotation_path=paths[parser.dataset]['draw_sagittal_annotation'],
                            image_path=paths[parser.dataset]['draw_sagittal_image'],
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

    else:
        raise ValueError('Unknown task {}.'.format(parser.task))


if __name__ == '__main__':
    main()
