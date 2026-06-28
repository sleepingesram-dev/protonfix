# ProtonFix — Frontend

Next.js 15 frontend for ProtonFix, the deterministic Linux gaming log analyzer.

## Dev

```bash
npm install
npm run dev
```

Open http://localhost:3000. The frontend expects the backend at `http://127.0.0.1:8000` (set in `.env.local`).

## Build

```bash
npm run build
npm start
```

## Environment

| Variable | Default | Purpose |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend URL baked in at build time |

For production, set this at build time:

```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com npm run build
```

## Docker

Built as a 3-stage image (deps → builder → runner) using Next.js standalone output. See the root `DEPLOYMENT.md`.
