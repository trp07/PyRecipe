FROM python:3.6.8-stretch

COPY pyproject.toml /PyRecipe/pyproject.toml

RUN wget https://repo.mongodb.org/apt/debian/dists/stretch/mongodb-org/4.0/main/binary-amd64/mongodb-org-server_4.0.5_amd64.deb && \
apt install ./mongodb-org-server_4.0.5_amd64.deb && \
rm mongodb-org-server_4.0.5_amd64.deb && \
pip install poetry && \
cd PyRecipe && \
poetry install
