import datetime
import pendulum
import os

import requests
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


@dag(
    dag_id="transform_from_staging",
    schedule=None,
    start_date=pendulum.datetime(2025, 5, 14, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def TransformFromStaging():
    def transform_ingredients():
        pg_hook = PostgresHook(postgres_conn_id='pizza_pg_conn')
        conn = pg_hook.get_conn()
        cur = conn.cursor()

        # Fetch all pizza types with their id and ingredient string
        cur.execute("SELECT id, ingredients FROM pizza_types")
        pizzas = cur.fetchall()  # List of tuples: (pizza_type_id, ingredients_str)

        # Cache existing ingredients {lower_name: id}
        cur.execute("SELECT id, name FROM ingredients")
        existing_ingredients = {name.lower(): ing_id for ing_id, name in cur.fetchall()}

        # Cache existing pizza_ingredients for quick duplicate check
        cur.execute("SELECT pizza_type_id, ingredient_id FROM pizza_ingredients")
        existing_mappings = set(cur.fetchall())  # set of (pizza_type_id, ingredient_id)

        for pizza_type_id, ingredient_str in pizzas:
            if not ingredient_str:
                continue
            ingredients = [i.strip() for i in ingredient_str.split(',') if i.strip()]

            for ing in ingredients:
                ing_lower = ing.lower()

                # Insert ingredient if missing and get its id
                if ing_lower not in existing_ingredients:
                    cur.execute(
                        """
                        INSERT INTO ingredients (name)
                        VALUES (%s)
                        ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
                        RETURNING id
                        """,
                        (ing,)
                    )
                    ing_id = cur.fetchone()[0]
                    existing_ingredients[ing_lower] = ing_id
                else:
                    ing_id = existing_ingredients[ing_lower]

                # Insert mapping if missing
                if (pizza_type_id, ing_id) not in existing_mappings:
                    cur.execute(
                        """
                        INSERT INTO pizza_ingredients (pizza_type_id, ingredient_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        (pizza_type_id, ing_id)
                    )
                    existing_mappings.add((pizza_type_id, ing_id))

        conn.commit()
        cur.close()
        conn.close()


    create_datawarehouse_tables = SQLExecuteQueryOperator(
        task_id="create_datawarehouse_tables",
        conn_id="pizza_pg_conn",
        sql="sql/create_datawarehouse_tables.sql"
    )


    transform_pizza_types = SQLExecuteQueryOperator(
        task_id="transform_pizza_types",
        conn_id="pizza_pg_conn",
        sql="sql/transform/transform_pizza_types.sql"
    )

    transform_pizzas = SQLExecuteQueryOperator(
        task_id="transform_pizzas",
        conn_id="pizza_pg_conn",
        sql="sql/transform/transform_pizzas.sql"
    )

    transform_orders = SQLExecuteQueryOperator(
        task_id="transform_orders",
        conn_id="pizza_pg_conn",
        sql="sql/transform/transform_orders.sql"
    )

    transform_order_details = SQLExecuteQueryOperator(
        task_id="transform_order_details",
        conn_id="pizza_pg_conn",
        sql="sql/transform/transform_order_details.sql"
    )

    transform_ingredients = PythonOperator(
        task_id="transform_ingredients",
        python_callable=transform_ingredients,
    )

    trigger_aggregate = TriggerDagRunOperator(
        task_id="trigger_aggregate_data",
        trigger_dag_id="aggregate_data",
        wait_for_completion=True,
        reset_dag_run=True,
    )


    create_datawarehouse_tables >> transform_pizza_types >> transform_pizzas >> transform_orders >> transform_order_details >> transform_ingredients >>trigger_aggregate


dag = TransformFromStaging()