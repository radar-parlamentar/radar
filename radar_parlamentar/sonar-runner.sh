#!/bin/bash
find . -type f -name "*.pyc" -exec rm -rf "{}" \;

git pull --rebase origin master

coverage erase
coverage run --source='.' manage.py test
coverage xml -o sonar/reports/coverage.xml

/opt/sonar-runner-2.3/bin/sonar-runner
