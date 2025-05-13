import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

export default function GoogleLoginComponent() {
  const navigate = useNavigate();

  const handleGoogleSuccess = (credentialResponse: { credential?: string }) => {
    if (credentialResponse.credential) {
      const decoded = jwtDecode<{ name: string }>(credentialResponse.credential);
      console.log("Google User:", decoded);
      toast.success(`✅ Welcome, ${decoded.name}!`, { position: "top-center" });
      navigate("/Survey")
    } else {
      toast.error("❌ Google Login Failed: No credential received.", { position: "top-center" });
    }
  };

  const handleGoogleFailure = () => {
    toast.error("❌ Google Login Failed.", { position: "top-center" });
  };

  return (
    <GoogleOAuthProvider clientId="227145979883-8tabm5ujec4plc9q0ueidk5rignmoicm.apps.googleusercontent.com">
      <GoogleLogin onSuccess={handleGoogleSuccess} onError={handleGoogleFailure} />
    </GoogleOAuthProvider>
  );
}
