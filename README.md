# Containerizing-Jupyter-Notebooks
This repository is a simple example of packaging Jupyter Notebooks and its required environment in a container to allow users to run them locally (without having a Python/Jupyter environment installed).

Jupyter Notebooks are an open-source tool that enable data analysts and scientists to create documents that integrate executable codes, widgets, modules, formulas, and visualizations. Along with these features, Jupyter Notebooks allows for the addition of textual narratives. These narratives explain the content in a way that the document itself tells a comprehensive story. With Jupyter supporting over 40 programming languages, including Python, R, Julia, and Scala, task specific packages can be easily included in each notebook to support data acquisition, cleansing and normalization, analysis, visualization, and machine learning. With its impressive set of capabilities, Jupyter Notebooks have become ubiquitous within the data science community, but not beyond that. Why? As great as Jupyter is, it can be burdensome when it comes to sharing your work and collaborating with executives and non-data scientists.  Although Jupyter notebooks allow you to interactively experiment with different scenarios and/or present a story and allows business professionals to change pieces of the narrative to see what happens, it requires some degree of setup. Unfortunately, this setup bars many business professionals and executives use them.

Containerization provides a way to deliver the analysis benefits of notebooks to non-technical audiences leaving the setup with the developer of the core code. Docker containers are an excellent way to package up an analysis. They can include the data you need, any scripts and code, and they’re guaranteed to work on everyone’s machine—no installation required.
Docker is a set of platform-as-a-service products that uses OS-level virtualization to deliver software in packages called containers. Containers are isolated from one another and bundle their own software, libraries and configuration files; they can communicate with each other through well-defined channels.

Docker uses a special ‘Dockerfile’ that describes all steps to build an image of that environment. You can then deploy that image to a Docker ‘container’, which is like a virtual computer than runs on your machine or in the cloud.

To get access to Jupyter Notebooks (or any of the many programming environments, servers, or databases that have been ‘dockerized’), we just need a Dockerfile. Jupyter has put together a collection of Dockerfiles for a variety of Jupyter notebooks and published them on Dockerhub.  This post will look at running Jupyter locally, using the DOCKER RUN command, and mounting a local directory as the source of the Jupyter Notebook. A prerequisite is that the user has Docker Desktop installed and running.

## Pre-requisites    
If you’re using Windows or Mac, you can install Docker Desktop, or if you’re using a Linux system you can install Docker using your package manager. You can find the instructions for your operating system at [Docker’s installation site](https://docs.docker.com/install).

## Directory Structure    
Before we begin, go over the directory structure.

![Directory Structure](notebooks/img/directory-structure.svg){: width="50%"}

### modules directory  
The `modules` directory is where the main Python (`*.py`) modules (code) are stored. These files do the heavy lifting and it’s what the developers spent all their time developing. This directory contains the `__init__.py` that is required to make Python treat the directory as a package. This prevents directories with a common name, such as string, unintentionally hiding valid modules that may occur later on the module search path.

### notebooks directory
The `notebooks` directory contains the Python Notebooks (`*.ipynb`) with the analysis and visualization that you want to be runnable for an audience who want to poke around. This directory also contains whatever raw data that may be required in the data folder and any images in the img directory.

### css and js directories
The `css` and `js` directories contain cascading stylesheets and JavaScript libraries, respectively, that may be used. Although Jupyter Notebooks do not natively support JavaScript, you can import Javascript into the environment and use it. This solution does just that, importing the d3, Data Driven Documents, libraries and uses it to build D3 dynamic trees from dataframes constructed in the notebook.

### Files
**requirements.txt** is a fil containing a list of items to be installed using `pip` install. **pip** is the standard package manager for Python. It allows you to install and manage additional packages that are not part of the Python standard library.

**Dockerfile** is the file used to build and run the container either locally (Docker desktop) or in the cloud.


## Jupyter Docker Images
The diagram below shows the various Jupyter Notebook Docker images:
