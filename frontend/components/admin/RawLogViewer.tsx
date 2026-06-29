import Card from "@/components/ui/Card";

type Props = {
  logText: string;
};

export default function RawLogViewer({ logText }: Props) {
  return (
    <Card>
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-lg font-semibold">Raw Log</h2>
        <span className="text-xs text-zinc-500">
          {logText.length.toLocaleString()} chars
        </span>
      </div>

      <pre className="max-h-[32rem] overflow-y-auto rounded bg-black p-4 text-xs text-zinc-300 whitespace-pre-wrap break-words">
        {logText}
      </pre>
    </Card>
  );
}
