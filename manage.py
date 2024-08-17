#!/usr/bin/env python
import os
import sys


def main():
    """Выполняет административные задачи."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_register.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    from shop.log_config import LogConfig
    from django.conf import settings
    log_config = LogConfig(settings.LOG_FILE_NAME)
    log_config.setup_logging()

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
