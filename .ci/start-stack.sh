#!/bin/bash

set -x

# Start stack components
docker-compose -f ./.ci/docker-compose.yml up --detach elasticsearch enterprise-search

# Wait until the product is up and running
set +x
echo -n 'Waiting for the stack to start (may take a while) .'
until curl --silent --output /dev/null --max-time 1 http://localhost:8080/swiftype-app-version; do
    sleep 3;
    echo -n '.';
done

echo ''
