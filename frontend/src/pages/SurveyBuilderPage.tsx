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
  condition?: {
    dependentQuestionId: string;
    requiredAnswers: string[];
    matchType?: "any" | "all";
  } | null;
}

const SurveyBuilderPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const [questions, setQuestions] = useState<Question[]>([]);
  const [label, setLabel] = useState("");
  const [type, setType] = useState("text");
  const [optionsList, setOptionsList] = useState<string[]>([""]);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [questionError, setQuestionError] = useState("");

  // condition holds parsed answers; rawAnswers holds the free-form input string
  const [condition, setCondition] = useState<{
    dependentQuestionId: string;
    requiredAnswers: string[];
    matchType?: "any" | "all";
  } | null>(null);
  const [rawAnswers, setRawAnswers] = useState<string>("");

  // sync rawAnswers when condition changes
  useEffect(() => {
    if (condition) {
      setRawAnswers(condition.requiredAnswers.join(","));
    } else {
      setRawAnswers("");
    }
  }, [condition]);

  useEffect(() => {
    if (location.state?.questions) {
      setQuestions(location.state.questions);
    }
  }, [location.state]);

  const addQuestion = () => {
  if (!label.trim()) {
    setQuestionError("Question label is required.");
    return;
  }

  if (["multiple_choice", "checkbox", "dropdown"].includes(type)) {
    const cleaned = optionsList.map(opt => opt.trim()).filter(opt => opt !== "");
    const unique = Array.from(new Set(cleaned));
    if (unique.length < 2) {
      setQuestionError("Please provide at least two unique options.");
      return;
    }
  }

  const newQuestion: Question = {
    id: editingId || uuidv4(),
    label,
    type,
    options: ["multiple_choice", "checkbox", "dropdown"].includes(type)
      ? optionsList.filter(opt => opt.trim() !== "")
      : undefined,
    condition,
  };

  setQuestions(prev =>
    editingId
      ? prev.map(q => (q.id === editingId ? newQuestion : q))
      : [...prev, newQuestion]
  );

  // Clear form and error
  setLabel("");
  setType("text");
  setOptionsList([""]);
  setCondition(null);
  setEditingId(null);
  setRawAnswers("");
  setQuestionError("");
};



  const handleEdit = (question: Question) => {
    setLabel(question.label);
    setType(question.type);
    setOptionsList(question.options || [""]);
    setCondition(question.condition ? { ...question.condition } : null);
    setEditingId(question.id);
  };

  const handleDelete = (id: string) => {
    setQuestions(prev => prev.filter(q => q.id !== id));
  };

  const handleNormalSurvey = () => navigate("/Survey");
  const handleCreateSurvey = () => navigate("/Created-Survey", { state: { questions } });

  // only earlier questions allowed as dependencies
  const availableDeps = editingId
    ? questions.filter((_, idx) => idx < questions.findIndex(x => x.id === editingId))
    : questions;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-100 to-pink-50 py-10 px-6">
      <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-2xl p-6 sm:p-10 space-y-6 border border-gray-200">
        <h1 className="text-3xl sm:text-4xl font-extrabold text-indigo-700 flex items-center gap-3">
          <span>🔨</span> Design Your Own Survey
        </h1>

        <QuestionInput label={label} setLabel={setLabel} type={type} setType={setType} />

        { ["multiple_choice", "checkbox", "dropdown"].includes(type) && (
          <OptionInputGroup optionsList={optionsList} setOptionsList={setOptionsList} />
        ) }

        {/* Appear upon responding (Optional) */}
        <div className="space-y-4">
          <label className="block text-sm sm:text-base font-medium text-gray-700">
            Appear upon responding (Optional)
          </label>

          <select
            data-testid="condition-select"
            value={condition?.dependentQuestionId || ""}
            onChange={e => {
              const depId = e.target.value;
              setCondition(
                depId
                  ? { dependentQuestionId: depId, requiredAnswers: [], matchType: "any" }
                  : null
              );
            }}
            className="w-full sm:w-1/2 border px-3 py-2 rounded-lg mb-2"
          >
            <option value="">Select dependent question</option>
            {availableDeps.map(q => (
              <option key={q.id} 
              value={q.id}
              data-testid={`condition-option-${q.label.toLowerCase().replace(/\s+/g, '-')}`}>
                {q.label}
              </option>
            ))}
          </select>

          {condition?.dependentQuestionId && (() => {
            const depQ = questions.find(q => q.id === condition.dependentQuestionId);
            if (depQ?.options) {
              // checkbox: multi-select plus matchType toggle
              if (depQ.type === "checkbox") {
                return (
                  <>
                    <div className="flex flex-wrap gap-2">
                      {depQ.options.map(opt => (
                        <label key={opt} className="inline-flex items-center gap-1">
                          <input
                            type="checkbox"
                            checked={condition.requiredAnswers.includes(opt)}
                            onChange={e => {
                              const checked = e.target.checked;
                              const newVals = checked
                                ? [...condition.requiredAnswers, opt]
                                : condition.requiredAnswers.filter(v => v !== opt);
                              setCondition({ ...condition, requiredAnswers: newVals });
                            }}
                          />
                          {opt}
                        </label>
                      ))}
                    </div>
                    <div className="mt-2 flex gap-4">
                      <label className="inline-flex items-center">
                        <input
                          type="radio"
                          name="matchType"
                          value="any"
                          checked={(condition.matchType ?? "any") === "any"}
                          onChange={() =>
                            setCondition({ ...condition, matchType: "any" })
                          }
                        />
                        <span className="ml-1">Match any</span>
                      </label>
                      <label className="inline-flex items-center">
                        <input
                          type="radio"
                          name="matchType"
                          value="all"
                          checked={condition.matchType === "all"}
                          onChange={() =>
                            setCondition({ ...condition, matchType: "all" })
                          }
                        />
                        <span className="ml-1">Match all</span>
                      </label>
                    </div>
                  </>
                );
              }
              // multiple-choice or dropdown: single-select radios
              return (
                <div className="flex flex-wrap gap-2">
                  {depQ.options.map(opt => (
                    <label key={opt} className="inline-flex items-center gap-1">
                      <input
                        type="radio"
                        name="condition-select"
                        checked={condition.requiredAnswers[0] === opt}
                        onChange={() => setCondition({ ...condition, requiredAnswers: [opt] })}
                      />
                      {opt}
                    </label>
                  ))}
                </div>
              );
            }
            // fallback free-form input
            return (
              <input
                type="text"
                placeholder="Required answers (comma-separated)"
                value={rawAnswers}
                onChange={e => setRawAnswers(e.target.value)}
                onBlur={() => {
                  const vals = rawAnswers
                    .split(',')
                    .map(s => s.trim())
                    .filter(s => s);
                  setCondition({ ...condition, requiredAnswers: vals });
                  setRawAnswers(vals.join(','));
                }}
                className="w-full sm:w-1/2 border px-3 py-2 rounded-lg"
              />
            );
          })()}
        </div>

        <button
          id="add-question-button"
          type="button"
          onClick={addQuestion}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 rounded-lg font-semibold transition sm:w-auto sm:px-6"
        >
          {editingId ? "✏️ Update Question" : "➕ Add Question"}
        </button>
          {questionError && (
            <p className="text-sm text-red-500 mt-1" id="question-error">
          {questionError}
          </p>
        )}
        <div className="space-y-6">
          <h2 className="text-xl sm:text-2xl font-semibold flex items-center gap-2 text-indigo-800">
            📝 Preview Survey
          </h2>
          {questions.length === 0 ? (
            <p className="text-gray-500">No questions yet.</p>
          ) : (
            questions.map((q, index) => (
              <PreviewQuestion key={q.id} index={index} question={q} onEdit={handleEdit} onDelete={handleDelete} />
            ))
          )}
        </div>

        <div className="flex flex-col sm:flex-row justify-center items-center gap-6 pt-6">
          <button onClick={handleNormalSurvey} className="w-full sm:w-60 bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300 font-semibold text-lg">
            🔙 Normal Survey
          </button>
          <button onClick={handleCreateSurvey} className="w-full sm:w-48 bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 font-semibold text-lg">
            🧪 Fill Survey
          </button>
          <button
            onClick={async () => {
              try {
                const res = await fetch("http://localhost:8000/logout", {
                  method: "POST",
                  credentials: "include",
                });
                if (res.ok) {
                  localStorage.removeItem("auth_token");
                  window.location.href = "/login";
                } else {
                  const data = await res.json();
                  alert(data.detail || "Logout failed.");
                }
              } catch {
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
