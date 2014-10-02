#!/bin/bash
pg_dump -h localhost -U radar radar --inserts -f $RADAR_HOME/static/db-dump/radar.sql
