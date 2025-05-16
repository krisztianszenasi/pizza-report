import datetime
import pendulum
import os
import shutil

import requests
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


@dag(
    dag_id="load_data_to_staging",
    schedule="* * * * *",
    start_date=pendulum.datetime(2025, 5, 14, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def LoadDataToStaging():
    create_staging_tables = SQLExecuteQueryOperator(
        task_id="create_staging_tables",
        conn_id="pizza_pg_conn",
        sql="sql/create_staging_tables.sql",
    )
    
    @task
    def load_csv_to_postgres(table_name: str, file_name: str):
        data_path = f'/opt/airflow/dags/files/to_process/{file_name}'
        done_path = f'/opt/airflow/dags/files/done/{file_name}'
        
        if not os.path.exists(data_path):
            print(f"File not found: {data_path}")
            return

        postgres_hook = PostgresHook(postgres_conn_id="pizza_pg_conn")
        conn = postgres_hook.get_conn()
        cur = conn.cursor()
        
        try:
            with open(data_path, "r", encoding='utf-8') as file:
                copy_sql = f"""
                    COPY {table_name}
                    FROM STDIN
                    WITH CSV HEADER DELIMITER AS ',' QUOTE '\"'
                """
                cur.copy_expert(copy_sql, file)
            conn.commit()
        finally:
            # Ensure the file is moved even if commit fails
            os.makedirs(os.path.dirname(done_path), exist_ok=True)
            shutil.move(data_path, done_path)
            print(f"Moved processed file to: {done_path}")


    trigger_transform = TriggerDagRunOperator(
        task_id="trigger_transform_from_staging",
        trigger_dag_id="transform_from_staging",
        wait_for_completion=True,
        reset_dag_run=True,
    )


    # Call data loading tasks
    load_pizza_types = load_csv_to_postgres("pizza_types_staging", "pizza_types.csv")
    load_pizzas = load_csv_to_postgres("pizzas_staging", "pizzas.csv")
    load_orders = load_csv_to_postgres("orders_staging", "orders.csv")
    load_order_details = load_csv_to_postgres("order_details_staging", "order_details.csv")

    # Chain create table -> load CSV
    create_staging_tables >> [
        load_pizza_types,
        load_pizzas,
        load_orders,
        load_order_details,  
    ] >> trigger_transform


dag = LoadDataToStaging()