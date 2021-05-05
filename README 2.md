# Jupyter-Notebook
Repository for executable Jupyter Notebooks

**Table of contents**
1. [Overview](#1.0)
1. [Pre-requisites](#2.0)
1. [Run Jupyter Notebook in a container](#3.0)

<a id="1.0"></a>

## Overview

[Jupyter](https://jupyter.org/) Notebooks gives users a quick and easy way to get an interactive programming environments for data science languages like Python and R, and has been extended to run code in a number of other languages (Java, C#, Ruby, Javascript, etc).
 
Jupyter lets you create notebooks that can mix sections of interactive, editable code blocks with plain text or markdown. This is great for creating interactive stories as you work with data.

[Docker](https://www.docker.com/)  is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers. Containers are isolated from one another and bundle their own software, libraries and configuration files; they can communicate with each other through well-defined channels.

Docker uses a special ‘Dockerfile’ that describes all steps to create the environment to build an image of that environment. You can then deploy that image to a Docker ‘container’, which  is like a virtual computer than runs on your machine or in the cloud.

Once you have a 'Dockerfile', anyone can build and access an exact copy of that environment, meaning environments can easily be shared, maintained, and version controlled. 

To get access to Jupyter Notebooks (or any of the many programming environments, servers, or databases that have been ‘dockerized’), we just need a Dockerfile for it. Jupyter have put together a  collection of Dockerfiles for a variety of Jupyter notebooks and pushed them to Dockerhub. 

<a id="2.0"></a>

## Pre-requisites

**Docker**

First things first, we’ll need to get Docker set up to access all these powerful features. If you’re using Windows or Mac, you can install Docker Desktop, or if you’re using a Linux system you can install Docker using your package manager. Find the instructions for your operating system at [Docker's intallation site]( https://docs.docker.com/install).


<center>
<img src="img/docker.svg" alt="Docker Icon" width="30%"/>
</center>


<a id="3.0"></a>

## Run Jupyter Notebook in a container

Once you have Docker on your computer, you can pull the image for the Jupyter notebook environment you prefer using the command line tool. Open your terminal then build a datascience environment that will allow us to run code in Python, Julia, or R.

First we’ll download the files required to build the image with the following command:

```
docker pull jupyter/datascience-notebook:latest
```

Then we can build our environment and deploy it to a Docker container with:

```
docker run -d -p 8888:8888 --name jupyter-container --env JUPYTER_TOKEN=jupyter_notebook_token --volume ~/github-ibm/cao/:/home/jovyan/work jupyter/datascience-notebook:latest
```
or
```
docker run -d -p 8888:8888 --name jupyter-container \
   --env JUPYTER_TOKEN=jupyter_notebook_token \
   --volume ~/github-ibm/cao/:/home/jovyan/work \
   jupyter/datascience-notebook:latest
```

To make things easier, we have set and environment variable, with the `–env` flag, for the token Jupyter notebooks should use for login.  We'll use this later. Also, because we’re specifying the token ourselves, we don’t need to see the console output (to copy and paste the token), so we also add the `-d` flag to run the container in detached mode in the background. To see the output from the container, we can just use `docker logs jupyter-container` or just look at the logs in Docker Desktop.

We are using the `-p` flag to tell docker to connect port 8888 of the computer to port 8888 on the container.  This allows us to connect to the Jupyter notebook server inside the container. We also use the `–name` flag to give us a convenient name for referring to this container in later commands. After you run this command, it will show you the url for connecting to the notebook server, and give you a token for logging in. Open a new browser window and go the url to test it out.

**Running existing Jupyter Notebooks in the container**  
This command also mounts a working folder as a volume in our container to hold new or existing notebooks as we’re working on them. This lets us read and save our notebooks locally, while still being able to access them in our container.  Using the `--volume` parameter, this example mounts the local Jupyter Notebook folder (downloaded from GitHub, `~/github-ibm/cao/`) to the default notebook location (`/home/jovyan/work`).

Now we can log into Jupyter notebook with the token we specified in our environment variable:

```
http://localhost:8888/?token=jupyter_notebook_token
```
