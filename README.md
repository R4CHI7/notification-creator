Notifications Creator
====================

A small (emulated) utility for scheduling and tracking notifications using Django.

Project setup
-------------

- Setup database:

    - Login to the root user using mysql shell.
    - Create database as follows:

        `CREATE DATABASE notification_creator;`

    - Create a new user:

        `CREATE USER 'ns-admin'@'localhost' IDENTIFIED BY '%password%';`

    - Grant permissions to user:

        `GRANT ALL PRIVILEGES ON notification_creator.* TO 'ns-admin'@'localhost';`

    - Select the database using:

        `USE notification_creator;`

- Create a file named `dev.py` or `production.py` in the `notification_sender/settings` directory and copy variables from `base.py` which need to be modified.

- Add the following line to your `.bashrc` or `.zshrc` or equivalent shell configuration file:

    `export DJANGO_SETTINGS_MODULE="notification_creator.settings.dev"`

- Load the new settings in your shell using `source ~/.zshrc` or `source ~/.bashrc`.

- Migrate the database:

    `python manage.py migrate`

- Check the setup using the following command:

    `python manage.py runserver`
