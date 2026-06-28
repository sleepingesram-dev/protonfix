import { ReactNode } from "react";

type CardProps = {
  children: ReactNode;
  className?: string;
};

export default function Card({ children, className = "" }: CardProps) {
  return (
    <div
      className={`rounded-xl border border-zinc-800 bg-zinc-900 p-6 ${className}`}
    >
      {children}
    </div>
  );
}
