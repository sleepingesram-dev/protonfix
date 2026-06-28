type ErrorBannerProps = {
  message: string;
  onDismiss?: () => void;
};

export default function ErrorBanner({ message, onDismiss }: ErrorBannerProps) {
  return (
    <div className="flex items-start gap-3 rounded-lg border border-red-800 bg-red-950/50 p-4">
      <span className="text-lg leading-none text-red-400">⚠</span>
      <p className="flex-1 text-sm text-red-200">{message}</p>
      {onDismiss && (
        <button
          onClick={onDismiss}
          aria-label="Dismiss"
          className="text-lg leading-none text-red-400 hover:text-red-300"
        >
          ×
        </button>
      )}
    </div>
  );
}
