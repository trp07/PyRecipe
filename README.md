# PyRecipe
A Cookbook Designed with Python!

# Under Developement
- This project is under development at the moment.
- The aim of this project is to have a **Flask** & **MongoDB** web app.
- To work on the project, below you'll find some installation instructions.

## Installation
1.  Install the [**MongoDB Server - Community Edition**](https://www.mongodb.com/download-center/community)
2.  Install the [**poetry**](https://github.com/sdispater/poetry/) package management system.
3.  Create a _virtual environment_ with python **3.6+**.
4.  Clone this repository.
```shell
$ git clone https://github.com/trp07/PyRecipe.git
```
5.  Install the project in **development** mode.
```shell
$ cd PyRecipe
$ poetry install
```
6.  Run Tests
```shell
$ pytest -v
```
7.  If tests successfully pass, then begin contributing in your **feature branch**.

## Running in Docker
To run this in Docker, use the following commands.
You shouldn't need to run build and poetry install except on first run.
```bash
docker build -t pyrecipe .
docker run --rm -itv $(pwd):/PyRecipe -w PyRecipe bash
poetry install
nohup /usr/bin/mongod &
pytest -v
```

This still needs work. Improvements that are still needed are:
* All dependencies to be installed in the build step without having all the files persist, so build doesn't have to happen often.
* The mongo daemon to be run in the background by default. Though this belongs in a separate container really.

If these improvements are made, we should then be able to just run:
```bash
docker run --rm -itv $(pwd):/PyRecipe -w PyRecipe pytest -v
```
