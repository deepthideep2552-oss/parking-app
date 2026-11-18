#!/bin/bash
# ------------------------------------------------------------------
# build-image.sh - Build the Docker image for Parking Slot Booking System
#
# Usage:
#   ./build-image.sh                 Build image with version = date-time
#   ./build-image.sh v1.0            Build image with version v1.0
#   ./build-image.sh v1.0 --run      Build image and run the container
#
# On Windows, run this script in "Git Bash" (installed with Git).
# ------------------------------------------------------------------

set -e   # stop the script if any command fails

IMAGE_NAME="parking-app"
CONTAINER_NAME="parking-app-container"
PORT=5000
VERSION=${1:-$(date +%Y%m%d-%H%M%S)}
RUN_AFTER_BUILD=$2

echo "=============================================="
echo "  Building Docker image: $IMAGE_NAME"
echo "  Version tag          : $VERSION"
echo "=============================================="

# 1. Check that Docker is installed and running
if ! command -v docker > /dev/null 2>&1; then
    echo "ERROR: Docker is not installed. Install Docker Desktop first."
    exit 1
fi

if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running. Start Docker Desktop and try again."
    exit 1
fi

# 2. Build the image with two tags: version and latest
echo ">> Step 1: Building image..."
docker build -t "$IMAGE_NAME:$VERSION" -t "$IMAGE_NAME:latest" .

# 3. Run the automated tests inside the new image
echo ">> Step 2: Running tests inside the image..."
docker run --rm "$IMAGE_NAME:latest" python -m pytest -v

# 4. Show the created images
echo ">> Step 3: Images created:"
docker images "$IMAGE_NAME"

# 5. Optionally run the container
if [ "$RUN_AFTER_BUILD" == "--run" ]; then
    echo ">> Step 4: Starting container..."
    docker rm -f "$CONTAINER_NAME" > /dev/null 2>&1 || true
    docker run -d --name "$CONTAINER_NAME" -p "$PORT:5000" "$IMAGE_NAME:latest"
    docker ps --filter "name=$CONTAINER_NAME"
    echo "App is running at: http://localhost:$PORT"
fi

echo "=============================================="
echo "  SUCCESS: Image $IMAGE_NAME:$VERSION is ready"
echo "=============================================="
