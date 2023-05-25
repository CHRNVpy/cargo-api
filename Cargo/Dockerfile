FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install cron and your project dependencies
RUN apt-get update && apt-get install -y cron
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /code

# Add the cron job file to the crontab
RUN crontab /code/crontab
RUN chmod 0644 crontab

# Run the command on container startup
CMD ["bash", "-c", "python manage.py runserver 0.0.0.0:8000"]
