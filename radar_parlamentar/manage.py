# !/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if (len(sys.argv) >= 2) and (sys.argv[1] == 'test'):
        os.environ["DJANGO_SETTINGS_MODULE"] = "settings.test"
    else:
        if not "DJANGO_SETTINGS_MODULE" in os.environ:
            os.environ.setdefault(
                "DJANGO_SETTINGS_MODULE", "settings.development")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
