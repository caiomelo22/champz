# Backend

## Setup

Create `.env` from `.env.example`, then set the MySQL credentials and replace both token secrets with independent random values.

```env
DB_HOST=host.docker.internal
DB_DATABASE=fifa-db
DB_USER=root
DB_PASSWORD=pwd
JWT_SECRET=replace-with-a-long-random-value
VERIFY_SECRET=replace-with-another-long-random-value
FRONTEND_URL=http://localhost:8080
```

Install dependencies and apply migrations:

```powershell
.\env\Scripts\python.exe -m pip install -r requirements-dev.txt
.\env\Scripts\alembic.exe upgrade head
```

Start the API from this directory:

```bash
./start.sh
```

Or run Uvicorn directly from PowerShell:

```powershell
.\env\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

## Account Verification

Password registrations must verify their e-mail before protected routes are available. If a championship owner entered that address on a participant beforehand, successful verification links the account automatically. Google OAuth accounts are treated as verified and resolve the same pending link.

Local development defaults to `EMAIL_BACKEND=console`; the verification URL is written to the backend log. For deployed environments, configure SMTP:

```env
EMAIL_BACKEND=smtp
EMAIL_FROM=Champz <no-reply@example.com>
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_USE_TLS=true
SMTP_USE_SSL=false
SMTP_TIMEOUT_SECONDS=10
```

Set exactly one of TLS or SSL according to the provider. Verification tokens are valid for 24 hours.

## Auctions

Auction deadlines arrive as ISO-8601 timestamps and are normalized to a UTC minute. The frontend converts the local `datetime-local` value to UTC before sending it. Bids are transactional: the winning amount is deducted immediately, a previous leader is refunded in the same transaction, and finalization does not debit the winner again.

The API lifespan starts a lightweight finalizer every 30 seconds. It scans the `(status, deadline)` index and closes due auctions idempotently, including auctions left open across an application restart. The auction list also reconciles due rows before responding.

An owner cannot change a participant's available budget while that participant leads an open auction. Cancel the auction first if the reservation must be released.

## Tests

The default suite uses isolated in-memory SQLite databases:

```powershell
.\env\Scripts\python.exe -m pytest tests -q
```

Concurrency behavior requires MySQL row locks. These tests create and remove a uniquely named temporary database using the credentials in `.env`:

```powershell
$env:RUN_MYSQL_TESTS='1'
.\env\Scripts\python.exe -m pytest tests\test_auction_mysql_concurrency.py -q
Remove-Item Env:\RUN_MYSQL_TESTS
```
