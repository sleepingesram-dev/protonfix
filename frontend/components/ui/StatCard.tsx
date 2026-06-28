import Card from "@/components/ui/Card";

type Props = {
  title: string;
  value: string | number;
};

export default function StatCard({
  title,
  value,
}: Props) {
  return (
    <Card>
      <p className="text-zinc-400">
        {title}
      </p>

      <p className="mt-2 text-4xl font-bold">
        {value}
      </p>
    </Card>
  );
}
