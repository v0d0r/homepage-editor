# Homepage Editor

A web-based UI for managing [Homepage](https://gethomepage.dev/) dashboard services. Homepage is an excellent self-hosted dashboard for organizing your services and applications, but editing the `services.yaml` file manually can be tedious. This tool provides a simple web interface to add, edit, and delete categories and services without touching YAML files directly.

## Features

- Web UI for managing Homepage services
- Add/edit/delete categories and services
- Preserves YAML formatting
- 3-column responsive layout
- No manual YAML editing required

## Usage

bash
docker run -d \
 -p 8080:5000 \
 -v /path/to/services.yaml:/data/settings.yaml \
 ghcr.io/v0d0r/homepage-editor:latest

Access the editor at `http://localhost:8080`
