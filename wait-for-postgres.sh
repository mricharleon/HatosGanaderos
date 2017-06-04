#!/bin/sh

postgres_host=$1
postgres_port=$2
shift 2
cmd="$@"

# wait for the postgres docker to be running
while ! pg_isready -h $postgres_host -p $postgres_port -q -U postgres; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

# run the command
exec $cmd
