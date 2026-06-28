export type Severity = "low" | "medium" | "high";
export type Confidence = "low" | "medium" | "high";

export interface FingerprintMetadata {
  display_name: string;
  short_description: string;
  icon: string;
}

export interface Fingerprint {
  fingerprint: string;
  category: string;
  severity: Severity;
  confidence: number;
  explanation: string;
  known_fix: string[];
  safe_commands: string[];
  metadata?: FingerprintMetadata;
}

export interface DiagnosisResult {
  filename: string;
  characters: number;

  summary: string;
  probable_cause: string;

  confidence: Confidence;
  severity: Severity;

  used_known_issue: boolean;
  known_issue_id?: string;

  detected_errors: string[];
  fix_steps: string[];
  recommended_commands: string[];
  extra_info_needed: string[];
  warnings: string[];

  parsed: {
    game: string | null;
    appid: string | null;
    proton_version: string | null;
    dxvk_version: string | null;
    vkd3d_version: string | null;
    gpu: string | null;
    errors: string[];
    fingerprints: Fingerprint[];
    primary_fingerprint: Fingerprint | null;
    dependency_chain: string[];
  };

  dependency_chain: string[];

  known_issue: unknown;
  ai_used: boolean;
  ai_result: unknown;
}

export interface Stats {
  total_logs: number;
  known_issue_used: number;
  ai_used: number;

  fingerprints: Record<string, number>;
  games: Record<string, number>;
  proton_versions: Record<string, number>;
  gpus: Record<string, number>;
  categories: Record<string, number>;
}

export interface HistoryEntry {
  id: number;
  timestamp: string;
  filename: string;
  game: string | null;
  appid: string | null;
  proton_version: string | null;
  primary_fingerprint: string | null;
  confidence: string;
  severity: string;
  summary: string;
  probable_cause: string;
}
