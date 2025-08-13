# To-Do List Application

This is a simple to-do list application that uses 2 base images and 1 application image:

- python
- nginx
- postgres

To run the application locally, run `docker compose up --build` and access the frontend at `http://localhost:3000/`.

It uses GitHub actions to build and push images to Docker Hub, scan the images with Grype, and generate an SBOM with Syft (WIP).

On the Chainguard branch, the Dockerfiles are converted to use Chainguard images.

- Docker Hub image branch:
- Chainguard image branch: 
