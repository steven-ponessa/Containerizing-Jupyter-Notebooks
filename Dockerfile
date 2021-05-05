FROM jupyter/datascience-notebook:latest

#LABEL steve ponessa <ponessa@us.ibm.com>

# This prevents Python from writing out pyc files
ENV JUPYTER_TOKEN jupyter_notebook_token
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

# install system dependencies
#RUN apt-get update \
#    && apt-get -y install gcc make \
#    && rm -rf /var/lib/apt/lists/*

#RUN python3 -m venv env
#RUN . env/bin/activate

# install dependencies
RUN pip install --no-cache-dir --upgrade pip

# set work directory
ENV WORKINGDIR = /src/app
#WORKDIR $WORKINGDIR
WORKDIR /src/app

# copy requirements.txt
COPY ./requirements.txt /src/app/requirements.txt

# install project requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .


USER root

#Set the permission on the Jupyter directory that stores the security token and the `notebooks` directory
#  that a number of notebooks wrote to. Here image is being built by the root.
RUN chmod -R a+rwx /home/jovyan
RUN chmod -R a+rwx notebooks

EXPOSE 8888

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0",  "--allow-root"]
