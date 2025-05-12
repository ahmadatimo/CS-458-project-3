import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Question } from "./SurveyBuilderPage";

interface Answer {
  [questionId: string]: string | string[];
}

const CreatedSurveyPage: React.FC = () => {
  const { state } = useLocation();
  const navigate = useNavigate();
  const questions: Question[] = state?.questions || [];
  const [answers, setAnswers] = useState<Answer>({});
  const [email, setEmail] = useState("");

  useEffect(() => {
    console.log("Received questions:", questions);
  }, [questions]);

  const handleChange = (id: string, value: string | string[]) => {
    setAnswers(prev => ({ ...prev, [id]: value }));
  };

  const shouldShowQuestion = (question: Question): boolean => {
    if (!question.condition) return true;
    const { dependentQuestionId, requiredAnswers, matchType = "any" } = question.condition;
    const userAnswer = answers[dependentQuestionId];
    if (userAnswer == null) return false;

    if (Array.isArray(userAnswer)) {
      if (matchType === "all") {
        // exact match: all required and no extras
        return (
          userAnswer.length === requiredAnswers.length &&
          requiredAnswers.every(ans => userAnswer.includes(ans))
        );
      } else {
        // any match: at least one required and no extras
        const hasAny = requiredAnswers.some(ans => userAnswer.includes(ans));
        const noExtras = userAnswer.every(ans => requiredAnswers.includes(ans));
        return hasAny && noExtras;
      }
    }

    return requiredAnswers.includes(userAnswer as string);
  };

  // Cleanup answers for hidden questions and their dependents
  useEffect(() => {
    const visibleIds = questions.filter(q => shouldShowQuestion(q)).map(q => q.id);
    setAnswers(prev => {
      const filteredEntries = Object.entries(prev).filter(([key]) => visibleIds.includes(key));
      const newState = Object.fromEntries(filteredEntries);
      const oldKeys = Object.keys(prev);
      const newKeys = Object.keys(newState);
      const equal = oldKeys.length === newKeys.length && oldKeys.every(k => newKeys.includes(k));
      return equal ? prev : newState;
    });
  }, [answers, questions]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) { alert("Please enter an email address."); return; }

    const surveyData = { questions, answers, email };
    try {
      const response = await fetch("http://localhost:8000/custom-survey", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(surveyData),
      });
      if (!response.ok) throw new Error((await response.json()).detail || "Failed to submit survey");
      alert("Survey submitted, stored, and email sent successfully!");
      handleLogout();
    } catch (err) {
      console.error(err);
      alert(`Error: ${err instanceof Error ? err.message : "Unknown error"}`);
    }
  };

  const handleEditSurvey = () => navigate("/builder", { state: { questions } });
  const handleNormalSurvey = () => navigate("/survey");
  const handleLogout = async () => {
    try {
      const res = await fetch("http://localhost:8000/logout", { method: "POST", credentials: "include" });
      if (res.ok) {
        localStorage.removeItem("auth_token");
        navigate("/login");
      } else {
        const data = await res.json();
        alert(data.detail || "Logout failed.");
      }
    } catch {
      alert("Error during logout.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 py-10 px-4 sm:px-6">
      <div className="max-w-3xl mx-auto bg-white rounded-xl shadow-lg p-6 sm:p-8 space-y-6 border border-gray-200">
        <h1 className="text-2xl sm:text-3xl font-bold text-purple-700">📋 Fill Your Custom Survey</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="block font-medium text-gray-800">Email Address</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full border px-3 py-2 rounded-lg sm:px-4"
              placeholder="Enter email to send results"
              required
            />
          </div>

          {questions.map(q =>
            shouldShowQuestion(q) ? (
              <div key={q.id} className="space-y-2">
                <label className="block font-medium text-gray-800">{q.label}</label>

                {q.type === "text" && (
                  <input
                    type="text"
                    onChange={e => handleChange(q.id, e.target.value)}
                    className="w-full border px-3 py-2 rounded-lg sm:px-4"
                  />
                )}

                {q.type === "multiple_choice" && q.options && (
                  <div className="space-y-1">
                    {q.options.map(opt => (
                      <label key={opt} className="block">
                        <input
                          type="radio"
                          name={q.id}
                          value={opt}
                          onChange={e => handleChange(q.id, e.target.value)}
                          className="mr-2"
                        />
                        {opt}
                      </label>
                    ))}
                  </div>
                )}

                {q.type === "checkbox" && q.options && (
                  <div className="space-y-1">
                    {q.options.map(opt => (
                      <label key={opt} className="block">
                        <input
                          type="checkbox"
                          value={opt}
                          onChange={e => {
                            const checked = e.target.checked;
                            setAnswers(prev => {
                              const current = Array.isArray(prev[q.id]) ? (prev[q.id] as string[]) : [];
                              const updated = checked ? [...current, opt] : current.filter(o => o !== opt);
                              return { ...prev, [q.id]: updated };
                            });
                          }}
                          className="mr-2"
                        />
                        {opt}
                      </label>
                    ))}
                  </div>
                )}

                {q.type === "dropdown" && q.options && (
                  <select
                    data-testid={`dropdown-${q.id}`}
                    onChange={e => handleChange(q.id, e.target.value)}
                    className="w-full border px-3 py-2 rounded-lg sm:px-4"
                  >
                    <option value="">Select...</option>
                    {q.options.map(opt => (
                      <option key={opt} value={opt}>{opt}</option>
                    ))}
                  </select>
                )}

                {q.type === "rating" && (
                  <div className="flex gap-2 flex-wrap sm:flex-nowrap">
                    {[1,2,3,4,5].map(num => (
                      <label key={num} className="flex items-center gap-1">
                        <input
                          type="radio"
                          name={q.id}
                          value={num}
                          onChange={e => handleChange(q.id, e.target.value)}
                        />
                        {num}
                      </label>
                    ))}
                  </div>
                )}
              </div>
            ) : null
          )}

          <div className="flex flex-wrap justify-center sm:justify-between gap-4 pt-6">
            <button type="button" onClick={handleLogout} className="w-full sm:w-auto bg-red-600 hover:bg-red-700 text-white py-2 px-6 rounded-lg font-semibold">🚪 Logout</button>
            <button type="button" onClick={handleEditSurvey} className="w-full sm:w-auto bg-yellow-500 hover:bg-yellow-600 text-white py-2 px-6 rounded-lg font-semibold">✏️ Edit Survey</button>
            <button type="submit" disabled={!email.includes("@") || !email.includes(".") || !email.includes("com")} className={`w-full sm:w-auto py-2 px-6 rounded-lg font-semibold transition ${(!email.includes("@") || !email.includes(".")) ? "bg-gray-400 text-white cursor-not-allowed" : "bg-purple-600 hover:bg-purple-700 text-white"}`}>✅ Submit</button>
            <button type="button" onClick={handleNormalSurvey} className="w-full sm:w-auto bg-gray-400 hover:bg-gray-500 text-white py-2 px-6 rounded-lg font-semibold">🔙 Normal Survey</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreatedSurveyPage;
