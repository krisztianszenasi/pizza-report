from airflow.models import Connection
from airflow import settings
import subprocess


def setup_connection(
    *,
    conn_id: str,
    conn_type: str,
    host: str,
    login: str,
    password: str,
    schema: str,
    port: int,
) -> None:
    session = settings.Session()
    if not session.query(Connection).filter(Connection.conn_id == conn_id).first():
        conn = Connection(
            conn_id=conn_id,
            conn_type=conn_type,
            host=host,
            login=login,
            password=password,
            schema=schema,
            port=port,
        )
        session.add(conn)
        session.commit()
        print(f"Connection '{conn_id}' added.")
    else:
        print(f"Connection '{conn_id}' already exists.")


if __name__ == "__main__":
    setup_connection(
        conn_id="pizza_pg_conn",
        conn_type="postgres",
        host="pizza_db",
        login="pizza",
        password="pizza",
        schema="pizza",
        port=5432,
    )
