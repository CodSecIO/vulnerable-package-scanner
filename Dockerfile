FROM python:3
RUN pip install GitPython semgrep tabulate requests
COPY src/ /src
WORKDIR /src
ENTRYPOINT [ "python", "main.py" ]
