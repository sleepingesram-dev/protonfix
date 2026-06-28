"use client";

import { useState } from "react";
import type { DiagnosisResult } from "@/types/diagnosis";

type ExportButtonProps = {
  result: DiagnosisResult;
};

export default function ExportButton({ result }: ExportButtonProps) {
  const [copied, setCopied] = useState(false);

  function exportJson() {
    const blob = new Blob([JSON.stringify(result, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `protonfix-${result.filename.replace(/[^a-z0-9._-]/gi, "_")}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  async function copySummary() {
    const fp = result.parsed?.primary_fingerprint;
    const source = result.ai_used
      ? "AI Analysis"
      : result.used_known_issue
        ? "Known Issue Match"
        : "Deterministic Engine";

    const lines: string[] = [
      `ProtonFix Diagnosis`,
      `═══════════════════════════════`,
      `File:     ${result.filename}`,
      result.version ? `Version:  ProtonFix v${result.version}` : "",
      `Source:   ${source}`,
      `Severity: ${result.severity.toUpperCase()}`,
      fp ? `Confidence: ${fp.confidence}%` : `Confidence: ${result.confidence}`,
      ``,
      `Cause:`,
      result.probable_cause,
      ``,
      `Summary:`,
      result.summary,
    ];

    if (result.fix_steps.length > 0) {
      lines.push(``, `Fix Steps:`);
      result.fix_steps.forEach((s, i) => lines.push(`  ${i + 1}. ${s}`));
    }

    if (result.warnings.length > 0) {
      lines.push(``, `Warnings:`);
      result.warnings.forEach((w) => lines.push(`  • ${w}`));
    }

    await navigator.clipboard.writeText(
      lines.filter((l) => l !== "").join("\n")
    );
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  return (
    <div className="flex gap-2">
      <button
        onClick={exportJson}
        className="rounded-lg bg-zinc-800 px-3 py-2 text-sm font-semibold hover:bg-zinc-700"
      >
        Export JSON
      </button>
      <button
        onClick={copySummary}
        className="rounded-lg bg-zinc-800 px-3 py-2 text-sm font-semibold hover:bg-zinc-700"
      >
        {copied ? "Copied!" : "Copy Summary"}
      </button>
    </div>
  );
}
