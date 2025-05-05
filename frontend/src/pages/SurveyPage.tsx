import React from "react";
import SurveyComponent from "../components/SurveyComponent.tsx";

const SurveyPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-100 py-10">
      <SurveyComponent />
    </div>
  );
};

export default SurveyPage;
