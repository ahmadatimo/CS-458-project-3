// components/OptionInputGroupComponent.tsx
import React from "react";

interface Props {
  optionsList: string[];
  setOptionsList: (value: string[]) => void;
}

const OptionInputGroupComponent: React.FC<Props> = ({ optionsList, setOptionsList }) => {
  const handleOptionChange = (index: number, value: string) => {
    const updated = [...optionsList];
    updated[index] = value;
    setOptionsList(updated);
  };

  const addOptionField = () => {
    setOptionsList([...optionsList, ""]);
  };

  const removeOptionField = (index: number) => {
    const updated = optionsList.filter((_, i) => i !== index);
    setOptionsList(updated);
  };

  return (
    <div className="col-span-2 space-y-2">
      <p className="text-sm font-medium text-gray-700">Options</p>
      {optionsList.map((opt, index) => (
  <div key={index} className="flex gap-2">
    <input
      data-testid={`option-input-${index}`}
      type="text"
      value={opt}
      onChange={(e) => handleOptionChange(index, e.target.value)}
      className="border border-indigo-200 rounded-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-indigo-300"
      placeholder={`Option ${index + 1}`}
    />
    {optionsList.length > 1 && (
      <button
        type="button"
        onClick={() => removeOptionField(index)}
        className="px-3 text-red-500 hover:text-red-700"
      >
        ✖
      </button>
    )}
  </div>
))}

<button
  data-testid="add-option-button"
  type="button"
  onClick={addOptionField}
  className="text-indigo-600 text-sm hover:underline"
>
  ➕ Add another option
</button>
    </div>
  );
};

export default OptionInputGroupComponent;
