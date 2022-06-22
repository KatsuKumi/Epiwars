<h1 align="center">
  <br>
  <a href="https://epitech.eu"><img src="https://raw.githubusercontent.com/KatsuKumi/Epiwars/main/client/src/assets/testlogo.png" alt="BeatConnect" width="200"></a>
  <br>
  Epiwars
  <br>
</h1>

<h4 align="center"> A hackathon plateform to organize and manage hackathons for Epitech students</h4>


<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#official-website">Official Website</a> •
  <a href="#license">License</a> •
  <a href="https://epitech.eu">Epitech Website</a>
</p>

## Key Features

- Login with Github
- Hackathon countdown
- Subject description in Markdown
- IDE in the browser to edit the code and tests
- Docker to run and test the code provided by the students
- Tests output
- Hackathon leaderboard
- Ranking system
- Multiple languages supported (WIP)
- Create a hackathon
- Manage hackathons and challenges


## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com) | [Python](https://www.python.org/downloads/) | [Node.js](https://nodejs.org/en/) installed on your computer.

You have to run the server and the client in different terminals.

To run the server, you can use the following command:

```bash
# Clone this repository
$ git clone https://github.com/KatsuKumi/Epiwars

# Go into the client repository
$ cd server

# Install dependencies
$ pip install -r requirements.txt

# Update the database
$ python manage.py migrate

# Run the app
$ python manage.py runserver 8000
```

Note: I highly recommend to create a virtual environnment for running the project [Documentation Here](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)

To run the client, you can use the following command:

```bash
# Clone this repository
$ git clone https://github.com/KatsuKumi/Epiwars

# Go into the client repository
$ cd client

# Install dependencies
$ npm install

# Run the app
$ npm run serve
# Or build for production
$ npm run build
```



## API Endpoints



## Official Website

The project don't have any official website, but you can find the source code on this GitHub repository.

## License

GNU General Public License v3.0

---

> GitHub [@VigeantAlex](https://github.com/frobot/) &nbsp;&middot;&nbsp;
> Linkedin [@alexandre-vigeant](https://www.linkedin.com/in/alexandre-vigeant/)