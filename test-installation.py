"""
Test logging to MLflow from outside the docker containers
If this script completes successfully, and you can see the associated
run in MLflow with the uploaded artifact, you are good to go.
"""
import os
import mlflow

os.environ["AWS_SECRET_ACCESS_KEY"] = "minioadmin"
os.environ["AWS_ACCESS_KEY_ID"] = "minioadmin"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:3001"
os.environ["MLFLOW_S3_IGNORE_TLS"] = "true"

mlflow.set_tracking_uri("http://localhost:3000")
mlflow.set_experiment("test-experiment")
mlflow.start_run()
mlflow.log_metric("acc", 0.5, step=10)
mlflow.log_metric("acc", 1, step=20)

with open("example-artifact.txt", "w") as f:
    f.write("test content")

mlflow.log_artifact("example-artifact.txt")

mlflow.end_run()
