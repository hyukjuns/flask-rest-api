FROM python:3.9-slim

# Create non-root user and working directory
RUN useradd --create-home --shell /bin/bash python

# Setting User and Working Directory
USER python
WORKDIR /home/python

# Copy Source files
COPY requirements.txt .
COPY ./*.py .

# Install Packages
RUN pip install -r requirements.txt

# Setting PATH and DB Info
ENV PATH="/home/python/.local/bin:$PATH"

# Expression PORT
EXPOSE 8000

# Run Application
CMD [ "gunicorn", "-c", "gunicorn_config.py", "main:app" ]