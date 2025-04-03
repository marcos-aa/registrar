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
3. Create a `.env` file at the root of the project
4. Add the following values to the `.env` file:
- SECRET_KEY=`<Random used to sign access tokens>`
- SECRET_REFRESH_KEY=`<Random key used to sign refresh tokens>`
- EMAIL_USERNAME=`<Your gmail account>`
- EMAIL_PASSWORD=`<Your gmail **app** password>` (Obtain at [Google app passwords](https://myaccount.google.com/apppasswords))
6. Install `uv`, the package manager:
- For macos and linux, run:
- `curl -LsSf https://astral.sh/uv/install.sh | sh` or `wget -qO- https://astral.sh/uv/install.sh | sh` if your system doesn't have CURL.
- For windows, install with winget:
- `winget install --id=astral-sh.uv  -e`
- For other options, see: [UV installation methods](https://docs.astral.sh/uv/getting-started/installation/#installation-methods`)
7. Create a virtual environment with uv: `uv venv .venv`
8. Activate the virtual environment: `source .venv/bin/activate`
9. Install the dependencies: `uv sync`
10. Apply the migrations: `alembic upgrade head`
11. Run the app: `task run`
