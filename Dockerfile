FROM python:3

ENV PYTHONUNBUFFERED 1

# Set working directory
RUN mkdir /opt/code
WORKDIR /opt/code

# Copy requirements and install
COPY requirements /opt/requirements
RUN pip install -r /opt/requirements/prod.txt

# Copy the rest of the application code
COPY . /opt/code
