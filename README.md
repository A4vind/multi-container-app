# Practical 6 – Multi-Container Application (Flask + MySQL) using Docker Compose

**Aim:** Run a web server (Flask) and a database (MySQL) as two separate containers that talk to each other, managed with Docker Compose.

## Project files

| File | Purpose |
|---|---|
| `app.py` | Flask web app that connects to MySQL and shows the result |
| `requirements.txt` | Python libraries needed (flask, mysql-connector-python) |
| `Dockerfile` | Builds the image for the Flask web container |
| `compose.yaml` | Defines both containers (`web` and `db`) and how they connect |
| `.env.example` | Sample passwords – copied to `.env` before running |
| `.gitignore` | Keeps the real `.env` (passwords) off GitHub |

## Requirements

- Windows 10/11 with **Docker Desktop** installed
- **Git** installed (only needed to clone the repo)

---

## Execution steps (Windows – Command Prompt)

### Step 1 – Start Docker
**When:** before anything else.

Open **Docker Desktop** and wait until it shows **Engine running**. Then check it in cmd:

```
docker --version
docker compose version
docker info
```

### Step 2 – Get the project
**When:** once, after Docker is running.

```
cd %USERPROFILE%
git clone https://github.com/YOUR-USERNAME/multi-container-app.git
cd multi-container-app
```

(Or download the ZIP from GitHub → extract → `cd` into the folder.)

### Step 3 – Create the `.env` file
**When:** once, before the first run. Docker Compose reads the passwords from this file.

```
copy .env.example .env
```

Optional: open it with `notepad .env` and change both passwords.

### Step 4 – Check the files
**When:** before building, to make sure no file got a `.txt` extension.

```
dir
```

You should see `app.py`, `requirements.txt`, `Dockerfile`, `compose.yaml`, `.env`.
If you see `Dockerfile.txt`, fix it with `ren Dockerfile.txt Dockerfile`.

### Step 5 – Build and start both containers
**When:** to run the application (first run takes a few minutes to download images).

```
docker compose up -d --build
```

- `--build` builds the Flask image from the `Dockerfile`
- `-d` runs the containers in the background

### Step 6 – Check the containers
**When:** right after Step 5. Repeat every ~30 seconds until `db` is healthy.

```
docker compose ps
```

Wait until **db** shows `(healthy)` and **web** shows `Up`.

### Step 7 – Open the application
**When:** after `db` is healthy.

Open a browser and go to: **http://localhost:5000**

Expected output:

> **Docker Multi-Container App**
> Flask Running
> Connected to MySQL successfully!

### Step 8 – View logs (only if something is wrong)
**When:** if the page doesn't load or shows an error.

```
docker compose logs web
docker compose logs db
```

### Step 9 – Stop the application
**When:** after you are done.

```
docker compose down
```

To also delete the database data (full reset):

```
docker compose down -v
```

---

## Command summary

| Order | Command | When to run |
|---|---|---|
| 1 | `docker --version` / `docker compose version` / `docker info` | Check Docker is running |
| 2 | `git clone ...` then `cd multi-container-app` | Get the project (once) |
| 3 | `copy .env.example .env` | Create password file (once) |
| 4 | `dir` | Verify file names |
| 5 | `docker compose up -d --build` | Build and start containers |
| 6 | `docker compose ps` | Check status (wait for healthy) |
| 7 | Open `http://localhost:5000` | See the output |
| 8 | `docker compose logs web` | Only if there is an error |
| 9 | `docker compose down` | Stop everything |

## Troubleshooting

- **"Database connection failed"** – MySQL is still starting. Wait 30 seconds and refresh.
- **"port is already allocated"** – change `"5000:5000"` to `"5001:5000"` in `compose.yaml`, run Step 5 again, open `http://localhost:5001`.
- **Errors after changing passwords in `.env`** – run `docker compose down -v`, then Step 5 again.
- **`cd %USERPROFILE%\Desktop` fails** – Desktop is inside OneDrive; use `cd %USERPROFILE%\OneDrive\Desktop` or just `cd %USERPROFILE%`.

## How it works

1. `docker compose up` starts the **db** container (MySQL 8.4) and creates the database `mydatabase` and user `appuser`.
2. The **healthcheck** pings MySQL every 10 seconds; the **web** container waits (`depends_on: service_healthy`) until MySQL is ready.
3. The **web** container (Flask) connects to the host name `db` – Compose's internal network lets containers find each other by service name.
4. MySQL data is stored in the `mysql_data` volume, so it survives restarts.
