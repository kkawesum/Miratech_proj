<h2>History Management System</h2>

This project implements a history management system that keeps track of the historical files. We are concerned with ingesting the data(csv files) and retrieving them based on few query parameters.

The broad objectives of the system are:
1. Develop an endpoint for authenticating the users. We are using a JWT token for this purpose.
2. Write a method for ingesting a source file from an AWS s3 bucket to snowflake tables.
3. Create a form in flask for getting the file name to be searched.
4. Pass the entered file name to another endpoint for retrieving the table contents from snowflake. The retrieved values are displayed in the form of a paginated json.

   Third endpoint will take 5 query parameters: 
	    id_ingestion=c71feb6fec8d00fd2f9a1a50220a357e[required]
	    table_name[optional]
	    hours=14[optional]
	    minutes=04[optional]
	    seconds=52[optional]
	    miliseconds=18[optional]
It will return a paginated list of updates, where every item contains all the history data from the update.

5. Restore data to SnowFlake database from historical data.
	- Fourth endpoint will have 2 parameters, id from ingestion and id from the update you want to apply.
	- Decide how to send the request with the 2 parameters, is completely open for you to define.
	- Submit the requested changes and apply the updates on the table, if no errors, return the old and new change on the response(define an ok and ko response, how do you think it should be?).
6. Create unit tests for every class and function defined
7. Ensure a code coverage of greater than 80% for the code.

<h2>Starting the Application</h2>

1. Start the app by running "auth.py". This is the entry point for our flask application.
2. Upon starting the app, we land to the index page.
3. We have to further navigate to the "/login" endpoint, it authenticates the user based on JWT token.
4. On authentication, we will be given access to a Ingestion service("/ingest") which will allow us to establish an AWS connection and ingest the s3 contents to a Snowflake warehouse. 

We are also given access to the Search service("/search") which is responsible for searching a file based on name.
 
5. I am in the process of adding further modifications and improvements as well as new test cases.
   
