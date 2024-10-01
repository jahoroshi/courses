#!/bin/bash
docker ps
docker run -d -p 8001:8000 -v $(pwd):/usr/src/app ap2
