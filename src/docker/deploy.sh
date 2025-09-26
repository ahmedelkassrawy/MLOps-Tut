#!/bin/bash

# Build and run script for MLOps API (run from project root)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}MLOps Water Potability API - Build & Deploy Script${NC}"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "model.pkl" ] || [ ! -f "requirements.txt" ]; then
    echo -e "${RED}Error: Please run this script from the project root directory!${NC}"
    echo -e "${YELLOW}Current directory: $(pwd)${NC}"
    echo -e "${YELLOW}Expected files: model.pkl, requirements.txt${NC}"
    exit 1
fi

# Function to build Docker image
build_image() {
    echo -e "${GREEN}Building Docker image...${NC}"
    docker build -f src/docker/Dockerfile -t mlops-water-api:latest .
    echo -e "${GREEN}Docker image built successfully!${NC}"
}

# Function to run with Docker
run_docker() {
    echo -e "${GREEN}Starting container...${NC}"
    docker run -d \
        --name mlops-water-api \
        -p 8000:8000 \
        --rm \
        mlops-water-api:latest
    
    echo -e "${GREEN}Container started!${NC}"
    echo "API available at: http://localhost:8000"
    echo "API docs: http://localhost:8000/docs"
    echo "Health check: http://localhost:8000/health"
}

# Function to run with docker-compose
run_compose() {
    echo -e "${GREEN}Starting services with docker-compose...${NC}"
    docker-compose -f src/docker/docker-compose.yml up -d
    
    echo -e "${GREEN}Services started!${NC}"
    echo "API available at: http://localhost:8000"
    echo "MLflow UI: http://localhost:5000"
}

# Function to stop containers
stop_containers() {
    echo -e "${YELLOW}Stopping containers...${NC}"
    docker stop mlops-water-api 2>/dev/null || true
    docker-compose -f src/docker/docker-compose.yml down 2>/dev/null || true
    echo -e "${GREEN}Containers stopped!${NC}"
}

# Function to show logs
show_logs() {
    docker logs -f mlops-water-api
}

# Parse command line arguments
case "${1:-help}" in
    "build")
        build_image
        ;;
    "run")
        build_image
        stop_containers
        run_docker
        ;;
    "compose")
        build_image
        stop_containers
        run_compose
        ;;
    "stop")
        stop_containers
        ;;
    "logs")
        show_logs
        ;;
    "restart")
        stop_containers
        build_image
        run_docker
        ;;
    "help"|*)
        echo "Usage: $0 {build|run|compose|stop|logs|restart|help}"
        echo ""
        echo "Commands:"
        echo "  build    - Build Docker image"
        echo "  run      - Build and run single container"
        echo "  compose  - Build and run with docker-compose (includes MLflow)"
        echo "  stop     - Stop all containers"
        echo "  logs     - Show container logs"
        echo "  restart  - Stop, rebuild, and restart"
        echo "  help     - Show this help message"
        echo ""
        echo "Note: Run this script from the project root directory!"
        ;;
esac