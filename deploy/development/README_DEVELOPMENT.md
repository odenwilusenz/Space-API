Development notes
-----------------

This folder contains the basics to develop and test locally.

Usage:

1. Create a virtualenv and install dependencies (Makefile helper provided):
   ```bash
   cd project-root
   make -C deploy/development install
   ```

2. Run the app locally with debug enabled:
   ```bash
   make -C deploy/development run
   ```

3. Run tests:
   ```bash
   make -C deploy/development test
   ```

Notes:
- The Makefile creates `.venv` in the repo root for convenience. You can remove it with `make -C deploy/development clean`.
- Use `.env.dev.example` as a basis for local environment variables.
