FROM python:3.11

WORKDIR /runner

ARG GITHUB_RUNNER_VERSION=2.304.0

ENV DEBIAN_FRONTEND=noninteractive \
    RUNNER_ALLOW_RUNASROOT=1

RUN curl -O -L https://github.com/actions/runner/releases/download/v$GITHUB_RUNNER_VERSION/actions-runner-linux-x64-$GITHUB_RUNNER_VERSION.tar.gz && \
    tar xzf actions-runner-linux-x64-2.304.0.tar.gz && \
    rm actions-runner-linux-x64-2.304.0.tar.gz && \
    bash ./bin/installdependencies.sh 

RUN curl -sSL https://get.docker.com/ | sh

RUN pip install poetry && \
    poetry config virtualenvs.create false

COPY images/entrypoints/github-runner-entrypoint.sh docker-entrypoint.sh

CMD ["bash", "docker-entrypoint.sh"]