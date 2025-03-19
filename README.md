# dev-academy-spring-2025-exercise

This is a submission to the pre-assignment for Solita Dev Academy Finland January 2025. The project involved creating a UI and a backend service to display data on electricity production, consumption, and prices.

The implementation utilized data provided by Fingrid, combined with electricity price data from Pörssisähkö.net. The goal was to design an intuitive and functional interface while ensuring efficient backend data handling to deliver real-time insights into the electricity market.

The project was implemented using the following technologies:
- Frontend: Vite, React, TypeScript, Material-UI, nginx (in deployment container).
- Backend: FastAPI, SQLAlchemy, Uvicorn.
- Database: PostgreSQL (provided with the assignment)

Project had live deployment (closed).

Deployment was done using Azure Container registry to Azure VM running docker swarm. CI/CD pipeline was implemented using GitHub Actions. CI/CD pipeline runs tests automatically and deploys the application with docker stack deploy.

# List of features

Since the time was limited, I focused on implementing a working deployment with a CI/CD pipeline rather than spending time polishing specific parts of the code.  Implemented features are marked with a checkmark ✔️.

## Daily statistics list (recommended features)
- Total electricity consumption per day ✔️
- Total electricity production per day ✔️
- Average electricity price per day ✔️
- Longest consecutive time in hours, when electricity price has been negative, per day ✔️

## Additional features for daily statistics list
- Pagination ✔️
- Ordering per column ✔️
- Searching ✔️
- Filtering ❌

## Other additional features
- Single day view ❌
- Graph visualisations ❌

## Surprise us with 
- Running backend in Docker ✔️
- Running backend in Cloud ✔️
- API integration tests ✔️
- Implement E2E tests ❌
- Implement CI/CD pipeline ✔️
    - Automated tests ✔️
    - Build and push container's to Azure Container Registry ✔️
    - Deployment to Azure with docker stack deploy✔️
- Most importantly dark mode ✔️

## things to improve
- Read secretish values from environment variables
- Add ordering option to mobile card view

# Instructions for running the project

Project can be run locally with docker-compose or by running the backend and frontend separately. The project can also be deployed using docker stack deploy.

prerequisite: 
- Docker with docker-compose

## Running the project with Docker locally

1. Run docker compose in the root folder with following parameters:
```bash
docker compose up --build --renew-anon-volumes -d
```
2. Open browser and navigate to http://localhost:8080

3. (Optional) Backend tests can be run with:
```bash
docker exec $(docker ps -q --filter name=backend) pytest
```

## Running the project locally for development

To enable hot-reloading for the frontend and backend, each part of the project can be run separately.

### Launch only the db container with docker-compose
Compose up only the db container with the following command:
```bash
docker compose up -d --renew-anon-volumes db
```
You can include other services like done above, for example adminer.

### Running the backend
The backend runs on python. Usign a virtual environment is recommended. Backend is developed and tested with python 3.10.12.

run all commands inside the backend folder.

example with of creating venv and activating it:
```bash
python -m venv venv
source venv/bin/activate
```

1. Install requirements
```bash
pip install -r requirements.txt
```

2. Launch the backend with uvicorn
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Running the frontend
The frontend is developed with Vite and React. Node.js is required to run the frontend.

run all commands inside the frontend folder.

1. Install dependencies
```bash
npm install
```

2. Launch the frontend development server and navigate the address shown in the terminal
```bash
npm run dev
```

## Deploying the project to cloud

### Prerequisites
- Docker and docker-compose
- ssh access to a server with docker and docker swarm (run `docker swarm init`) and server needs to have port 80 open and have a public IP address
- Azure Container Registry with public pull access



1. Build images locally
```bash
docker compose --file docker-compose.prod.yml build
```

2. Push the built images to Azure Container Registry
```bash
docker login <azure-container-registry-url>

docker push <azure-container-registry-url>/dev-academy-spring-2025-exercise-frontend:latest
... and so on 
```

3. Set up docker context to the server
```bash
docker context create \
    --docker host=ssh://<user>@<hostname/ip>\
    <name-for-context>
```

4. Activate the docker context
```bash
docker context use <name-for-context>
```

5. Deploy the stack to the server
```bash
docker stack deploy -c docker-stack.yml <stack-name>
```
