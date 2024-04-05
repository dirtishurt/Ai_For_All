Set-ExecutionPolicy -ExecutionPolicy Unrestricted
iwr -useb community.chocolatey.org/install.ps1 | iex
choco install mingw

**Requires Python 3.11 or Earlier**
------------
If you are training a dataset, and you need a gpu first install Conda.

Run:
>conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
>conda install -c conda-forge charset-normalizer
