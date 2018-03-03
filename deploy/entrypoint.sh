#!/usr/bin/env sh

TRY_LOOP="20"


# Não checa nada se estivermos em ambiente de teste, visto que, POR ENQUANTO,
# estamos usando sqlite para testes.
export DB_HOST="postgres"
export DB_PORT="5432"

# Install custom python package if requirements.txt is present
if [ -e "/radar/radar_parlamentar/requirements.txt" ]; then
    pip install -r /radar/radar_parlamentar/requirements.txt
fi

wait_for_port() {
  local name="$1" host="$2" port="$3"
  local j=0
  while ! nc -z "$host" "$port" >/dev/null 2>&1 < /dev/null; do
    j=$((j+1))
    if [ $j -ge $TRY_LOOP ]; then
      echo >&2 "$(date) - $host:$port still not reachable, giving up"
      exit 1
    fi
    echo "$(date) - waiting for $name... $j/$TRY_LOOP"
    sleep 5
  done
}

case "$RADAR_CMD" in
  deploy)
    wait_for_port "Postgres" "$DB_HOST" "$DB_PORT"
    python manage.py migrate
    python manage.py collectstatic --noinput
    ;;
  migrate)
    wait_for_port "Postgres" "$DB_HOST" "$DB_PORT"
    python manage.py migrate
    ;;
  test)
    # Radar will use SQLite
    export RADAR_TEST='True'
    python manage.py migrate
    # To make the container do not die and wait for the test execution:
    tail -f /dev/null
    ;;
  *)
    # The command is something like bash, not an airflow subcommand. Just run it in the right environment.
    wait_for_port "Postgres" "$DB_HOST" "$DB_PORT"
    python manage.py migrate
    python manage.py collectstatic --noinput
    uwsgi --ini /radar/deploy/radar_uwsgi.ini
    ;;
esac

rm -f /radar/sockets/radar.sock
