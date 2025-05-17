from airflow.models import Connection
from airflow import settings
import subprocess

def setup_connection():
    session = settings.Session()
    conn_id = "pizza_pg_conn"
    if not session.query(Connection).filter(Connection.conn_id == conn_id).first():
        conn = Connection(
            conn_id=conn_id,
            conn_type="postgres",
            host="pizza_db",
            login="pizza",
            password="pizza",
            schema="pizza",
            port=5432,
        )
        session.add(conn)
        session.commit()
        print(f"Connection '{conn_id}' added.")
    else:
        print(f"Connection '{conn_id}' already exists.")

def activate_dag(dag_id):
    subprocess.run(["airflow", "dags", "unpause", dag_id], check=True)

if __name__ == "__main__":
    setup_connection()
    for dag_id in ['aggregate_data', 'transform_from_staging', 'load_data_to_staging']:
        activate_dag(dag_id)
        print(f'Activated dag with id "{dag_id}"')
