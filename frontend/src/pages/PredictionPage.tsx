import PageHeader from "../components/prediction/PageHeader.tsx";
import PredictionCards from "../components/prediction/PredictionCards.tsx";
import PredictionSection from "../components/prediction/PredictionSection.tsx";
import TrendSection from "../components/prediction/TrendSection.tsx";

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

      {prediction && (
        <>
          <PredictionCards data={prediction} />
          <TrendSection data={prediction} />
        </>
      )}
    </>
  );
}

export default PredictionPage;