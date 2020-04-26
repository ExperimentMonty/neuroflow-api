# neuroflow-api
REST API for NeuroFlow coding assignment

## Sample API Commands

#### Create a user
`curl http://127.0.0.1:5000/users -H "Content-Type: application/json" -X POST -d '{"username": "coal", "password": "test"}'`

#### Post a mood
`curl -u coal:test http://127.0.0.1:5000/moods -H "Content-Type: application/json" -X POST -d '{"mood": "hungry"}'`

#### Retrieve moods
`curl -u coal:test http://127.0.0.1:5000/moods`

## Things I would change if this was a production environment
* We're currently using Flask's dev server, transition to an actual web server.
* Only basic auth is allowed, add functionality for token auth and/or OAuth.
* When calculating percentiles, we need to get and sort every user in the system, and then find the current user's place in that list. That will be a scaling issue eventually. Instead, we should have a separate table that keeps track of the number of users in each bucket, and when a user gets a longer streak, decrement the count of the old bucket he belonged to, and increment the count of his new bucket.  This solution would then be O(number of days app has existed) which should be fine for around decade.
* We're using SQLite, we should use a real production-level database.
* I implemented all of the REST endpoints manually, might use something like Flask-RESTful next time.
* There's not great documentation for each of these endpoints, I'd probably use something like Swagger to document these endpoints better for a production app.
* I'd probably want to think about adding some DB indices if we were scaling up a huge amount.

## Other thoughts
* I thought this was an interesting project, though there's a part of me that initially got caught up when you started off saying make a REST API, and then in the first requirement you say make a web REST application, I started making a web page and stuff to display the results of the endpoints I made before realizing that this is still just meant to be just an API. I'd ditch any mention of "web" and "application" just to make things a little more clear.
* The last requirement about getting this app prepped for containerization was a bit of a pain for me, ordinarily I'm doing that kind of development on a Mac or some kind of computer where installing docker is much easier/I've already got it set up, my home computer, I run some smaller scripts on it, but I don't do that level of dev work on it usually.  So, I spent way too long just trying to get docker running on my laptop with Windows 10 Home on it, and the installer docker provided me (because Windows 10 Home can't use the normal installer) screwed up my already-installed version of VirtualBox and Git, so I wiped it out, re-installed those, then installed docker inside of an Ubuntu VM I had. If there was one part of this assessment I wish was removed, it'd be that last requirement, I feel like setting up a container like this from scratch is a fire-and-forget kind of action, something you do a couple times a year, you look up the docs/your own previous examples each time, and aside from that, you don't need to know more than how to edit an existing Dockerfile. Maybe there would be some simpler way to have applicants demonstrate they have some kind of basic knowledge of Docker than to do this.
* I imagine this is probably something you purposefully chose to leave to the applicant's choice, but saying what kind of authentication you'd want would be nice. I imagine some people might get nervous, spiral, and try to implement something way too complicated for a test assessment like this, because they wouldn't know if they were doing enough for this slightly vague requirement.