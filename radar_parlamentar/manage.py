#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if sys.argv[1] == 'test':
        os.environ["DJANGO_SETTINGS_MODULE"] = "radar_parlamentar.settings.test"
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "radar_parlamentar.settings.development")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
