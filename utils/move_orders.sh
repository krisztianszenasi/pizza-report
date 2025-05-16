#!/bin/bash

# Usage: ./move_orders.sh 2015_01

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 YYYY_MM"
  exit 1
fi

DATE=$1
SRC_DIR="./monthly_chunks"                      # Adjust if your files are in a different source folder
DEST_DIR="../airflow/dags/files/to_process"

mkdir -p "$DEST_DIR"

for file_prefix in orders order_details; do
  SRC_FILE="${SRC_DIR}/${file_prefix}_${DATE}.csv"
  DEST_FILE="${DEST_DIR}/${file_prefix}.csv"
  
  if [ -f "$SRC_FILE" ]; then
    echo "Copying $SRC_FILE to $DEST_FILE"
    cp "$SRC_FILE" "$DEST_FILE"
  else
    echo "File $SRC_FILE not found, skipping."
  fi
done