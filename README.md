# Flask App

A simple Python REST API used as the target application for the [jenkins-cicd](https://github.com/MrSfaxiano/jenkins-cicd) pipeline project. Demonstrates a fully automated CI/CD workflow from push to deployment.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/<id>` | Get task by ID |
| GET | `/tasks/done` | List completed tasks |

## Pipeline

Every push to `master` triggers the full Jenkins pipeline:

```
Checkout → Lint → Test → Build → Scan → Push → Deploy
```

| Stage | Tool | Gate |
|---|---|---|
| Lint | flake8 | Fails on PEP8 violations |
| Test | pytest | Fails if coverage < 70% |
| Build | Docker | Builds image tagged with commit SHA |
| Scan | Trivy | Reports HIGH/CRITICAL CVEs |
| Push | Docker Hub | Pushes to mrsfaxiano/flask-app |
| Deploy | Docker | Runs on jenkins-cicd_cicd network |

## Local Development

```bash
# Install dependencies
pip install -r requirements-dev.txt

# Run linter
python -m flake8 app/

# Run tests with coverage
python -m pytest tests/ -v --cov=app --cov-fail-under=70

# Run the app
python -m app.main
```

## Docker

```bash
# Build
docker build -t flask-app .

# Run
docker run -p 5000:5000 flask-app

# Test
curl http://localhost:5000/health
```

## CI Image

A pre-built CI image (`flask-ci:latest`) is used by Jenkins for lint and test stages to avoid runtime pip installs:

```bash
docker build --network host -t flask-ci:latest -f Dockerfile.ci .
```

## Infrastructure

See [jenkins-cicd](https://github.com/MrSfaxiano/jenkins-cicd) for the full pipeline infrastructure.
