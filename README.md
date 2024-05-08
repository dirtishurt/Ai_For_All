# Table of Contents:
<!-- TOC -->
* [Application Based Issues](#application-based-issues)
  * [How to use the Program](#how-to-use-the-program)
    * [Adding a Label to an Image](#adding-a-label-to-an-image)
    * [Creating A Dataset](#creating-a-dataset)
    * [Training a model](#training-a-model)
      * [Adjusting Settings](#adjusting-settings)
* [Training Issues:](#training-issues)
<!-- TOC -->







# Application Based Issues

**Requires Python 3.11 or Earlier if you are not using a GPU**

<p>
If nothing is working at all, you probably forgot to set a project directory. To do that click 'Set Project Directory'
on either the initial window, or the annotation window.
</p>

## How to use the Program

<p>
The application starts on the Main Window, if you are simply seeking to create a model from scratch you first need
to hit 'Create Model &rAarr; Open Annotation Window'. From there you can click 'Add Images' and select one of the 
options. Note: hitting 'Select Folder' will remove all currently loaded files, this is intentional, it will not
remove them from the dataset, to reload those images just reload the directory.
</p>

### Adding a Label to an Image


<p>
You may have noticed the toolbar on the left side of the Annotation Window, and you may have also noticed that
the polygon tool is selected by default, that and the bounding box tool are the two annotation modes currently supported.
Clicking a different mode than the currently selected won't cause issues when using the yolov8n-seg.pt model during
training, but it might when using yolov8n.pt.
</p>

### Creating A Dataset
<p>So, you're ready to create a dataset. Simply hit 'Create Training Set' and it will work it's magic. You can then
safely close the Annotation Window.</p>
<p>As a side note, I'm working on getting image generation / image modification working, for better results.</p>

### Training a model
<p>To begin the process hit, 'Create Model &rAarr; Train Model'</p> 

#### Adjusting Settings and Selecting a model
<p>Some of these can be confusing, for a more detailed explanation please go to 
<a href=https://docs.ultralytics.com/models/yolov8/#supported-tasks-and-mode>Ultralytics.com</a></p>


* Epochs
  * The amount of training iterations, i.e. the more of these, generally the better the accuracy.
* Patience
  * The maximum amount of epochs without improvement, setting this value to 0 disables this.

##### Models
* yolov8n
  * The quickest, works only with bounding box detection
* yolov8n-cls
  * The simplest, assigns a class to the whole image
  * By default, if you have no annotations drawn when changing images, it will just write the currently selected class to the image's label file
* yolov8n-seg
  * A more accurate model, only truly compatible with the polygon tool, takes longer to train than yolov8n
* yolov8s-seg
  * Like the previous one, just better. Takes even longer to train

***
# Training Issues

<p>Training with a GPU is Nvidia only, there just is not enough support for AMD cards at the moment.</p>
<p>If you are training a dataset, and you want to use a gpu first install Conda 3.10.</p>
<p>Once Conda is set as the interpreter run:</p>

>conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

>conda install -c conda-forge charset-normalizer

<p>If you are having issues with getting the training to use the GPU, especially if you are on a laptop, make
sure that the GPU is enabled when the program/program interpreter is run. Also make sure your laptop is plugged in, 
in some cases the GPU will not run if it is not. See the figure below</p>

<figure>
    <img src="img.png" width="714" height="570"
        alt="Set High Performance Mode in Windows"
    >
</figure>



