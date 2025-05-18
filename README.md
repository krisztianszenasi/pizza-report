# Pizza Sales BI Project

This is a little demo I whipped up for a BI class assignment at uni. It’s
strictly for local development — not production, unless you enjoy living
dangerously.

A somewhat detailed documentation can be read [here](docs/DOCUMENTATION.md) (_in hungarian_).

## CSV Files

The `untouched` directory contains the original `.csv` files from [here](https://www.kaggle.com/datasets/mysarahmadbhat/pizza-place-sales).

In the `utils` folder with the `spit_csv_files.py` script the orders can be
split up by month. The results will appear in the `utils/monthly_chunks` folder.

```
cd utils && python split_csv_files.py
```

> The repository includes the splited `.csv` files by default.

> If you wan't to run it yourself dont forget to install the packages from `requirements.txt`

## Starting The Project

The project is very simple to start since it uses docker containers.

First you need to initialize the **apache airflow** components:

```
docker compose up airflow-init
```

and the you can run with build

```
docker compose up --build
```

> Some operating systems (Fedora, ArchLinux, RHEL, Rocky) have recently introduced Kernel changes that result in Airflow in Docker Compose consuming 100% memory when run inside the community Docker implementation maintained by the OS teams. Read more [here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).

## Airflow

[Apache Airflow](https://airflow.apache.org/) is used as the **ETL engine** in
the project. You can visit it's control panal at http://localhost:8080/.
The login credential are `airflow:airflow`.

The **DAGS** (_like ETL jobs_) are configred in a way that if you place the
appropirate `.csv` files into `airflow/files/to_process` then the engine will
process them automatically. Mainly there are three **DAGS**:

* **load_data_to_staging**: loads the data from the `.csv` files to the **staging tables**
* **transform_from_staging**: moves the data from the **staging tables** to the **final tables** and optionally removes incorrect data
* **aggragate_data**: creates additional tables for preaggregated data to speed up queries

To tigger the pipeline simply place the `.csv` files into the `to_process` folder.

You can either place all the files from `untouched_data` or use the `move_orders.sh` script for incremental loading.

Assuming that the `pizzas.csv` and `pizza_types.csv` files are already loaded you can incrementally load the orders data by month:

```
./move_orders.sh 2015_01
```

> This script copies the `.csv` files associated with **2015_01** and places
> them inside `airflow/dags/files/to_process` from where the **scheduled** dag
> can pick it up.

## Superset

[Apache Superset](https://superset.apache.org/) is used for data visualiztaion.
You can access the application at http://localhost:8088.
The login credentials are `admin:admin`.

## Additional Thougts

* Yup, I know there are some secret keys chilling in this repo — but don’t worry
 it’s just a dummy uni assignment. The goal was to make it super easy to spin up,
 not secure the Pentagon.

* Storing the Superset charts like this? Definitely not award-winning. Ideally,
they’d be exported as `.json` or `.yaml` and loaded in like a pro — but hey,
deadlines.

* Feel free to poke around, steal ideas, or use this as inspiration. Just
remember: this ain’t best practice land — it’s more like “sleep-deprived student
trying their best to hand something in on time” land.
