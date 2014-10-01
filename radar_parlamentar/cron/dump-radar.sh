#!/bin/bash
pg_dump -h localhost -U radar radar --inserts -f $RADAR_PATH/static/files/db-dump/radar.sql
