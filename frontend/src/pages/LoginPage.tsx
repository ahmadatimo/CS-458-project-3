import { useState, useEffect } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import EmailPasswordLogin from "../components/NormalLoginComponent.tsx";
import GoogleLoginComponent from "../components/GoogleLoginComponent.tsx";
import { useNavigate } from "react-router-dom";
import SpotifyLoginComponent from "../components/SpotifyLoginComponent.tsx";

export default function LoginPage() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Handle Spotify login callback
  useEffect(() => {
    
    // Force logout by clearing the Spotify access token
    const forceLogout = async () => {
      try {
        await fetch('https://accounts.spotify.com/api/token', {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('spotify_access_token')}`
          }
        });

        localStorage.removeItem('spotify_access_token');
        window.location.href = '/login'; // Redirect to the login page
      } catch (error) {
        console.error('Error logging out from Spotify:', error);
      }
    };

    localStorage.removeItem("auth_token"); // Clear the authentication token

    const handleSpotifyCallback = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get("code");

      if (code) {
        setLoading(true);

        try {
          const response = await fetch("http://localhost:8000/spotify/callback", {
            method: "GET",
            headers: { "Content-Type": "application/json" },
          });

          const data = await response.json();
          if (response.ok) {
            toast.success("✅ Spotify Login Successful!", { position: "top-center" });
            localStorage.setItem("auth_token", data.user.spotify_id); // Store Spotify ID as token
            setTimeout(() => {
              navigate("/Successful"); // Redirect to the success page
            }, 2000);
          } else {
            toast.error(data.detail || "Failed to log in with Spotify.", { position: "top-center" });
          }
        } catch (err) {
          toast.error("⚠️ Unable to connect to the server.", { position: "top-center" });
        } finally {
          setLoading(false);
        }
      }
    };

    handleSpotifyCallback();
  }, [navigate]);

  // Handle email/password login
  const handleLogin = async (email: string, password: string) => {
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      if (response.ok) {
        toast.success("✅ Login Successful!", { position: "top-center" });
        localStorage.setItem("auth_token", data.token); // Store token from email/password login
        setTimeout(() => {
          navigate("/Successful");
        }, 1000);
      } else {
        toast.error(data.detail || "Invalid email or password.", { position: "top-center" });
      }
    } catch (err) {
      toast.error("⚠️ Unable to connect to the server.", { position: "top-center" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-gradient-to-r from-purple-600 to-blue-500">
      <ToastContainer />
      <div className="bg-white p-8 shadow-2xl rounded-2xl w-96">
        <h2 className="text-3xl font-extrabold text-center text-gray-800 mb-6">Sign In</h2>

        <EmailPasswordLogin onLogin={handleLogin} loading={loading} />

        <div className="mt-6 text-center space-y-3">
          <p className="text-gray-600 text-sm">Or login with</p>
          <GoogleLoginComponent />
          <SpotifyLoginComponent /> {/* Add Spotify Login Button */}
        </div>
      </div>
    </div>
  );
}
