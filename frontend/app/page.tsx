// Server Component — fully static, no client-side JS required.

import Link from "next/link";

// ── Static data ──────────────────────────────────────────────────────────────

const PIPELINE = [
  {
    n: "01",
    title: "Parse",
    body: "Raw log text is tokenised. Proton version, Steam AppID, game name, DXVK / Mesa build strings, and error messages are extracted into structured evidence.",
  },
  {
    n: "02",
    title: "Match fingerprints",
    body: "71 pattern definitions are evaluated against the extracted evidence. Each match is scored by severity, category priority, and co-occurrence weights.",
  },
  {
    n: "03",
    title: "Resolve root cause",
    body: "ROOT_CAUSE_GRAPH links fingerprints to their upstream causes. Downstream symptoms are pruned. The highest-ranked root node becomes the primary finding.",
  },
  {
    n: "04",
    title: "AI fallback — if needed",
    body: "When no fingerprint matches, GPT-4.1-mini is called with the structured parse context. Most logs never reach this step.",
  },
] as const;

const TECHNOLOGIES = [
  "Steam",
  "Proton",
  "Proton-GE",
  "Wine",
  "Wine-GE",
  "DXVK",
  "VKD3D-Proton",
  "Vulkan",
  "Mesa / RADV",
  "AMDGPU",
  "NVIDIA",
  "Intel ANV",
  "Gamescope",
  "GameMode",
  "MangoHud",
] as const;

const PRIVACY = [
  {
    title: "No account required",
    body: "Log submission is anonymous. No sign-up, no session cookies, no tracking pixels.",
  },
  {
    title: "IP stored as a hash",
    body: "Submission IP is converted to a 16-character SHA-256 truncation before being written to disk. The plain-text IP is never persisted.",
  },
  {
    title: "PII stripped before storage",
    body: "17 redaction categories run before every save: Linux and Windows home paths, Steam IDs, usernames, UUIDs, MAC addresses, hostnames, and email addresses.",
  },
  {
    title: "Data stays on your server",
    body: "Submissions are stored in SQLite on the host running ProtonFix. Nothing is forwarded to third parties except the optional OpenAI fallback call.",
  },
] as const;

const EXAMPLE_FIX = [
  "sudo apt install mesa-vulkan-drivers",
  "vulkaninfo",
  "Restart Steam after driver installation",
];

// ── Page ─────────────────────────────────────────────────────────────────────

export default function LandingPage() {
  return (
    <div className="bg-zinc-950 text-white">

      {/* ── Hero ─────────────────────────────────────────────────────────── */}
      <section
        aria-label="Introduction"
        className="border-b border-zinc-800 px-8 py-24"
      >
        <div className="mx-auto max-w-6xl">
          <p className="mb-4 text-sm font-semibold uppercase tracking-widest text-blue-400">
            Linux Gaming Troubleshooter
          </p>

          <h1 className="mb-4 text-6xl font-bold leading-none tracking-tight lg:text-8xl">
            ProtonFix
          </h1>

          <p className="mb-3 max-w-2xl text-xl font-semibold text-zinc-100">
            Deterministic log analysis for Linux gaming.
          </p>

          <p className="mb-10 max-w-2xl text-zinc-400">
            Upload a Steam, Proton, Wine, DXVK, VKD3D, or Vulkan log.
            ProtonFix runs 71 pattern fingerprints first. GPT-4.1-mini is only
            called when no fingerprint matches — not by default.
          </p>

          <div className="flex flex-wrap gap-3">
            <Link
              href="/analyze"
              className="rounded-xl bg-blue-600 px-7 py-3 font-bold transition hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-400"
            >
              Analyze a Log →
            </Link>
            <a
              href="https://github.com"
              aria-label="View ProtonFix on GitHub"
              className="rounded-xl border border-zinc-700 bg-zinc-900 px-7 py-3 font-bold transition hover:bg-zinc-800"
            >
              GitHub
            </a>
          </div>

          {/* Stats bar */}
          <div
            aria-label="Quick stats"
            className="mt-16 flex flex-wrap gap-x-10 gap-y-3 border-t border-zinc-800 pt-8 text-sm"
          >
            <span className="text-zinc-400">
              <strong className="text-white">71</strong> fingerprints
            </span>
            <span className="text-zinc-400">
              <strong className="text-white">17</strong> PII redaction categories
            </span>
            <span className="text-zinc-400">
              <strong className="text-white">MIT</strong> license
            </span>
            <span className="text-zinc-400">
              <strong className="text-white">SQLite</strong> — no external database
            </span>
            <span className="text-zinc-400">
              <strong className="text-white">Self-hosted</strong> — your data stays local
            </span>
          </div>
        </div>
      </section>

      {/* ── How it works ─────────────────────────────────────────────────── */}
      <section
        aria-labelledby="pipeline-heading"
        className="border-b border-zinc-800 px-8 py-20"
      >
        <div className="mx-auto max-w-6xl">
          <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-blue-400">
            Pipeline
          </p>
          <h2
            id="pipeline-heading"
            className="mb-12 text-3xl font-bold"
          >
            How ProtonFix works
          </h2>

          <div className="grid gap-px rounded-2xl border border-zinc-800 bg-zinc-800 md:grid-cols-2 lg:grid-cols-4">
            {PIPELINE.map(({ n, title, body }) => (
              <article
                key={n}
                className="rounded-none bg-zinc-950 p-6 first:rounded-tl-2xl first:rounded-tr-2xl last:rounded-bl-2xl last:rounded-br-2xl md:first:rounded-tl-2xl md:first:rounded-tr-none md:last:rounded-bl-none md:last:rounded-br-2xl lg:first:rounded-l-2xl lg:first:rounded-tr-none lg:last:rounded-r-2xl lg:last:rounded-bl-none"
              >
                <p className="mb-4 font-mono text-4xl font-bold text-blue-600">
                  {n}
                </p>
                <h3 className="mb-2 font-bold">{title}</h3>
                <p className="text-sm leading-relaxed text-zinc-400">{body}</p>
              </article>
            ))}
          </div>

          <p className="mt-8 max-w-2xl text-sm text-zinc-500">
            Steps 01–03 are fully deterministic — no network calls, no model
            inference. Step 04 is gated behind a check: if the fingerprint engine
            returns any result, the AI call is skipped entirely.
          </p>
        </div>
      </section>

      {/* ── Supported technologies ───────────────────────────────────────── */}
      <section
        aria-labelledby="tech-heading"
        className="border-b border-zinc-800 px-8 py-20"
      >
        <div className="mx-auto max-w-6xl">
          <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-blue-400">
            Coverage
          </p>
          <h2
            id="tech-heading"
            className="mb-3 text-3xl font-bold"
          >
            Supported technologies
          </h2>
          <p className="mb-10 max-w-2xl text-zinc-400">
            ProtonFix parses and cross-references log output from these runtimes,
            compatibility layers, and GPU stacks.
          </p>

          <ul
            aria-label="Supported technology list"
            className="flex flex-wrap gap-2"
          >
            {TECHNOLOGIES.map((tech) => (
              <li key={tech}>
                <span className="rounded-full border border-zinc-700 bg-zinc-900 px-4 py-1.5 text-sm font-medium text-zinc-200">
                  {tech}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* ── Example diagnosis ────────────────────────────────────────────── */}
      <section
        aria-labelledby="example-heading"
        className="border-b border-zinc-800 px-8 py-20"
      >
        <div className="mx-auto max-w-6xl">
          <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-blue-400">
            Example
          </p>
          <h2
            id="example-heading"
            className="mb-3 text-3xl font-bold"
          >
            What a diagnosis looks like
          </h2>
          <p className="mb-10 max-w-2xl text-zinc-400">
            A representative output from the deterministic engine. This result
            required zero AI calls — the root cause was matched directly from the
            log.
          </p>

          {/* Mock diagnosis card */}
          <div
            role="region"
            aria-label="Example diagnosis result"
            className="overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900"
          >
            {/* Card header */}
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-800 px-6 py-4">
              <h3 className="text-lg font-bold">Diagnosis</h3>
              <span className="rounded-lg border border-blue-700 bg-blue-950/60 px-3 py-1 text-sm font-semibold text-blue-300">
                ⚡ Deterministic Engine
              </span>
            </div>

            <div className="p-6">
              {/* Meta + probable cause */}
              <div className="mb-5 grid gap-4 md:grid-cols-2">
                <div className="space-y-2 rounded-lg border border-zinc-800 bg-zinc-950 p-4 text-sm">
                  <p>
                    <strong>File:</strong>{" "}
                    <span className="font-mono text-zinc-300">
                      steam_proton_620.log
                    </span>
                  </p>
                  <p>
                    <strong>Game:</strong> Portal 2
                  </p>
                  <p>
                    <strong>Proton:</strong> 8.0-5
                  </p>
                  <p>
                    <strong>Confidence:</strong> 91%
                  </p>
                  <p className="flex items-center gap-2">
                    <strong>Severity:</strong>
                    <span className="rounded bg-red-900 px-2 py-0.5 text-xs font-bold text-red-200">
                      🔴 HIGH
                    </span>
                  </p>
                </div>

                <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-400">
                    Summary
                  </p>
                  <p className="text-sm leading-relaxed text-zinc-300">
                    Vulkan initialisation failed immediately after launch. DXVK
                    could not create a Vulkan device, causing the renderer to
                    crash. Root cause matched from the ICD error string — no AI
                    fallback used.
                  </p>
                </div>
              </div>

              {/* Primary cause */}
              <div className="rounded-xl border border-blue-800 bg-zinc-950 p-5">
                <p className="mb-3 text-xs font-semibold uppercase tracking-widest text-blue-400">
                  Primary Cause
                </p>
                <h4 className="mb-1 text-xl font-bold">
                  Missing or Broken Vulkan Driver
                </h4>
                <p className="mb-1 font-mono text-xs text-zinc-500">
                  VULKAN_DRIVER_MISSING
                </p>
                <span className="mb-4 inline-block rounded bg-red-900 px-2 py-0.5 text-xs font-bold text-red-200">
                  🔴 HIGH
                </span>
                <p className="text-sm leading-relaxed text-zinc-300">
                  No Vulkan ICD loader was found at runtime. DXVK and VKD3D both
                  require a working Vulkan driver to initialise. This failure
                  blocks all DirectX translation layers.
                </p>

                <div className="mt-5">
                  <p className="mb-2 text-sm font-semibold">Known fixes</p>
                  <pre className="overflow-x-auto rounded-lg bg-black px-5 py-4 font-mono text-sm text-zinc-300">
{EXAMPLE_FIX.join("\n")}</pre>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Privacy ──────────────────────────────────────────────────────── */}
      <section
        aria-labelledby="privacy-heading"
        className="border-b border-zinc-800 px-8 py-20"
      >
        <div className="mx-auto max-w-6xl">
          <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-blue-400">
            Privacy
          </p>
          <h2
            id="privacy-heading"
            className="mb-3 text-3xl font-bold"
          >
            What gets collected
          </h2>
          <p className="mb-10 max-w-2xl text-zinc-400">
            Log submission is anonymous. PII is detected and removed automatically
            before anything is stored.
          </p>

          <div className="grid gap-4 sm:grid-cols-2">
            {PRIVACY.map(({ title, body }) => (
              <article
                key={title}
                className="rounded-xl border border-zinc-800 bg-zinc-900 p-5"
              >
                <h3 className="mb-2 font-bold">{title}</h3>
                <p className="text-sm leading-relaxed text-zinc-400">{body}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* ── Open source + Community ──────────────────────────────────────── */}
      <section
        aria-labelledby="community-heading"
        className="border-b border-zinc-800 px-8 py-20"
      >
        <div className="mx-auto max-w-6xl">
          <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-blue-400">
            Open Source
          </p>
          <h2
            id="community-heading"
            className="mb-3 text-3xl font-bold"
          >
            Built in the open
          </h2>
          <p className="mb-12 max-w-2xl text-zinc-400">
            The fingerprint database, causal dependency graph, and confidence
            scoring engine are plain Python dicts — no black boxes, no vendor
            lock-in.
          </p>

          <div className="grid gap-5 md:grid-cols-3">
            {/* MIT card */}
            <div className="flex flex-col rounded-xl border border-zinc-800 bg-zinc-900 p-6">
              <p className="mb-1 text-xs font-semibold uppercase tracking-widest text-zinc-500">
                License
              </p>
              <p className="mb-3 text-2xl font-bold">MIT</p>
              <p className="text-sm leading-relaxed text-zinc-400">
                Use it, fork it, embed it. The entire diagnosis engine is
                auditable source — no compiled weights, no opaque models.
              </p>
            </div>

            {/* GitHub card */}
            <a
              href="https://github.com"
              aria-label="View ProtonFix source on GitHub"
              className="group flex flex-col rounded-xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-blue-600/50 hover:bg-zinc-800"
            >
              <p className="mb-1 text-xs font-semibold uppercase tracking-widest text-zinc-500">
                GitHub
              </p>
              <p className="mb-3 text-2xl font-bold transition group-hover:text-blue-300">
                View source →
              </p>
              <p className="text-sm leading-relaxed text-zinc-400">
                Browse the fingerprint database, open an issue, or submit a pull
                request to add new patterns for games you&apos;ve diagnosed.
              </p>
            </a>

            {/* Discord card */}
            <a
              href="https://discord.com"
              aria-label="Join the ProtonFix Discord server"
              className="group flex flex-col rounded-xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-blue-600/50 hover:bg-zinc-800"
            >
              <p className="mb-1 text-xs font-semibold uppercase tracking-widest text-zinc-500">
                Discord
              </p>
              <p className="mb-3 text-2xl font-bold transition group-hover:text-blue-300">
                Join the server →
              </p>
              <p className="text-sm leading-relaxed text-zinc-400">
                Discuss Linux gaming failures, request new fingerprint patterns,
                and share diagnosis results with the community.
              </p>
            </a>
          </div>
        </div>
      </section>

      {/* ── Footer ───────────────────────────────────────────────────────── */}
      <footer className="px-8 py-10">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <div
              aria-hidden="true"
              className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 font-mono text-sm font-bold"
            >
              PF
            </div>
            <span className="text-sm text-zinc-400">
              ProtonFix · MIT License · Built for Linux gamers
            </span>
          </div>

          <nav aria-label="Footer navigation" className="flex flex-wrap gap-5 text-sm text-zinc-500">
            <Link href="/analyze" className="transition hover:text-zinc-200">
              Analyze
            </Link>
            <Link href="/history" className="transition hover:text-zinc-200">
              History
            </Link>
            <Link href="/stats" className="transition hover:text-zinc-200">
              Stats
            </Link>
            <Link href="/submit" className="transition hover:text-zinc-200">
              Submit Log
            </Link>
            <a
              href="https://github.com"
              className="transition hover:text-zinc-200"
            >
              GitHub
            </a>
          </nav>
        </div>
      </footer>

    </div>
  );
}
