# Milestone 5: Report

## Task 1)
### Questions
Q: How can you train a predictive model? How could you manage experiments, and create reports/visualizations while training your model?

A: When training a predictive model, we split our data into train and test set. We train the model on the train set with labels, which the algorithm learns to predict. Then we feed the test data without labels into the model and we let the model predict the labels. As a last step, we compare the predicted labels with the actual values to evaluate the performance of the model.

We can write report on our project and visualize the performance and other selected metrics with Weights and Biases, where we can see graphical representations of our different runs of the code, as we did in Milestone 4.

Q: How can you improve collaboration in a team?

A: The main tool in collaborating on the project has been GitHub and WhatsApp. One thing we would have to improve in the future would be to let each other know how far we have come in the task. Sometimes it is quite complicated to see what was actually done in the project, because when we are still figuring out parts of the assignment, the individual branches can get messy.

Q: How would you assess and ensure the quality of your code?

A: To make sure our code is of good quality, we followed the following guidelines:

- use the PEP8 style guide of Python code
- divide the code into snippets that are related
- define our own functions
- test the functions and modules individually
- when the whole code works on one machine, test it on the other machine as well

Q: How can you provide data to the model at inference time and save its predictions to analyze the model's performance in a real-world scenario?

A: The inference data could be provided by a REST API like in our example and we could have a database, which already stores the train and test data and to which we would save the predictions as well. Therefore we could measure the performance on the extended data points.

Q: How can you  improve on the model iteratively and deploy it to customers in a web application? How could you structure your product as a microservice architecture?

A: When preparing the model, we can use gradient descent to find values of parameters that minimize the loss function of a model (can be seen in the compile() function). We can also do hyperparameter tuning and tune f.e. number of epochs, batch size and learning rate. Both methods are approaches of machine learning iteration. Finally, we would deploy the model with best results to the customer.

Microservice architecture is basically about splitting a big, complex system into smaller sub-systems based on their function. Each of the sub-systems can be deployed individually. In the project, we have been using this architecture almost from the start. We have several containers - f.e. one that takes care of PostgreSQL, one where we run our Python code - and then we connect them to the web application, where they work together to bring the predictions to customers.

### Example
Describe the process step by step with the example of an E-mail spam detector. Assume you want to provide a service where customers can send their E-mails to (f.e. a web page where you can upload E-mail text). The service responds with either "Spam" or "No Spam". Which tools would you use for each step in the process until the response ends up at the customers'screens? Also describe what metrics you might use to find out whether your model works (f.e. would you focus on Precision or Recall? Etc).

First, we would have to decide which kind of model we want to build for this service. Since we are talking about sequence/text data, recurrent neural network would be our choice. Because we have different length of input and output in this sequence-to-vector model, we would have to use an encoder-decoder architecture for the model and we should explore the possibility of including an attention layer to avoid problems with longer messages.

We have to collect/find a dataset with spam and no spam emails with labels. We can store the data in a database like PostgreSQL. Then we train the model, optimize and tune it and evaluate the performance on test data. When we are happy with the result, we save the trained model. For the compiling of the model, we would use Keras. To evaluate the performance of the model, we could make use of Weights and Biases again.

Then we prepare an app.py script, where we initialize the flask app, load the model and specify where we want to run the app. We would have two docker containers - the Flask app and the database.

Once we run the app, we would get new inputs from customers and return predictions, which we can then store in the database to extend our dataset.

We would focus on recall, as it tells us how many of spam emails the model correctly classifies. We expect that most of the inputs would be spam, because people would most probably only check emails they find suspicious. Therefore it would be useful to know how many of the spam emails the model classifies correctly.

## Task 2)
