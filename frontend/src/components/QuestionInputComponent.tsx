// components/QuestionInputComponent.tsx
import React from "react";

interface Props {
  label: string;
  setLabel: (value: string) => void;
  type: string;
  setType: (value: string) => void;
}

const questionTypes = [
  { label: "Text Field", value: "text" },
  { label: "Multiple Choice", value: "multiple_choice" },
  { label: "Checkboxes", value: "checkbox" },
  { label: "Dropdown", value: "dropdown" },
  { label: "Rating Scale (1-5)", value: "rating" },
];

const QuestionInputComponent: React.FC<Props> = ({ label, setLabel, type, setType }) => {
  return (
    <div className="grid sm:grid-cols-2 gap-4">
      <input
        type="text"
        placeholder="Enter your question"
        value={label}
        onChange={(e) => setLabel(e.target.value)}
        className="border border-indigo-300 rounded-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
      <select
        value={type}
        onChange={(e) => setType(e.target.value)}
        className="border border-indigo-300 rounded-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-indigo-400"
      >
        {questionTypes.map((qt) => (
          <option key={qt.value} value={qt.value}>
            {qt.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default QuestionInputComponent;
