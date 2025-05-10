import { useState } from "react";

interface NormalLogin {
  onLogin: (email: string, password: string) => Promise<void>;
  loading: boolean;
}

export default function NormalLogin({ onLogin, loading }: NormalLogin) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email) {
      setError("Email is required.");
      return;
    }

    if (!password) {
      setError("Password is required.");
      return;
    }

    setError(""); // clear previous errors
    await onLogin(email, password);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        id="email"
        name="email"
        type="email"
        placeholder="Email"
        className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        id="password"
        name="password"
        type="password"
        placeholder="Password"
        className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      {error && (
        <p className="text-red-500 text-sm font-medium" id="login-error">
          {error}
        </p>
      )}

      <button
        id="login-button"
        name="submit"
        type="submit"
        className="w-full bg-blue-500 text-white p-3 rounded-lg font-semibold hover:bg-blue-600 transition duration-300"
        disabled={loading}
      >
        {loading ? "Logging in..." : "Login"}
      </button>
    </form>
  );
}
