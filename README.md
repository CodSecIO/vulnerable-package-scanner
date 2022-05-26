# VPS - Vulnerable Package Scanner
VPS is a tool to validate if your python projects are making use of vulnerable CTX package. It supports individual repository scan, or a whole Github organization.

This tool is delivered as a docker container, you need to have docker installed in your system, and build the image before running as presented in the instructions below.

# How to use
```bash
# build the docker image
$ docker build -t codsec/vps .

# run against an individual public repository
$ docker run --rm -it codsec/vps <git-url>

# run against public repositories of an entire Github organization
$ docker run --rm -it codsec/vps <organization-url>

# run against an individual private repository
$ docker run --rm -it codsec/vps <git-url> <access-token>

# run against public repositories of an entire Github organization
$ docker run --rm -it codsec/vps <organization-url> <access-token>


# git-url e.g.:
# https://github.com/CodSecIO/vulnerable-package-scanner.git

# organization-url e.g.:
# https://github.com/CodSecIO 
```

**Note:** Internally the provided `access-token` is injected into the repository url to access private repositories, e.g.: `https://<access-token>@github.com/CodSecIO/vulnerable-package-scanner.git`
