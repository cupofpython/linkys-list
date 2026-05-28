# To-Do List Application

## What is it
This is a simple to-do list application that uses 2 base images and 1 application image:

- python
- nginx
- postgres

## How to run
To run the standard Docker application locally, run `docker compose up --build` and access the frontend at `http://localhost:3000/`.

To run the Chainguard application locally, run `docker compose -f compose-cg.yml up --build --force-recreate --no-deps`. To stop, run `docker compose down --rmi all --remove-orphans`.

# Building individually
To build Chainguard backend locally, simply run `DOCKER_BUILDKIT=1 docker build --secret id=netrc,src=.netrc -f backend/Dockerfile.converted -t cg-backend:latest backend/`

## How does it work?

First, an integrity check ensures that the base images come from a trusted source. Then the images are built and pushed to GHCR, with the Chainguard backend using Python libraries pulled directly from Chainguard. These are scanned with grype. Digestabot updates image digests on a daily cadence, and dependabot runs to update the requirements.txt daily as well.

# How to verify the Chainguard libraries

Run `chainctl verify libraries verify $IMAGE_NAME`

## How do I demo this?
Visit the `demos/` folder to show how the Dockerfile converter tool was used, additional tweaks required, and scanning the Docker images vs the Chainguard images.
