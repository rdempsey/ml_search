FROM python:3.7-slim

# Update the underlying OS
RUN apt-get update

# Install git so we can pull libs from Github
RUN apt-get -y install git

# Install the requirements
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy over the code
COPY . /usr/src/app

WORKDIR /usr/src/app/ml_search
CMD ["python", "ml_search.py"]