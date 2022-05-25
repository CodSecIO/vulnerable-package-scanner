FROM python:3
RUN pip install GitPython semgrep
COPY src/ /src
WORKDIR /src
ENTRYPOINT [ "python", "main.py" ]
