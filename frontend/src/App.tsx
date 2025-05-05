import { Route, createBrowserRouter, createRoutesFromElements, RouterProvider } from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import SurveyPage from "./pages/SurveyPage";


export default function App() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        {/* HomePage is the default page */}
        <Route path="/" element={<LoginPage />} />
        <Route path="/login" element={<LoginPage />} /> {/* Explicit route for /login */}
        <Route path="/survey" element={<SurveyPage />} />
      </>
    )
  );

  return <RouterProvider router={router} />;
}


