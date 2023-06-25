# Use a specific version of the base image
FROM python:3.11-bullseye

# Set the working directory in the container to /api-getway
WORKDIR /api-getway

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Set up virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 5555
EXPOSE 5555

# Run the command to start your application
CMD ["python3", "App/run.py"]
