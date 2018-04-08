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

cleanup() {
    # Cleanup instance files, such as socket files, test files and so on.
    echo "Doing exit cleanup."
    echo "  - Removing /radar/sockets folder."
    rm -rf /radar/sockets
    rm -rf /radar/radar_parlamentar/static
    rm -rf /radar/radar_parlamentar/htmlcov
}

setup_cron() {
  echo "Setuping cron"
  crontab -l > mycron
  # Executes 'manage.py runcrons' hourly:
  echo "5 * * * * python /radar/radar_parlamentar/manage.py runcrons >> /var/log/radar/cronjob.log 2>&1" >> mycron
  crontab mycron
  rm mycron
  crond
}

case "$1" in
  deploy)
    echo "Initializing deploy mode."
    wait_for_port "Postgres" "$DB_HOST" "$DB_PORT"
    python manage.py migrate
    python manage.py collectstatic --noinput
    setup_cron
    ;;
  celery)
    echo "Initializing celery."
    celery -A radar_parlamentar worker -l info --concurrency 1
    ;;
  migrate)
    echo "Initializing migrate mode."
    wait_for_port "Postgres" "$DB_HOST" "$DB_PORT"
    python manage.py migrate
    ;;
  clean)
    echo "Initializing cleaning mode."
    cleanup
    ;;
  test_only)
    echo "Initializing test only mode".
    # Radar will use SQLite
    export RADAR_TEST='True'
    python manage.py test
    ;;
  test|test_and_coverage)
    echo "Initializing test and coverage mode."
    # Radar will use SQLite
    export RADAR_TEST='True'
    coverage run --rcfile="../.coveragerc" --source="." manage.py test analises exportadores importadores modelagem plenaria radar_parlamentar
    echo ""
    echo ""
    echo "################################################################"
    echo "Coverage report:"
    coverage report
    coverage html &> /dev/null
    echo "To see the detailed coverage report, open the file radar_parlamentar/htmlcov/index.html on your browser."
    ;;
  travis)
    echo "Initializing travis mode."
    export RADAR_TEST='True'
    coverage run --source="." manage.py test analises exportadores importadores modelagem plenaria radar_parlamentar
    coverage xml
    coverage report
    ;;
  *)
    # The command is something like bash, not an airflow subcommand. Just run it in the right environment.
    echo "Default initialization."
    wait_for_port "Postgres" "$DB_HOST" "$DB_PORT"
    python manage.py migrate
    python manage.py collectstatic --noinput
    setup_cron
    echo "Starting uwsgi"
    uwsgi --ini /radar/deploy/radar_uwsgi.ini
    ;;
esac
