import type { BackfillPhase } from "../../hooks/useBackfill";
import BackfillButton from "./BackfillButton";
import BackfillProgress from "./BackfillProgress";
import {
  BackfillIceTexture,
  BackfillIceTextureTopRight,
} from "./BackfillIceTexture";
import "./BackfillSection.css";

type BackfillSectionProps = {
  progress: number;
  phase: BackfillPhase;
  error: string | null;
  onBackfill: () => void;
};

function BackfillSection({
  progress,
  phase,
  error,
  onBackfill,
}: BackfillSectionProps) {
  const isRunning =
    phase === "raw" ||
    phase === "engineered" ||
    phase === "training";

  const isUpToDate =
    phase === "up-to-date";

  return (
    <section className="backfill-section">
      <div className="backfill-card">
        <BackfillIceTexture />
        <BackfillIceTextureTopRight />

        <BackfillProgress
          progress={progress}
          phase={phase}
          error={error}
        />

        <BackfillButton
          disabled={isRunning || isUpToDate}
          label={
            isUpToDate
              ? "Already Updated"
              : undefined
          }
          onClick={onBackfill}
        />
      </div>
    </section>
  );
}

export default BackfillSection;