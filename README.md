# To-Do List Application

## What is it
This is a simple to-do list application that uses 2 base images and 1 application image:

- python
- nginx
- postgres

## How to run
To run the standard Docker application locally, run `docker compose up --build` and access the frontend at `http://localhost:3000/`.

To run the Chainguard application locally, run `docker compose -f compose-cg.yml up --build --force-recreate --no-deps`. To stop, run `docker compose down --rmi all --remove-orphans`.

## How does it work?
It uses GitHub actions to build and push images to Docker Hub, scan the images with Grype, and comments the scan results on PR action. Currently it only scans the Docker Hub base image images. Scanning the Chainguardized version is WIP.

## How do I demo this?
Visit the `demos/` folder to show how the Dockerfile converter tool was used, additional tweaks required, and scanning the Docker images vs the Chainguard images.
