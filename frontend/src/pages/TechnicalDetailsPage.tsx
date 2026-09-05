import PageHeader from "../components/common/PageHeader.tsx";
import DataFreshnessNotice from "../components/prediction/DataFreshnessNotice.tsx";
import TechnicalDetailsCard from "../components/technical_details/TechnicalDetailsCard.tsx";
import TechnicalDetailsSection from "../components/technical_details/TechnicalDetailsSection.tsx";
import TechnicalDetailsLoadingSkeleton from "../components/technical_details/TechnicalDetailsLoadingSkeleton.tsx";

import usePrediction from "../hooks/usePrediction.ts";
import useTechnicalDetails from "../hooks/useTechnicalDetails.ts";

function TechnicalDetailsPage() {
  const { prediction } = usePrediction();

  const {
    technicalDetails,
    loading,
  } = useTechnicalDetails(prediction?.ts);

  return (
    <>
      <PageHeader
        title="Technical Details"
        subtitle="Aura AQI Prediction System"
      />

      {loading && (
        <TechnicalDetailsLoadingSkeleton />
      )}

      {!loading && prediction && (
        <DataFreshnessNotice
          date={prediction.ts}
        />
      )}

      {!loading &&
        technicalDetails?.models.map(
          (model, index) => (
            <TechnicalDetailsSection
              key={model.model_name}
              day={index + 1}
              defaultOpen={index === 0}
            >
              <TechnicalDetailsCard
                day={index + 1}
                model={model}
              />
            </TechnicalDetailsSection>
          ),
        )}
    </>
  );
}

export default TechnicalDetailsPage;