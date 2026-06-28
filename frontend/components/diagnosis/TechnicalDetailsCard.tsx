import type { DiagnosisResult } from "@/types/diagnosis";

type TechnicalDetailsCardProps = {
  result: DiagnosisResult;
};

export default function TechnicalDetailsCard({
  result,
}: TechnicalDetailsCardProps) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
      <h3 className="mb-3 text-xl font-bold">
        Technical Details
      </h3>

      <div className="grid gap-3 md:grid-cols-2">
        <p><strong>Game:</strong> {result.parsed.game || "Unknown"}</p>
        <p><strong>App ID:</strong> {result.parsed.appid || "Unknown"}</p>
        <p><strong>Proton:</strong> {result.parsed.proton_version || "Unknown"}</p>
        <p><strong>DXVK:</strong> {result.parsed.dxvk_version || "Unknown"}</p>
        <p><strong>VKD3D:</strong> {result.parsed.vkd3d_version || "Unknown"}</p>
        <p><strong>GPU:</strong> {result.parsed.gpu || "Unknown"}</p>
      </div>
    </div>
  );
}
