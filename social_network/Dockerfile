# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=social_network.settings

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Expose port 8000 to the outside world
EXPOSE 8000

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=social_network.settings

# Run the Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
