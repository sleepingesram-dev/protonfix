"use client";

import RedactionCard from "@/components/admin/RedactionCard";
import FingerprintCard from "@/components/admin/FingerprintCard";
import ParsedMetadata from "@/components/admin/ParsedMetadata";
import RawLogViewer from "@/components/admin/RawLogViewer";
import DiagnosisCard from "@/components/admin/DiagnosisCard";
import SubmissionMetadata from "@/components/admin/SubmissionMetadata";
import SubmissionHeader from "@/components/admin/SubmissionHeader";
import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { ApiError, getSubmission, diagnoseSubmission } from "@/lib/api";
import type { Submission, DiagnosisResult, RedactionReport } from "@/types/diagnosis";
import ErrorBanner from "@/components/ui/ErrorBanner";
import AdminTokenForm from "@/components/admin/AdminTokenForm";

export default function AdminSubmissionPage() {
  const params = useParams<{ id: string }>();
  const subId = params.id;

  const [submission, setSubmission] = useState<Submission | null>(null);
  const [loading, setLoading] = useState(true);
  const [diagnosing, setDiagnosing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [unauthorized, setUnauthorized] = useState(false);

  const load = useCallback(() => {
    if (!subId) return;
    getSubmission(subId)
      .then((sub) => {
        setSubmission(sub);
        setUnauthorized(false);
        setError(null);
      })
      .catch((err) => {
        if (err instanceof ApiError && err.status === 401) {
          setUnauthorized(true);
        } else {
          setError(
            err instanceof Error ? err.message : "Failed to load submission."
          );
        }
      })
      .finally(() => setLoading(false));
  }, [subId]);

  useEffect(() => {
    load();
  }, [load]);

  function retry() {
    setLoading(true);
    setError(null);
    setUnauthorized(false);
    load();
  }

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

  if (unauthorized) {
    return (
      <main className="min-h-screen bg-zinc-950 p-8 text-white">
        <div className="mx-auto max-w-xl">
          <AdminTokenForm onSubmit={retry} />
        </div>
      </main>
    );
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
