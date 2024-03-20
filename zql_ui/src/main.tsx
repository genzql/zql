import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import ZqlApp from "./ZqlApp.tsx";
import TranslatorApp from "./TranslatorApp.tsx";
import "./index.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <ZqlApp />,
  },
  {
    path: "/translate",
    element: <TranslatorApp />,
  },
])

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
