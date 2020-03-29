
# quizBuddy
QuizBuddy is an webapp created to help improve students learning while making it easier for teachers to test students in a fun atmosphere.

## Background
QuizBuddy is designed to motivate students to do class quizzes by giving them a character whose development depends on their work ethic. On registration, the student can choose between 3 potential characters. The student can evolve their character in 3 stages by reaching certain score milestones after completing quizzes.

## External Sources
* Bootstrap 
	 * Nothing is required to be done to set up 

* Google Calendar API
	* Instructions below on how to set up

## Google Calendar API
We have used the Google Calendar API in our web app which requires you to get a api key and update the client id in the javascript script

#### Instructions to set up:
* To generate an api key follow this link: [https://console.developers.google.com/apis/library/calendar-json.googleapis.com](https://console.developers.google.com/apis/library/calendar-json.googleapis.com)
* In the quizBuddy folder (where the settings.py file is) create a new file called ".env"
* In the ".env" file add 
APIKEY = < Your generated API key >
* In the addEvent.js file (which is in the static/javascript directory) change the clientId to your generated clientId 

#### Extra Information:
Due to Google API restrictions to run the Django webapp on your local device you will have to use the url [http://localhost:8000/](http://localhost:8000/)
## Additional Packages
* asgiref 3.2.3
* astroid 2.3.3
* autopep8 1.5
* certifi 2019.11.28
* colorama 0.4.3
* Django 3.0.3
* isort 4.3.21
* lazy-object-proxy 1.4.3
* mccabe 0.6.1
* pycodestyle 2.5.0
* pylint 2.4.4
* python-dotenv 0.12.0
* pytz 2019.3
* six 1.14.0
* sqlparse 0.3.0
* wincertstore 0.2
* wrapt 1.11.2
## REFERENCES  
* Questions for psychology quiz taken from:
https://quizpug.com. (2020). Can You Answer 12 Basic Psychology Questions?. [online] Available at: https://quizpug.com/can-you-answer-12-basic-psychology-questions/ [Accessed 7 Mar. 2020].
