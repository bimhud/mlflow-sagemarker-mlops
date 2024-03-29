import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn import datasets

# uncomment portion below if using a remote mlflow instance
import socket
ip=socket.gethostbyname(socket.gethostname())
port='5000'

#set the server address in order to communiate with S3, otherwise will generate data locally on mlruns folder
mlflow.set_tracking_uri("http://{0}:{1}".format(ip,port))
mlflow.set_experiment("iris") # creates an experiment if it doesn't exist

iris = datasets.load_iris()
x = iris.data[:, 2:]
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=7)

with mlflow.start_run(run_name="Iris RF Experiment") as run:
    
    # add parameters for tuning
    num_estimators = 100
    mlflow.log_param("num_estimators",num_estimators)

    # train the model
    rf = RandomForestRegressor(n_estimators=num_estimators)
    rf.fit(X_train, y_train)
    predictions = rf.predict(X_test)

    # save the model artifact for deployment
    # this will save the model locally or to the S3 bucket if using a server
    mlflow.sklearn.log_model(rf, "random-forest-model")

    # log model performance 
    mse = mean_squared_error(y_test, predictions)
    mlflow.log_metric("mse", mse)
    print("  mse: %f" % mse)

    run_id = run.info.run_uuid
    experiment_id = run.info.experiment_id
    print(experiment_id)
    
    print(mlflow.get_artifact_uri())
    print("runID: %s" % run_id)

    mlflow.end_run()
