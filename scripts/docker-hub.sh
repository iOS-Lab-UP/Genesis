#!/bin/bash

# Source the .env file from the parent directory to load the credentials
source "../.env"

# List of Docker image directories
IMAGE_DIRECTORIES=(
  "Services/0-api-getway"
  "Services/1-doctor-service"
  "Services/2-doctor-verification-service"
  "Services/3-user-service"
  "Services/4-monitoring-service"
  "Services/5-symptom-analysis-service"
)

# Iterate over the image directories and build/push Docker images
for directory in "${IMAGE_DIRECTORIES[@]}"; do
  echo "Building Docker image in directory: $directory"

  # Get the image name from the directory name
  image_name=$(basename "$directory")

  # Build the Docker image
  docker build -t "$username/$image_name" "$directory"

  # Login to Docker Hub
  echo "$dockerhub-password" | docker login -u "$dockerhub-username" --password-stdin

  # Push the Docker image to Docker Hub
  docker push "$username/$image_name"

  # Logout from Docker Hub
  docker logout
done
