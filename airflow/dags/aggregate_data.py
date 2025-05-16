import datetime
import pendulum
import os

import requests
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


@dag(
    dag_id="aggregate_data",
    schedule=None,
    start_date=pendulum.datetime(2025, 5, 14, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def AggregateData():

    aggregate_order_total_price = SQLExecuteQueryOperator(
        task_id="aggregate_order_total_price",
        conn_id="pizza_pg_conn",
        sql="sql/aggregates/aggregate_order_total_price.sql"
    )

    aggregate_ingredients_per_day= SQLExecuteQueryOperator(
        task_id="aggregate_ingredients_per_day",
        conn_id="pizza_pg_conn",
        sql="sql/aggregates/aggregate_ingredients_per_day.sql"
    )

    aggregate_order_total_price >> aggregate_ingredients_per_day


dag = AggregateData()