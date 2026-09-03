import PageHeader from "../components/common/PageHeader.tsx";
import BackfillSection from "../components/backfill/BackfillSection";
import useBackfill from "../hooks/useBackfill";
import usePrediction from "../hooks/usePrediction";

function BackfillPage() {
  const {
    prediction,
    refreshPrediction,
  } = usePrediction();

  const {
    phase,
    progress,
    error,
    startBackfill,
  } = useBackfill(
    prediction?.ts ?? null,
    refreshPrediction,
  );

  return (
    <>
      <PageHeader
        title="Backfill"
        subtitle="Lahore"
      />

      <BackfillSection
        progress={progress}
        phase={phase}
        error={error}
        onBackfill={startBackfill}
      />
    </>
  );
}

export default BackfillPage;
