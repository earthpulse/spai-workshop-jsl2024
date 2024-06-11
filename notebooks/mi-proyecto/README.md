# Getting started

SPAI projects are designed to facilitate the development of Earth Observation applications.They are flexible development and production environments that can be used in many different ways. These are some of the features that it offers:

- **Notebooks**: Run your jupyter notebooks headlessly to generate analytics, reports, etc.
- **Scripts**: Run your python scripts to process data, schedule tasks, etc.
- **APIs**: Create your own API endpoints to expose your layers and analytics.
- **UIs**: Start user interface applications to interact with your data.

This guide will help you get started with a simple SPAI project. To start, install spai

```bash
pip install spai
```

## SPAI project structure

A SPAI project is a directory with a specific structure. This structure is designed to facilitate the development and deployment of Earth Observation applications. The following is an example of a SPAI project structure:

```
- project-name
    - notebooks
        - notebook-name
            main.ipynb
            requirements.txt
            .env
        - ...
    - scripts
        - script1-name
            main.py
            requirements.txt
            .env
        - script2-name
            main.py
        - ...
    - apis
        - api1-name
            main.py
        - api2-name
            main.py
        - ...
    - uis
        - ui-name
            main.py
        - ...
    - shared
        - shared-group-name
            requirements.txt
            .env
        - ...
    - spai.config.yml
```

To create a SPAI project, create a folder with the name of your project. Inside, create a `spai.config.yml` file, where you can tell SPAI how to run your project. Then, create the folders for the different parts of your project: notebooks, scripts, apis and uis. Inside each folder, create subfolders with the names of the different services. You can have as many as you want. Finally, inside each subfolder, create a `main` file with the appropriate extension (`.ipynb` for notebooks, `.py` for the rest). Optionally, you can create a `requirements.txt` file to install the dependencies of each service and a `.env` file to define environment variables. If you want to reuse dependencies or environemnt variables between services, you can create a `shared` folder with the dependencies that you want to reuse inside a subfolder with the name of the group. Then, remember to add the name of the group to the `shared` field of the `spai.config.yml` file.

Alternatively, you can use the SPAI CLI to create a project structure. To do so, run the following command:

```bash
spai init
```

This guide assumes you are following with the template project provided by the CLI.

### Scripts

Let's start by creating a script that downloads Sentinel-2 images. In the `scripts` folder inside your project you will find subfolder with the name `downloader`. Inside, a `main.py` file contains the code. You can try to run it locally by running the following command:

```bash
python scripts/downloader/main.py
```

> Do it from the root dir to save outputs in the right place.

It should have created a `data` folder with the most recent available images for the provided location.

Let's create now a second script that computes NDVI from the downloaded images. You'll find it in `scripts/nvdi`. Again, you can try to run it locally by running the following command:

```bash
python scripts/ndvi/main.py
```

### Notebooks

The next step is to create a notebook that computes some analytics and generates a report. You'll find it in `notebooks/analytics`. Again, you can try to run it locally.

### APIs

Now that we have some scripts and notebooks to access, process and analyse data, let's make it available through APIs. The first api serves our analytics. You'll find it in `apis/analytics`. You can run the API locally with the command.

```bash
python apis/analytics/main.py
```

APIs in SPAI are just FastAPI apis, so you can use all the features of FastAPI.

The second API will serve our images and layers as an XYZ endpoint. You'll find it in `apis/xyz`. Again, you can run the API locally with the command.

```bash
python apis/xyz/main.py
```

### UIs

Finally, let's create a UI with streamlit to present our data. You'll find it in `uis/map`. You can run the UI locally with the command.

```bash
python uis/map/main.py
```

> Make sure to have the xyz API running!

## Deploying your project

Now that we have a working project, let's deploy it. To do so, we will use the SPAI CLI.

```bash
spai run
```

With this command, SPAI will deploy all the different services in your local machine.

The deployment can be configured via the `spai.config.yml` file. Here you can configure things such as the interval at which the scripts and notebooks should run (and in which order), the port in which the APIs and UIs should run, etc. The order in which you define the services will determine the order in which they will be run.

> TODO: docs with all the options

In order to deploy the project in the cloud, run

```bash
spai run --cloud
```

And that's all you need to deploy your project in the cloud! You can now go to your project's URL in the SPAI dashboard and get URLs for your APIs and UIs as well as the logs from the scripts and notebooks.

> TODO: You can also configure cloud parameters in the `spai.config.yml`, such as the type of resources that you want to use, the number of instances, GPUs, dependencies, etc.
