import type { Submission } from "@/types/diagnosis";

type SubmissionHeaderProps = {
  submission: Submission;
};

export default function SubmissionHeader({
  submission,
}: SubmissionHeaderProps) {
  return (
    <div>
      <p className="mb-1 text-sm font-semibold uppercase tracking-wide text-blue-400">
        Admin — Submission #{submission.id}
      </p>

      <h1 className="mb-1 text-3xl font-bold">
        {submission.filename || "Unnamed log"}
      </h1>

      <p className="text-sm text-zinc-500">
        Submitted {submission.submitted_at?.slice(0, 16).replace("T", " ")} UTC
        · IP hash: <code className="font-mono">{submission.ip_hash}</code>
      </p>

      <a
        href="/admin"
        className="mt-3 inline-block text-sm text-blue-400 hover:text-blue-300"
      >
        ← All submissions
      </a>
    </div>
  );
}
