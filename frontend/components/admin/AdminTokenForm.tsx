"use client";

import { useState } from "react";
import { setAdminToken } from "@/lib/api";
import Card from "@/components/ui/Card";

type AdminTokenFormProps = {
  onSubmit: () => void;
};

export default function AdminTokenForm({ onSubmit }: AdminTokenFormProps) {
  const [token, setToken] = useState("");

  return (
    <Card>
      <h2 className="mb-2 text-xl font-bold">Admin token required</h2>
      <p className="mb-4 text-sm text-zinc-400">
        This backend is protected. Enter the admin token
        (PROTONFIX_ADMIN_TOKEN) to continue.
      </p>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (!token.trim()) return;
          setAdminToken(token.trim());
          onSubmit();
        }}
        className="flex gap-3"
      >
        <input
          type="password"
          value={token}
          onChange={(e) => setToken(e.target.value)}
          placeholder="Admin token"
          className="flex-1 rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2 text-sm text-white placeholder-zinc-600 focus:border-blue-500 focus:outline-none"
        />
        <button
          type="submit"
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold hover:bg-blue-500"
        >
          Unlock
        </button>
      </form>
    </Card>
  );
}
