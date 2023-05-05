FROM  python:3.10.2-slim

RUN apt update && apt install -y --no-install-recommends \
                    default-jre \
                    git \
                    zsh \
                    curl \
                    wget \
                    fonts-powerline

RUN useradd -ms /bin/bash python

USER python

WORKDIR /home/python/app/src

ENV PYTHONPATH=${PYTHONPATH}/home/python/app
ENV JAVA_HOME=/usr/lib/jvw/java-11-openjdk-amd64


# configuring shell
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" \
    -t https://github.com/romkatv/powerlevel10k \
    -p git \
    -p git-flow \
    -p https://github.com/zdharma-continuum/fast-syntax-highlighting \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -a 'export TERM=xterm-256color'

RUN echo '[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh' >> ~/.zshrc

CMD [ "tail", "-f", "/dev/null" ]