# dockerfile-requirements
Inlining requirements.txt files into Dockerfiles for better caching

## What does this do?
Dockerfile-requirements gives you an easy way to inline `requirements.txt` requirements into a `Dockerfile` without manually having to keep the two in sync. This allows you to avoid the pain of cache invalidation and having to reinstall all your project's dependencies every time you add to or update your `requirements.txt`.

## Installation
```bash
pip install dockerfile-requirements
```

## Usage
<!-- First, prepare a `Dockerfile` like so: -->
First, prepare a `Dockerfile.template` file like so:

```dockerfile
FROM python:latest

{{ add_requirements('requirements.txt') }}
# These two lines will become redundant:
ADD requirements.txt /tmp/requirements.txt
RUN pip install -U -r /tmp/requirements.txt

ADD . /code
WORKDIR /code
VOLUME /code
EXPOSE 5000
```

And a `requirements.txt` a la:
```
mlflow
scikit-learn
pandas
matplotlib
seaborn
statsmodels
keras
tensorflow
```


Then, you can simply run:
<!--
```bash
docker build -t my-image-name -f <(dockerfile-requirements Dockerfile) .
```

Or, if you prefer, name the `Dockerfile` above as `Dockerfile.template`, and execute:
-->
```
dockerfile-requirements Dockerfile.template > Dockerfile
docker build -t my-image-name .
```

The `Dockerfile` generated will look like:
```dockerfile
FROM python:latest

# Requirements populated from requirements.txt
RUN pip install matplotlib
RUN pip install mlflow
RUN pip install pandas
RUN pip install seaborn
RUN pip install statsmodels
RUN pip install keras
RUN pip install tensorflow
RUN pip install scikit-learn

# These two lines will become redundant:
ADD requirements.txt /tmp/requirements.txt
RUN pip install -U -r /tmp/requirements.txt

ADD . /code
WORKDIR /code
VOLUME /code
EXPOSE 5000
```

with your requirements sorted by git authorship datetime, from oldest to newest. This helps retain as many intermediary layers as possible during the image build process, which can make things significantly faster in comparison to a simple `ADD` and `RUN pip install -r`, especially if you're just adding a new dependency.

## Known issues
- `dockerfile-requirements` does not support comments in `requirements.txt` (yet)

## Contacts

* Name: [H. Chase Stevens](http://www.chasestevens.com)
* Twitter: [@hchasestevens](https://twitter.com/hchasestevens)
