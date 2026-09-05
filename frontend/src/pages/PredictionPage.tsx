import PageHeader from "../components/common/PageHeader.tsx";
import PredictionCards from "../components/prediction/PredictionCards.tsx";
import PredictionSection from "../components/prediction/PredictionSection.tsx";
import TrendSection from "../components/prediction/TrendSection.tsx";
import DataFreshnessNotice from "../components/prediction/DataFreshnessNotice.tsx";
import PredictionLoadingSkeleton from "../components/prediction/PredictionLoadingSkeleton.tsx";

import usePrediction from "../hooks/usePrediction";

function PredictionPage() {
  const {
    prediction,
    loading,
    refreshPrediction,
  } = usePrediction();

  return (
    <>
      <PageHeader
        title="Prediction"
        subtitle="Lahore"
      />

      <PredictionSection
        onRefresh={refreshPrediction}
        loading={loading}
      />

      {loading && !prediction && (
        <PredictionLoadingSkeleton />
      )}

      {prediction && (
        <>
          <DataFreshnessNotice
            date={prediction.ts}
          />

          <PredictionCards data={prediction} />

          <TrendSection data={prediction} />
        </>
      )}
    </>
  );
}

export default PredictionPage;