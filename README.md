Set-ExecutionPolicy -ExecutionPolicy Unrestricted
iwr -useb community.chocolatey.org/install.ps1 | iex
choco install mingw

Requires Python version 3.9 