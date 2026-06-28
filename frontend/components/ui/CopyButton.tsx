"use client";

import { useState } from "react";

type CopyButtonProps = {
  text: string;
};

export default function CopyButton({ text }: CopyButtonProps) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    await navigator.clipboard.writeText(text);

    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 1500);
  }

  return (
    <button
      onClick={copy}
      className="rounded bg-zinc-800 px-3 py-1 text-sm font-semibold hover:bg-zinc-700"
    >
      {copied ? "Copied" : "Copy"}
    </button>
  );
}
