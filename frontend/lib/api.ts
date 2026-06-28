import type { DiagnosisResult, HistoryEntry, RedactionReport, Stats, Submission } from "@/types/diagnosis";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

async function _fetch<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init);
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error((detail as { detail?: string })?.detail ?? `Request failed (${res.status})`);
  }
  return res.json() as Promise<T>;
}

export async function analyzeLog(file: File): Promise<DiagnosisResult> {
  const formData = new FormData();
  formData.append("file", file);
  return _fetch<DiagnosisResult>(`${API_BASE_URL}/analyze-log`, {
    method: "POST",
    body: formData,
  });
}

export async function submitLog(
  file: File,
  note: string
): Promise<{ submitted: boolean; submission_id: number; redaction?: RedactionReport }> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("note", note);
  return _fetch(`${API_BASE_URL}/submit`, { method: "POST", body: formData });
}

export async function getStats(): Promise<Stats> {
  return _fetch<Stats>(`${API_BASE_URL}/stats`);
}

export async function getHistory(): Promise<HistoryEntry[]> {
  return _fetch<HistoryEntry[]>(`${API_BASE_URL}/history`);
}

export async function getHistoryEntry(
  id: number | string
): Promise<DiagnosisResult> {
  return _fetch<DiagnosisResult>(`${API_BASE_URL}/history/${id}`);
}

export async function getSubmissions(): Promise<Submission[]> {
  return _fetch<Submission[]>(`${API_BASE_URL}/admin/submissions`);
}

export async function getSubmission(id: number | string): Promise<Submission> {
  return _fetch<Submission>(`${API_BASE_URL}/admin/submissions/${id}`);
}

export async function diagnoseSubmission(
  id: number | string
): Promise<DiagnosisResult> {
  return _fetch<DiagnosisResult>(
    `${API_BASE_URL}/admin/submissions/${id}/diagnose`,
    { method: "POST" }
  );
}
