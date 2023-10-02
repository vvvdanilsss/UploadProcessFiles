# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Install Django
RUN pip install django

# Copy the current directory contents into the container at /app
COPY . /app
