import "./BackfillButton.css";

type BackfillButtonProps = {
  disabled: boolean;
  onClick: () => void;
  label?: string;
};

function BackfillButton({
  disabled,
  onClick,
  label,
}: BackfillButtonProps) {
  return (
    <button
      className="backfill-button"
      type="button"
      disabled={disabled}
      onClick={onClick}
    >
      {label ??
        (disabled
          ? "Processing..."
          : "Run Backfill")}
    </button>
  );
}

export default BackfillButton;