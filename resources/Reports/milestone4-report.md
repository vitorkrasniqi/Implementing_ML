# Milestone 4: Report
## Task 0)
Unfortunately, as some of the other groups, we were not able to finish the missing parts of our milestone 3 due to complexity and time constraints. 

## Task 1)
### Questions
Q: What is Experiment Management and why is it important?

A: Experiment Management is a process of tracking experiment data, like code and data versions, hyperparameters and so on and it is important to keep track of which approaches were used and how they performed, so that we can orient well in our machine learning experiment. 

Q: What is a Metric in ML?

A: Metric is a summary of a model outcome in the form of one or more numbers. 

Q: What is Precision and Recall? Why is there often a Trade-off between them?

A: Precision is the true positive rate divided by all data points predicted as positives (including the ones that are not actually positive). It tells us how many of our positive predictions are actually positive. Recall or sensitivity is the true positive rate divided by all data points that are actually positive. This metric tells us how many of the actually positive points we predicted correctly. There is a tradeoff, because if I predicted that all the data points are positive, my recall would be great but my precision would be really bad. 

Q: What is AUROC Metric?

A: It is a metric that shows us how much/how well the model can distinguish between classes. It uses AUC (=area under the curve) and ROC (= receiver operating characterstics). The higher the ROC curve is, the better is the model at predicting classes. The metric is plotted with FPR (= false positive rate) at x-axis and TPR (= true positive rate) at y-axis.

Q: What is a Confusion Matrix?

A: Confusion Matrix is a table that visualises the predictions of a model. It consists of True and False Positives and True and False Negatives and by combining these numbers, we can get several metrics: Precision, Negative Predictive Value, Sensitivity, Specificity and Accuracy. 

## Task 2) 
All files for this task are included in the wandb folder of our repository.

### Our Code

To instrument our code with weights and biases, we added the following code to our main python script:
```sh
import wandb 
from wandb.keras import WandbCallback

run = wandb.init(project='our-wandb',
           config={
              "learning_rate": 0.005,
              "epochs": 12,
              "batch_size": 128,
              "loss": "categorical_crossentropy",
              "architecture": "CNN",
              "dataset": "MNIST"
           })
config = wandb.config
```
This was added at the beginning of our file before our code base. We also had to add the following code at the end of our main.py script:
```sh
wandb.log({'Test loss': score[0], 'Test accuracy': score[1]})
run.join()
```
We also made some changes in our compile function in compile_model.py:
```sh
def compile(learning_rate):
    import wandb
    config = wandb.config
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(config.learning_rate),
                  metrics=['accuracy'])
```
In the individual files we also had to import wandb and other wandb features we need to use, because the files do not "see" the code in our main.py file. 

The last change we needed to implement is in our fit_save_score_model.py, specificaly in the fit_model function. The function now looks like this:
```sh
def fit_model(batch_size, epochs):
    import wandb
    from wandb.keras import WandbCallback
    config = wandb.config
    model.fit(x_train, y_train,
              batch_size=config.batch_size,
              epochs=config.epochs,
              verbose=1,
              validation_data=(x_test, y_test),
              callbacks=[WandbCallback()])
```

### Dockerfile
We've had several problems with the Dockerfile. One was that we wanted to use an Alpine image of python and it weirdly interacted with pip which caused errors. This was resolved by simply using a different base. Some of the errors just stopped happening without making any changes to the code. The last problem was that during the building of the image, the program was not able to find the path to the $WANDB_TOKEN. We resolved it by assing "bash" to ENTRYPOINT like this: `ENTRYPOINT ["bash","docker_entrypoint.sh"]`. 

Our Dockerfile now looks like this:
```sh
FROM python:3.8.3

WORKDIR /home/parallels/Desktop/test

COPY . /home/parallels/Desktop/test

RUN pip install -U pip
RUN pip install -r requirements.txt

ENTRYPOINT ["bash","docker_entrypoint.sh"]

CMD python3 main.py
```
### entrypoint script
The entrypoint script is the same as recommended in the assignment:
```sh
#!/bin/bash
set -e

wandb login $WANDB_TOKEN

exec "$@"
```
### Running It Together
We did not have any other problems with buidling the image, however, we did run into some when running the Docker container. The error message was different every time we tried to run it. I found out that it was probably caused by reloading the wandb website and checking the results while the code in the container was still running. Once I ran the whole code without reloading the website, everything worked perfectly. 

We used the following code:
```sh
docker build --tag test_run .
docker run --name test_running --env-file=my.env -d <image_id>
```
After that, we checked the code with the `docker logs <container_name>` command.

You can see our runs [here](https://wandb.ai/michaelahavl/our-wandb?workspace=user-michaelahavl). Two of them are marked as failed because the the score was not properly defined, but otherwise it has all the data. 

## Task 3) 
The jupyter notebook can be seen in our repository. There are comments for the code as well.
