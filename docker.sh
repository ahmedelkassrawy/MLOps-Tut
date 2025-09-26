#!/bin/bash
# Convenience wrapper for Docker deployment
# This allows running ./docker.sh from project root

exec ./src/docker/deploy.sh "$@"