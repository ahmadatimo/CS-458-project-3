import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

export default function SuccessfulLogin() {
  const navigate = useNavigate();

 
  const handleLogout = async () => {
      try {
        const response = await fetch("http://localhost:8000/logout", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });
    
        const data = await response.json();
        if (response.ok) {
          toast.success("✅ Logout Successful!", { position: "top-center" });
          localStorage.removeItem("auth_token"); // Clear token
          setTimeout(() => {
            navigate("/"); // Redirect to login page
          }, 1000);
        } else {
          toast.error(data.detail || "Failed to log out.", { position: "top-center" });
        }
      } catch (err) {
        toast.error("⚠️ Unable to connect to the server.", { position: "top-center" });
      }
    };

  return (
    <div className="flex h-screen items-center justify-center bg-gradient-to-r from-green-400 to-blue-500">
      <div className="bg-white p-8 shadow-2xl rounded-2xl w-96 text-center">
        <h2 className="text-4xl font-extrabold text-gray-800 mb-4">✅ Success!</h2>
        <p className="text-gray-600 text-lg mb-6">You have successfully logged in.</p>

        <button
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition duration-300"
          onClick={handleLogout} // Call logout function on click
        >
          Go to Login Page
        </button>
      </div>
    </div>
  );
}
