#!/bin/bash

# Source the .env file from the parent directory to load the credentials
source "./.env"

# Set the base directory
base_dir="$(dirname "$(dirname "$0")")/Services"

echo $base_dir

# List of Docker image directories
IMAGE_DIRECTORIES=(
  "/0-api-getway"
  "/1-doctor-service"
  "/2-doctor-verification-service"
  "/3-user-service"
  "/4-monitoring-service"
  "/5-symptom-analysis-service"
)

# Login to Docker Hub
echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

# Iterate over the image directories and build/push Docker images
for directory in "${IMAGE_DIRECTORIES[@]}"; do
  echo "Building Docker image in directory: $directory"

  # Get the image name from the directory name
  image_name=$(basename "$directory")

  # Build the Docker image
  docker build -t "$DOCKERHUB_USERNAME/$image_name" "$base_dir/$directory"

  # Push the Docker image to Docker Hub
  docker push "$DOCKERHUB_USERNAME/$image_name"
done

# Logout from Docker Hub
docker logout
