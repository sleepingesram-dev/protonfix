import CopyButton from "@/components/ui/CopyButton";

type Props = {
  commands: string[];
};

export default function CommandBox({ commands }: Props) {
  if (!commands.length) {
    return (
      <p className="text-zinc-400">
        No commands recommended.
      </p>
    );
  }

  return (
    <>
      <div className="mb-3 flex items-center justify-between">
        <strong>Commands</strong>

        <CopyButton text={commands.join("\n")} />
      </div>

      <pre className="overflow-x-auto rounded-lg bg-black p-4 text-sm">
        {commands.join("\n")}
      </pre>
    </>
  );
}
