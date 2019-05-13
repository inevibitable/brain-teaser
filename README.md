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

You can then make HTTP API requests to the container via the port defined above from curl or your favorite browser directly to the docker container from your host OS. 

```bash
> curl localhost:8000/users/0
[{'user': 'root', 'uid': '0', 'gid': '0', 'comment': 'root', 'home': '/root', 'shell': '/bin/ash'}]
```

## Running the tests


## Deployment

Deploying on a production system.

## Built With

* [Docker](https://hub.docker.com/search/?type=edition&offering=community) - Testing and deployment

## Authors

* **Paul M** 

## License

See LICENSE file.

## Acknowledgments

* Work smarter, not harder


