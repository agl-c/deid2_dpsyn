# denote the python version
FROM python:3.9.0

# maintainer name
MAINTAINER caq caq@pku.edu.cn

# the code directory
WORKDIR /DPSyn

# add code directory into the container
ADD . /DPSyn

# install the pkgs in requiremnets.txt
RUN pip install -r requirements.txt

# entry point
ENTRYPOINT ["python", "experiment.py"]

