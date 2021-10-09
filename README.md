# mlflow-docker

This repo configures an MLflow tracking server + Minio artifact store as Docker containers, organized with `docker-compose`. Use this repo for standalone experiment tracking for multiple projects, or for plug-and-play experiment tracking with existing machine learning project repos via `git submodule`.

## Motivation

Self-hosted experiment tracking that can be rolled out consistently over multiple projects, as an on-prem alternative to services like Weights & Biases or Comet.ml.

## Setup

1. For standalone use, `git clone` this repo. For integration with an existing ML project repo, `cd` to the ML project repo and `git submodule` this repo. 
2. Changes environment variables in `.env` as needed, then run `docker-compose up -d` from within this repo dir.
3. Access the Minio console (defaults to `http://localhost:3002`) and create the bucket with the name specified in `.env` (defaults to `my-mlflow-bucket`).
4. Configure local MLflow to have the same env vars in the bottom section of `.env`
5. Run the test script from your local setup and verify your installation is working.
6. Enjoy! 

## Architecture

`docker-compose.yml` defines the following services:

+ `mlflow`: houses the MLflow tracking server, dashboard accessible from `http://localhost:3000`.
+ `minio`: houses the Minio object store, API exposed at `http://localhost:3001`. User console accessible from `http://localhost:3002`.
+ `postgres`: stores data for the MLflow tracking server

When run, the services will create folders `minio-data/` and `mlflow-data/`. 

## Notes

**Credentials and version control**: The `.env` file provided is committed to git since the credentials within are safe to expose within the context of local usage. If you are hosting on cloud, please remember to NOT commit changes to `.env` to version control.

**Multiple users**: If shared between multiple users, it would be prudent to create individual key-secret pairs for each user from the Minio console. Probably also want to consider adding `nginx` for load balancing.

**Removing output folders**:  If you don't want the `minio-data/` and `mlflow-data/` folders to be created, you can opt to mount them as Docker volumes instead.

**Why local MLflow needs setting up env vars**: Local MLflow needs to have env vars to access the Minio server, because artifacts are logged directly to the artifact store instead of through the tracking server. The MLflow devs are working on logging artifacts directly through the tracking server, progress tracked in [this PR](https://github.com/mlflow/mlflow/issues/629).

## Example: Using MLflow in Python

``` python
# Setup env vars for MLflow
# These are the defaults specified in `.env`
import os
os.environ["AWS_SECRET_ACCESS_KEY"] = "minioadmin"
os.environ["AWS_ACCESS_KEY_ID"] = "minioadmin"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:3001"
os.environ["MLFLOW_S3_IGNORE_TLS"] = "true"

# Setup MLflow
import mlflow
mlflow.set_tracking_uri("http://localhost:3000") # MLflow tracking server exposed on port 3000 by default
mlflow.set_experiment("experiment-name")
mlflow.start_run()

# Log params
mlflow.log_params({
    "lr": 5e-4"
})

# Log figure
mlflow.log_figure(fig, "figure.png")

# Log metric
mlflow.log_metric("loss/train", loss.sum(), step=step)

# Log metrics
mlflow.log_metrics({
    "acc/train/0": acc[0].item(),
    "acc/train/1": acc[1].item()
}, step=step)

# End run
mlflow.end_run()
```

## Useful links

+ [About MLflow Tracking](https://www.mlflow.org/docs/latest/tracking.html)
+ [Minio Quickstart on Docker](https://docs.min.io/docs/minio-docker-quickstart-guide.html)
