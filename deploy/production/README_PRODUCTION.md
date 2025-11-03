Production deployment notes
--------------------------

This folder contains sample artifacts to deploy the Odenwilusenz SpaceAPI in production.

Files and purpose:

- `Dockerfile` - Container image to run the app with Gunicorn.
- `docker-compose.yml` - Convenience compose file mapping port 5000 and mounting `api.json`.
- `Procfile` - For Heroku-like PaaS.
- `gunicorn.conf.py` - Gunicorn configuration.
- `systemd/spaceapi.service` - Example systemd unit for server deployments.
- `.env.example` - Environment example (API_TOKEN, PORT).

Instructions (containerized):

1. Build image:
   ```bash
   docker compose -f deploy/production/docker-compose.yml build
   ```
2. Run:
   ```bash
   docker compose -f deploy/production/docker-compose.yml up -d
   ```

Non-containerized (systemd):

1. Install gunicorn in system Python or virtualenv.
2. Copy the `spaceapi.service` file to `/etc/systemd/system/` and update paths/user.
3. Set `API_TOKEN` in the environment or a secure location.
4. Start the service: `systemctl daemon-reload && systemctl enable --now spaceapi`
