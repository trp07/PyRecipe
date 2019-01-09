FROM python:3.6.8-stretch

COPY pyproject.toml /PyRecipe/pyproject.toml

RUN wget https://repo.mongodb.org/apt/debian/dists/stretch/mongodb-org/4.0/main/binary-amd64/mongodb-org-server_4.0.5_amd64.deb && \
mkdir -p /data/db && \
apt install ./mongodb-org-server_4.0.5_amd64.deb && \
rm mongodb-org-server_4.0.5_amd64.deb && \
pip install poetry && \
mkdir -p ~/.config/pypoetry && \
cd ~/.config/pypoetry && \
echo "settings.virtualenvs.create = false" > config.toml && \
cd /PyRecipe && \
poetry install
