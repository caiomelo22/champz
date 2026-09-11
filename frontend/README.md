## Setup
To run the project, just create a `.env` file with the following variables. They represent your API base url, and the static directory of your API where your static images are going to be mirrored as a volume.

```
VUE_APP_BASE_URL="http://localhost:8000"
VUE_APP_MEDIA_URL="http://localhost:8000/static"
```

Install dependencies and start Nuxt on port 8080:

```powershell
npm install
npm run dev
```

The draft page polls the auction snapshot every three seconds. This keeps current bids, countdowns, completed assignments, and outbid notifications synchronized without requiring a WebSocket service. Countdown values are visual only; the backend UTC deadline is authoritative.

Use `npm run build` for a production build. The npm scripts include the OpenSSL compatibility option required by this Nuxt 2/Webpack 4 stack on modern Node versions.
