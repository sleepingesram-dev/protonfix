import type { DiagnosisResult, HistoryEntry, Stats } from "@/types/diagnosis";

const API_BASE_URL =
process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export async function analyzeLog(file: File): Promise<DiagnosisResult> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/analyze-log`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Failed to analyze log.");
    }

    return response.json();
}

export async function getStats(): Promise<Stats> {
    const response = await fetch(`${API_BASE_URL}/stats`);

    if (!response.ok) {
        throw new Error("Failed to load stats.");
    }

    return response.json();
}

export async function getHistory(): Promise<HistoryEntry[]> {
    const response = await fetch(`${API_BASE_URL}/history`);

    if (!response.ok) {
        throw new Error("Failed to load history.");
    }

    return response.json();
}

export async function getHistoryEntry(id: number | string): Promise<DiagnosisResult> {
    const response = await fetch(`${API_BASE_URL}/history/${id}`);

    if (!response.ok) {
        throw new Error("Failed to load diagnosis.");
    }

    return response.json();
}
