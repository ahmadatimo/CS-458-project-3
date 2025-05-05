import { Route, createBrowserRouter, createRoutesFromElements, RouterProvider } from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import SurveyPage from "./pages/SurveyPage";
import SurveyBuilderPage from "./pages/SurveyBuilderPage";
import CreatedSurveyPage from "./pages/CreatedSurveyPage";

export default function App() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        {/* HomePage is the default page */}
        <Route path="/" element={<LoginPage />} />
        <Route path="/Login" element={<LoginPage />} /> {/* Explicit route for /login */}
        <Route path="/Survey" element={<SurveyPage />} />
        <Route path="/Builder" element={<SurveyBuilderPage />} />
        <Route path="/Created-Survey" element={<CreatedSurveyPage />} /> {/* Explicit route for /successful */}
      </>
    )
  );

  return <RouterProvider router={router} />;
}


