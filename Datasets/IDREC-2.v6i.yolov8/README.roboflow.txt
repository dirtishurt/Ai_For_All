
IDREC-2 - v6 2024-04-07 7:22am
==============================

This dataset was exported via roboflow.com on April 7, 2024 at 12:25 PM GMT

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand and search unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

For state of the art Computer Vision training notebooks you can use with this dataset,
visit https://github.com/roboflow/notebooks

To find over 100k other datasets and pre-trained models, visit https://universe.roboflow.com

The dataset includes 1248 images.
People are annotated in YOLOv8 format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 640x640 (Fill (with center crop))
* Auto-contrast via contrast stretching

The following augmentation was applied to create 7 versions of each source image:
* Random rotation of between -9 and +9 degrees
* Random shear of between -10° to +10° horizontally and -10° to +10° vertically
* Salt and pepper noise was applied to 0.77 percent of pixels

The following transformations were applied to the bounding boxes of each image:
* Random exposure adjustment of between -10 and +10 percent


