import React, { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import { useNavigate, useLocation } from "react-router-dom";
import QuestionInput from "../components/QuestionInputComponent";
import OptionInputGroup from "../components/OptionInputGroupComponent";
import PreviewQuestion from "../components/PreviewQuestionComponent";

export interface Question {
  id: string;
  label: string;
  type: string;
  options?: string[];
  condition?: { dependentQuestionId: string; requiredAnswer: string } | null;
}

const SurveyBuilderPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [label, setLabel] = useState("");
  const [type, setType] = useState("text");
  const [optionsList, setOptionsList] = useState<string[]>([""]);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [condition, setCondition] = useState<
    { dependentQuestionId: string; requiredAnswer: string } | null | undefined
  >(undefined);

  useEffect(() => {
    if (location.state?.questions) {
      setQuestions(location.state.questions);
    }
  }, [location.state]);

  const addQuestion = () => {
    if (!label.trim()) return;

    const newQuestion: Question = {
      id: editingId || uuidv4(),
      label,
      type,
      options: ["multiple_choice", "checkbox", "dropdown"].includes(type)
        ? optionsList.filter((opt) => opt.trim() !== "")
        : undefined,
      condition: condition,
    };

    setQuestions((prev) => {
      if (editingId) {
        return prev.map((q) => (q.id === editingId ? newQuestion : q));
      } else {
        return [...prev, newQuestion];
      }
    });

    setLabel("");
    setType("text");
    setOptionsList([""]);
    setCondition(null);
    setEditingId(null);
  };

  const handleEdit = (question: Question) => {
    setLabel(question.label);
    setType(question.type);
    setOptionsList(question.options || [""]);
    setCondition(question.condition);
    setEditingId(question.id);
  };

  const handleDelete = (id: string) => {
    setQuestions((prev) => prev.filter((q) => q.id !== id));
  };

  const handleNormalSurvey = () => {
    navigate("/Survey");
  };

  const handleCreateSurvey = () => {
    navigate("/Created-Survey", { state: { questions } });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-100 to-pink-50 py-10 px-6">
      <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-2xl p-6 sm:p-10 space-y-6 border border-gray-200">
        <h1 className="text-3xl sm:text-4xl font-extrabold text-indigo-700 flex items-center gap-3">
          <span>🔨</span> Design Your Own Survey
        </h1>

        <QuestionInput
          label={label}
          setLabel={setLabel}
          type={type}
          setType={setType}
        />

        {["multiple_choice", "checkbox", "dropdown"].includes(type) && (
          <OptionInputGroup
            optionsList={optionsList}
            setOptionsList={setOptionsList}
          />
        )}

        <div className="space-y-4">
          <label className="block text-sm sm:text-base font-medium text-gray-700">
            Conditional Logic (Optional)
          </label>
          <select
            value={condition?.dependentQuestionId || ""}
            onChange={(e) =>
              setCondition(
                e.target.value
                  ? {
                      dependentQuestionId: e.target.value,
                      requiredAnswer: condition?.requiredAnswer || "",
                    }
                  : null
              )
            }
            className="w-full sm:w-1/2 border px-3 py-2 rounded-lg mb-2"
          >
            <option value="">Select dependent question</option>
            {questions
              .filter((q) => q.id !== editingId)
              .map((q) => (
                <option key={q.id} value={q.id}>
                  {q.label}
                </option>
              ))}
          </select>
          {condition?.dependentQuestionId && (
            <input
              type="text"
              placeholder="Required answer to show this question"
              value={condition?.requiredAnswer || ""}
              onChange={(e) =>
                setCondition({
                  ...condition,
                  requiredAnswer: e.target.value,
                })
              }
              className="w-full sm:w-1/2 border px-3 py-2 rounded-lg"
            />
          )}
        </div>

        <button
          type="button"
          onClick={addQuestion}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 rounded-lg font-semibold transition sm:w-auto sm:px-6"
        >
          {editingId ? "✏️ Update Question" : "➕ Add Question"}
        </button>

        <div className="space-y-6">
          <h2 className="text-xl sm:text-2xl font-semibold flex items-center gap-2 text-indigo-800">
            📝 Preview Survey
          </h2>
          {questions.length === 0 ? (
            <p className="text-gray-500">No questions yet.</p>
          ) : (
            questions.map((q, index) => (
              <PreviewQuestion
                key={q.id}
                index={index}
                question={q}
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            ))
          )}
        </div>

        <div className="flex flex-col sm:flex-row justify-center items-center gap-6 pt-6">
          <button
            onClick={handleNormalSurvey}
            className="w-full sm:w-60 bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300 font-semibold text-lg"
          >
            🔙 Normal Survey
          </button>
          <button
            onClick={handleCreateSurvey}
            className="w-full sm:w-48 bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 font-semibold text-lg"
          >
            🧪 Fill Survey
          </button>
          <button
            onClick={async () => {
              try {
                const res = await fetch("http://localhost:8000/logout", {
                  method: "POST",
                  credentials: "include", // in case cookies/session is used
                });

                if (res.ok) {
                  localStorage.removeItem("auth_token"); // optional: remove stored token
                  window.location.href = "/login"; // or use navigate("/login")
                } else {
                  const data = await res.json();
                  alert(data.detail || "Logout failed.");
                }
              } catch (err) {
                alert("Error while logging out.");
              }
            }}
            className="w-full sm:w-36 bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 font-semibold text-lg"
          >
            🚪 Logout
          </button>
        </div>
      </div>
    </div>
  );
};

export default SurveyBuilderPage;
