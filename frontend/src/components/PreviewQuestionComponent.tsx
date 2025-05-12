// components/PreviewQuestionComponent.tsx
import React from "react";
import { Question } from "../pages/SurveyBuilderPage";

interface Props {
  index: number;
  question: Question;
  onEdit: (q: Question) => void;
  onDelete: (id: string) => void;
}

const PreviewQuestionComponent: React.FC<Props> = ({ index, question, onEdit, onDelete }) => {
  return (
    <div className="p-4 border border-indigo-100 rounded-lg bg-indigo-50"
    data-testid={`preview-question-${question.id}`}>
      <div className="flex justify-between items-center">
        <p className="font-medium text-gray-800">
          {index + 1}. {question.label}{" "}
          <span className="text-sm text-indigo-600">[{question.type}]</span>
        </p>
        <div className="flex gap-3">
          <button
            onClick={() => onEdit(question)}
            data-testid={`edit-button-${question.id}`}
            title="Edit Question"
            className="text-blue-600 hover:underline text-sm"
          >
            ✏️ Edit
          </button>
          <button
            onClick={() => onDelete(question.id)}
            className="text-red-600 hover:underline text-sm"
          >
            🗑️ Delete
          </button>
        </div>
      </div>
      {question.options && (
        <ul className="ml-4 mt-2 list-disc text-gray-700 text-sm">
          {question.options.map((opt, i) => (
            <li key={i}>{opt}</li>
          ))}
        </ul>
      )}
      {question.type === "rating" && (
        <div className="flex space-x-1 mt-2">
          {[1, 2, 3, 4, 5].map((num) => (
            <span
              key={num}
              className="px-2 py-1 bg-yellow-300 rounded text-sm text-black"
            >
              {num}
            </span>
          ))}
        </div>
      )}
    </div>
  );
};

export default PreviewQuestionComponent;
