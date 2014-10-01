#!/bin/bash
pg_dump -h localhost -U radar radar --inserts -f $RADAR_HOME/static/files/db-dump/radar.sql
