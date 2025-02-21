import React, { useEffect, useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import "./App.css";
import MainComponent from "./Components/MainComponent";
import LoginPage from "./Components/LoginPage";
import ProtectedRoute from "./Components/ProtectedRoute"; 

import { AuthProvider } from "./Components/AuthContext";


import { useAuth } from "./Components/AuthContext";
import AdminDashboard from "./Pages/Admin/AdminDashboard";
import DoctorDashboard from "./Pages/Doctor/DoctorDashboard";
import LabDashboard from "./Pages/Lab/LabDashboard";
import ReceptionDashboard from "./Pages/Reception/ReceptionDashboard";

const LoadingSpinner = () => (
  <div className="loading-spinner">
    <div className="spinner"></div>
  </div>
);

const AuthenticatedLayout = () => (
  <div className="app-container">
    <MainComponent />
    <div className="content-container">
      <Routes>
        <Route element={<ProtectedRoute roles={['admin','doctor','lab','reception',"nurse","injection","raj","ultrasound"]} />}>
          <Route path="/" element={<AdminDashboard />} />
        </Route>
        
        <Route element={<ProtectedRoute roles={['admin']} />}>

        <Route path="/sell/view-sell" element={<AdminDashboard />} />

        </Route>

        <Route element={<ProtectedRoute roles={['doctor']} />}>

        <Route path="/sell/view-sell" element={<DoctorDashboard />} />

        </Route>

        <Route element={<ProtectedRoute roles={['lab']} />}>

        <Route path="/sell/view-sell" element={<LabDashboard />} />
        
        </Route>
        
        <Route element={<ProtectedRoute roles={['recept']} />}>

        <Route path="/sell/view-sell" element={<ReceptionDashboard />} />

        </Route>
                
        <Route path="/login" element={<LoginPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  </div>
);

const AppRoutes = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div>
          <MainComponent />

    <Routes>
      {!isAuthenticated ? (
        <>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<AdminDashboard />} />

          <Route path="*" element={<Navigate to="/login" replace />} />
        </>
      ) : (
        <Route path="*" element={<AuthenticatedLayout />} />
      )}
    </Routes>
    </div>
  );
};

function App() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadApp = async () => {
      // Simulate loading
      await new Promise(resolve => setTimeout(resolve, 2000));
      setIsLoading(false);
    };

    loadApp();
  }, []);

  return (
    <AuthProvider>
      {isLoading ? (
        <LoadingSpinner />
      ) : (
        <AppRoutes />
      )}
    </AuthProvider>
  );
}

export default App;
