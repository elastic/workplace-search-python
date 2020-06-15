#!/bin/bash

set -x

# Stop all stack components
docker-compose -f ./.ci/docker-compose.yml down --timeout 10
