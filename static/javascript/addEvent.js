function execute(quizName, dateTime) {
    authenticate().then(loadClient(quizName, dateTime));
}

function authenticate() {
    return gapi.auth2.getAuthInstance()
        .signIn({ scope: "https://www.googleapis.com/auth/calendar" })
        .then(function () { console.log("Sign-in successful"); },
            function (err) { console.error("Error signing in", err); });
}
function loadClient(quizName, dateTime) {
    gapi.client.setApiKey("AIzaSyBb3qko1h66HlW-nibqJ2QRdtIj9ovH4ZI"); //add calendar api_key here
    return gapi.client.load("https://content.googleapis.com/discovery/v1/apis/calendar/v3/rest")
        .then(function () {
            console.log("GAPI client loaded for API");
            addEvent(quizName, dateTime);
        },
            function (err) { console.error("Error loading GAPI client for API", err); });
}

// Make sure the client is loaded and sign-in is complete before calling this method.
function addEvent(quizName, dateTime) {
    console.log(dateTime)
    var dateTime = dateTime.split(" ")
    console.log(dateTime)
    return gapi.client.calendar.events.insert({
        'calendarId': 'primary',
        'resource': {
            'summary': `Quiz Buddy deadline for ${quizName}`,
            'description': `This is the deadline for your ${quizName} quiz`,
            'start': {
                'dateTime': `${dateTime[0]}T${dateTime[1]}`,
                'timeZone': 'Europe/London'
            },
            'end': {
                'dateTime': `${dateTime[0]}T${dateTime[1]}`,
                'timeZone': 'Europe/London'
            }
        }
    })
        .then(function (response) {
            console.log('Event', response);
        },
            function (err) { console.error("Execute error", err); });
}

gapi.load("client:auth2", function () {
    gapi.auth2.init({ client_id: "227321397067-j428048k4q8bs8ap7v67temnm3j4hv1k.apps.googleusercontent.com" }); //add calendar client_id here
});
