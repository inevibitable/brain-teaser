# Brain Teaser

This is a toy project to implement basic read access to the /etc/passwd and /etc/group files as an HTTP service.
It is not intended for any real use case

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You'll need an internet connection, and [Docker](https://docs.docker.com/install/) for the operating system you're running on. 

```bash
docker --version 
Docker version 18.09.2, build 6247962
```

### Installing

A step by step series of examples that tell you how to get a development env running

Step 1

cd into the /src/ folder and build the docker container with:

```bash
docker build -t brain-teaser .
```

then, if nothing went wrong, run the container with 

```bash
docker run -p localhost:{your-favorite-unused-port}:5000/tcp brain-teaser
```

You can then make HTTP API requests to the container via the port defined above from curl or your favorite browser. 


```bash
curl localhost:8000/users
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Paul Mayzeles** 

## License



## Acknowledgments

* Work smarter, not harder


