import { Route, createBrowserRouter, createRoutesFromElements, RouterProvider } from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import SuccessfulLogin from "./pages/SuccessfulPage";


export default function App() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        {/* HomePage is the default page */}
        <Route path="/" element={<LoginPage />} />
        <Route path="/login" element={<LoginPage />} /> {/* Explicit route for /login */}
        <Route path="/successful" element={<SuccessfulLogin />} />
      </>
    )
  );

  return <RouterProvider router={router} />;
}


