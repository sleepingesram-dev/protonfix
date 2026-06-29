"use client";

import RedactionCard from "@/components/admin/RedactionCard";
import FingerprintCard from "@/components/admin/FingerprintCard";
import ParsedMetadata from "@/components/admin/ParsedMetadata";
import RawLogViewer from "@/components/admin/RawLogViewer";
import DiagnosisCard from "@/components/admin/DiagnosisCard";
import SubmissionMetadata from "@/components/admin/SubmissionMetadata";
import SubmissionHeader from "@/components/admin/SubmissionHeader";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getSubmission, diagnoseSubmission } from "@/lib/api";
import type { Submission, DiagnosisResult, RedactionReport } from "@/types/diagnosis";
import Card from "@/components/ui/Card";
import ErrorBanner from "@/components/ui/ErrorBanner";

const STATUS_COLORS: Record<string, string> = {
  pending: "bg-yellow-900 text-yellow-200",
  diagnosed: "bg-green-900 text-green-200",
  reviewed: "bg-blue-900 text-blue-200",
};

export default function AdminSubmissionPage() {
  const params = useParams<{ id: string }>();
  const subId = params.id;

  const [submission, setSubmission] = useState<Submission | null>(null);
  const [loading, setLoading] = useState(true);
  const [diagnosing, setDiagnosing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!subId) return;
    getSubmission(subId)
      .then(setSubmission)
      .catch((err) =>
        setError(
          err instanceof Error ? err.message : "Failed to load submission."
        )
      )
      .finally(() => setLoading(false));
  }, [subId]);

  async function runDiagnosis() {
    if (!subId) return;
    setDiagnosing(true);
    setError(null);
    try {
      const result = await diagnoseSubmission(subId);
      setSubmission((prev) =>
        prev ? { ...prev, diagnosis: result, status: "diagnosed" } : prev
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? `Diagnosis failed: ${err.message}`
          : "Diagnosis failed. Is the backend running?"
      );
    } finally {
      setDiagnosing(false);
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-zinc-950 p-8 text-white">
        <p className="text-zinc-400">Loading submission...</p>
      </main>
    );
  }

  if (!submission && !error) {
    return (
      <main className="min-h-screen bg-zinc-950 p-8 text-white">
        <p className="text-zinc-400">Submission not found.</p>
      </main>
    );
  }

  const diag: DiagnosisResult | undefined = submission?.diagnosis;
  const redaction: RedactionReport | undefined = submission?.redaction;

  return (
    <main className="min-h-screen bg-zinc-950 p-8 text-white">
      <div className="mx-auto max-w-5xl space-y-6">
        {submission && <SubmissionHeader submission={submission} />}

        {error && (
          <ErrorBanner message={error} onDismiss={() => setError(null)} />
        )}

        {submission && (
          <SubmissionMetadata
          submission={submission}
          redaction={redaction}
          diagnosing={diagnosing}
          onRunDiagnosis={runDiagnosis}
          />
        )}

        <RedactionCard redaction={redaction} />

        {diag && <DiagnosisCard diagnosis={diag} />}

        {diag && <ParsedMetadata parsed={diag.parsed} />}

        {diag && <FingerprintCard fingerprints={diag.parsed.fingerprints} />}

        {submission?.log_text && <RawLogViewer logText={submission.log_text} />}
      </div>
    </main>
  );
}
