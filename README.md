# Registrar

A POC application that authenticates and authorizes users.

## Features
- User registration
- Email sending and confirmation
- Password update
- Persistent logins and JWT roken rotation

## How to run
1. Clone this repository: `git clone https://github.com/marcos-aa/registrar.git`
2. Open the apps directory: `cd registrar`
3. Create a `.env` file
4. Add the following values to the `.env` file:
- SECRET_KEY=`<Key used to sign access tokens>`
- SECRET_REFRESH_KEY=`<Key used to sign refresh tokens>`
- EMAIL_USERNAME=`<Your gmail account>`
- EMAIL_PASSWORD=`<Your gmail **app** password>` (Obtain at [Google app passwords](https://myaccount.google.com/apppasswords))
6. Activate the virtual environment: `source .venv/bin/activate`
7. Install the dependencies: `uv sync`
8. Run the app: `task run`
