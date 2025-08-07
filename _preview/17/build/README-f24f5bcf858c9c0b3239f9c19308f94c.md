# MPAS+JEDI Cookbook

<img src="thumbnail.png" alt="thumbnail" width="300"/>

[![nightly-build](https://github.com/ProjectPythia/cookbook-template/actions/workflows/nightly-build.yaml/badge.svg)](https://github.com/ProjectPythia/cookbook-template/actions/workflows/nightly-build.yaml)
[![Binder](https://binder.projectpythia.org/badge_logo.svg)](https://binder.projectpythia.org/v2/gh/ProjectPythia/cookbook-template/main?labpath=notebooks)
[![DOI](https://zenodo.org/badge/475509405.svg)](https://zenodo.org/badge/latestdoi/475509405)

This Project Pythia Cookbook focuses on analyzing, visualizing, and understanding output from the MPAS model and the JEDI system on an unstructured grid, as well as evaluating data assimilation performance in observation space.

## Motivation

[NOAA](https://www.noaa.gov/)'s next generation Rapid Refresh Forecast System (RRFS) is built on the MPAS (Model for Prediction Accross Scals) Model and the JEDI (Joint Effort for Data assimilation Integration) system. While both MPAS and JEDI are powerful tools, they can also be complex to use and interpret. This cookbook will demonstrate how to explore MPAS forecasts and JEDI analyses directly on the unstructed grid using the UXARRAY (https://github.com/UXARRAY/uxarray) package. It also includes examples for examining JEDI analyses in observation space.

## Authors

[Guoqing Ge](https://github.com/guoqing-noaa), [Orhan Eroglu](https://github.com/erogluorhan), etc.    
_(Acknowledge primary content authors here)_

### Contributors

<a href="https://github.com/ProjectPythia/mpas-jedi-cookbook/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ProjectPythia/mpas-jedi-cookbook" />
</a>

## Structure

(State one or more sections that will comprise the notebook. E.g., _This cookbook is broken up into two main sections - "Foundations" and "Example Workflows."_ Then, describe each section below.)

### Section 1 ( Replace with the title of this section, e.g. "Foundations" )

(Add content for this section, e.g., "The foundational content includes ... ")

### Section 2 ( Replace with the title of this section, e.g. "Example workflows" )

(Add content for this section, e.g., "Example workflows include ... ")

## Running the Notebooks

You can either run the notebook using [Binder](https://binder.projectpythia.org/) or on your local machine.

### Running on Binder

The simplest way to interact with a Jupyter Notebook is through [Binder](https://binder.projectpythia.org/), which enables the execution of a [Jupyter Book](https://jupyterbook.org) in the cloud.   
All you need to know is how to launch a Pythia Cookbooks chapter via Binder. Simply navigate your mouse to the top right corner of the book chapter you are viewing and click on the rocket ship icon, (see figure below), and be sure to select “launch Binder”. After a moment you should be presented with a notebook that you can interact with. I.e. you’ll be able to execute and even change the example programs. You’ll see that the code cells have no output at first, until you execute them by pressing {kbd}`Shift`\+{kbd}`Enter`. Complete details on how to interact with a live Jupyter notebook are described in [Getting Started with Jupyter](https://foundations.projectpythia.org/foundations/getting-started-jupyter.html).

Note, not all Cookbook chapters are executable. If you do not see the rocket ship icon, such as on this page, you are not viewing an executable book chapter.

### Running on Your Own Machine

If you are interested in running this material locally on your computer, you will need to follow this workflow:

1. Clone the `https://github.com/ProjectPythia/mpas-jedi-cookbook` repository:

   ```bash
    git clone https://github.com/ProjectPythia/mpas-jedi-cookbook
   ```

1. Move into the `mpas-jedi-cookbook` directory
   ```bash
   cd mpas-jedi-cookbook
   ```
1. Create and activate your conda environment from the `environment.yml` file
   ```bash
   conda env create -f environment.yml
   conda activate mpas-jedi-cookbook
   ```
1. Move into the `notebooks` directory and start up Jupyterlab
   ```bash
   cd notebooks/
   jupyter lab
   ```
