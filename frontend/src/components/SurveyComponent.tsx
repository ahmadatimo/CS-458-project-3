import React, { useEffect, useState } from "react";
import axios from "axios";

const educationLevels = [
  "Primary School",
  "Middle School",
  "High School",
  "Undergraduate",
  "Postgraduate",
  "PhD",
];

const availableAIModels = ["ChatGPT", "Bard", "Gemini", "Claude", "DeepSeek"];

const SurveyForm: React.FC = () => {
  const [form, setForm] = useState({
    name_surname: "",
    birth_day: "",
    birth_month: "",
    birth_year: "",
    education_level: "",
    city: "",
    gender: "",
    ai_models: [] as string[],
    defects: {} as Record<string, string>,
    beneficial_use: "",
    email: "",
  });

  const [birthDate, setBirthDate] = useState<string | null>(null);
  const [submitEnabled, setSubmitEnabled] = useState(false);
  const maxLength = 150;
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Validate age
  useEffect(() => {
    const { birth_day, birth_month, birth_year } = form;
    const day = parseInt(birth_day);
    const month = parseInt(birth_month);
    const year = parseInt(birth_year);
    try {
      const date = new Date(year, month - 1, day);
      const age = new Date().getFullYear() - year;
      if (age >= 6 && age <= 120) {
        setBirthDate(date.toISOString().split("T")[0]);
      } else {
        setBirthDate(null);
      }
    } catch {
      setBirthDate(null);
    }
  }, [form.birth_day, form.birth_month, form.birth_year]);

  useEffect(() => {
    const valid =
      form.name_surname &&
      birthDate &&
      form.education_level &&
      form.city &&
      form.gender &&
      form.ai_models.length > 0 &&
      form.ai_models.every((model) => form.defects[model]?.length > 0) &&
      form.beneficial_use &&
      form.email.includes("@") &&
      form.email.includes(".");
    setSubmitEnabled(Boolean(valid));
  }, [form, birthDate]);

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleModelToggle = (model: string) => {
    setForm((prev) => {
      const updated = [...prev.ai_models];
      const defects = { ...prev.defects };
      if (updated.includes(model)) {
        updated.splice(updated.indexOf(model), 1);
        delete defects[model];
      } else {
        updated.push(model);
        defects[model] = "";
      }
      return { ...prev, ai_models: updated, defects };
    });
  };

  const handleDefectChange = (model: string, value: string) => {
    setForm((prev) => ({
      ...prev,
      defects: { ...prev.defects, [model]: value },
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!submitEnabled || !birthDate) return;

    setIsSubmitting(true);

    try {
      const payload = {
        name_surname: form.name_surname,
        birth_date: birthDate,
        education_level: form.education_level,
        city: form.city,
        gender: form.gender,
        ai_models: form.ai_models,
        defects: form.defects, // <-- pass as actual object,
        beneficial_use: form.beneficial_use,
        email: form.email,
      };

      const res = await axios.post("http://localhost:8000/survey", payload);

      alert(
        typeof res.data === "string" ? res.data : JSON.stringify(res.data) // ✅ display real message, not [object Object]
      );
    } catch (err: any) {
      const errorMsg =
        err.response?.data?.detail || "Something went wrong during submission.";
      alert(JSON.stringify(errorMsg));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-3xl mx-auto bg-white shadow-lg rounded-2xl p-8 space-y-6"
    >
      <h2 className="text-2xl font-bold text-gray-800 text-center">
        AI Usage Survey
      </h2>

      <div>
        <label className="block mb-1 font-medium">Full Name</label>
        <input
          name="name_surname"
          onChange={handleChange}
          required
          className="w-full border px-4 py-2 rounded-lg"
        />
      </div>

      <div>
        <label className="block mb-1 font-medium">Birth Date</label>
        <div className="flex gap-2">
          <input
            name="birth_day"
            type="number"
            max={31}
            placeholder="DD"
            className="w-1/3 border px-4 py-2 rounded-lg"
            onChange={handleChange}
          />
          <input
            name="birth_month"
            type="number"
            max={12}
            placeholder="MM"
            className="w-1/3 border px-4 py-2 rounded-lg"
            onChange={handleChange}
          />
          <input
            name="birth_year"
            type="number"
            placeholder="YYYY"
            className="w-1/3 border px-4 py-2 rounded-lg"
            onChange={handleChange}
          />
        </div>
        {birthDate === null && (
          <p className="text-sm text-red-500 mt-1">
            Enter valid date (Age 6–120)
          </p>
        )}
      </div>

      <div>
        <label className="block mb-1 font-medium">Education Level</label>
        <select
          name="education_level"
          onChange={handleChange}
          required
          className="w-full border px-4 py-2 rounded-lg"
        >
          <option value="">Select</option>
          {educationLevels.map((level) => (
            <option key={level} value={level}>
              {level}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block mb-1 font-medium">City</label>
        <input
          name="city"
          onChange={handleChange}
          className="w-full border px-4 py-2 rounded-lg"
        />
      </div>

      <div>
        <label className="block mb-1 font-medium">Gender</label>
        <div className="flex gap-4">
          {[
            { label: "Male", value: "male" },
            { label: "Female", value: "female" },
          ].map(({ label, value }) => (
            <label key={value} className="flex items-center gap-2">
              <input
                type="radio"
                name="gender"
                value={value}
                checked={form.gender === value}
                onChange={handleChange}
              />
              {label}
            </label>
          ))}
        </div>
      </div>

      <div>
        <label className="block mb-2 font-medium">AI Models Used</label>
        <div className="flex flex-wrap gap-3">
          {availableAIModels.map((model, i) => {
            const selected = form.ai_models.includes(model);
            const colors = [
              "bg-pink-500",
              "bg-yellow-500",
              "bg-green-500",
              "bg-purple-500",
              "bg-blue-500",
            ];
            const bgColor = colors[i % colors.length];

            return (
              <button
                type="button"
                key={model}
                onClick={() => handleModelToggle(model)}
                className={`px-4 py-1 rounded-full text-sm font-medium transition ${
                  selected
                    ? `${bgColor} text-white shadow-md`
                    : "bg-gray-200 text-gray-800 hover:bg-gray-300"
                }`}
              >
                {model}
              </button>
            );
          })}
        </div>
      </div>

      {form.ai_models.length > 0 && (
        <div>
          <label className="block font-medium mb-2">Model Defects</label>
          {form.ai_models.map((model) => (
            <div key={model} className="mb-3">
              <input
                placeholder={`${model} - What are its flaws?`}
                value={form.defects[model]}
                onChange={(e) => handleDefectChange(model, e.target.value)}
                className="w-full border px-4 py-2 rounded-lg"
              />
            </div>
          ))}
        </div>
      )}

      <div>
        <label className="block font-medium mb-1">Beneficial Use of AI</label>
        <textarea
          name="beneficial_use"
          maxLength={maxLength}
          onChange={handleChange}
          className="w-full border px-4 py-2 rounded-lg h-24 resize-none"
        />
        <p className="text-sm text-gray-500">
          {maxLength - form.beneficial_use.length} characters left
        </p>
      </div>

      <div>
        <label className="block font-medium mb-1">Email</label>
        <input
          name="email"
          type="email"
          onChange={handleChange}
          className="w-full border px-4 py-2 rounded-lg"
        />
      </div>

      <button
        type="submit"
        disabled={!submitEnabled || isSubmitting}
        className={`w-full py-3 text-white font-semibold rounded-lg ${
          submitEnabled
            ? "bg-blue-600 hover:bg-blue-700"
            : "bg-gray-400 cursor-not-allowed"
        }`}
      >
        {isSubmitting ? "Submitting..." : "Submit Survey"}
      </button>
    </form>
  );
};

export default SurveyForm;
