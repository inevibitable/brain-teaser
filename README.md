# Brain Teaser

This is a toy project to implement basic read access to the /etc/passwd and /etc/group files as an HTTP service.
It is not intended for any real use case. Feel free to look at the code and use it in your your own projects.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project in production

### Prerequisites

You'll need an internet connection, and [Docker](https://hub.docker.com/search/?type=edition&offering=community) for the operating system you're running on. Once you've installed and set up docker, you should be able to invoke this command in a shell.

```bash
> docker --version 
Docker version 18.09.2, build 6247962
```

To run the unit tests, you'll need to install pytest via python pip:

```bash
python -m pip -U install pytest
```

### Installing

A step by step series of examples that tell you how to get a development env running

Step 1

cd into the /src/ folder and build the docker container with:

```bash
> docker build -t brain-teaser .
```

then, if nothing went wrong, run the container with 

```bash
> docker run -p localhost:{your-favorite-unused-port}:5000/tcp brain-teaser
```

If you'd like to use your own group or passwd file, set the GROUPFILE_PATH and PASSWDFILE_PATH environment variables in the container. 
Don't forget to copy the files to the location you specified in your container. 

```bash
> docker run -p localhost:{your-favorite-unused-port}:5000/tcp -e GROUPFILE_PATH="/your/groupfile/path/group" -e PASSWDFILE_PATH="/your/passwdfile/path/passwd" --detach brain-teaser
> docker ps 
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                      NAMES
0eaff0ae41e3        brain-teaser        "flask run --host=0.…"   9 seconds ago       Up 7 seconds        127.0.0.1:8000->5000/tcp   optimistic_mestorf
> docker cp ./group optimistic_mestorf:/your/groupfile/path/group
> docker cp ./passwd optimistic_mestorf:/your/passwdfile/path/passwd
```

You can then make HTTP API requests to the container via the port defined above from curl or your favorite browser directly to the docker container from your host OS. 

```bash
> curl localhost:8000/users/0
[{'user': 'root', 'uid': '0', 'gid': '0', 'comment': 'root', 'home': '/root', 'shell': '/bin/ash'}]
```

Stop the service by running 

```bash
> docker stop optimistic_mestorf
```

## Running the tests

To run the unit tests, just open a shell in the /src/ directory and run:

```bash
pytest
```

## Built With

* [python](https://www.python.org/) - Python. 
* [Flask](http://flask.pocoo.org/) - Flask, a microframework for Python. 
* [Docker](https://hub.docker.com/search/?type=edition&offering=community) - Testing and deployment
* [pytest](https://docs.pytest.org/en/latest/) - Unit tests

## Authors

* **Paul M** 

## License

See LICENSE file.

## Acknowledgments

* Work smarter, not harder


