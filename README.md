# One-click cloud deployment

This package is prepared for Render using Docker and `render.yaml`.
Render can deploy from GitHub and provides a public `onrender.com` URL. See:
https://render.com/docs/web-services

## Tablet-only deployment

1. Create a GitHub account on your tablet.
2. Create a new repository named `agri-intelligence`.
3. Upload the contents of this folder to the repository.
4. Open Render and connect GitHub.
5. Create a Web Service from `agri-intelligence`.
6. Render detects the Dockerfile and deploys it.
7. Open the generated HTTPS URL on the tablet.

The app listens on the `PORT` environment variable and has `/health`.

## Alternative
Railway can also deploy directly from a GitHub repository and automatically use a Dockerfile.
