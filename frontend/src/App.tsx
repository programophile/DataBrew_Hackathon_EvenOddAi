import { useState, useEffect } from "react";
import { Sidebar } from "./components/dashboard/Sidebar";
import { Header } from "./components/dashboard/Header";
import { DashboardPage } from "./components/pages/DashboardPage";
import { SalesAnalyticsPage } from "./components/pages/SalesAnalyticsPage";
import { InventoryPage } from "./components/pages/InventoryPage";
import { StaffManagementPage } from "./components/pages/StaffManagementPage";
import { AIInsightsPage } from "./components/pages/AIInsightsPage";
import { IngredientsPage } from "./components/pages/IngredientsPage";
import { SettingsPage } from "./components/pages/SettingsPage";
import { LoginPage } from "./components/auth/LoginPage";
import { SignupPage } from "./components/auth/SignupPage";

function App() {
  const [activePage, setActivePage] = useState("dashboard");
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    // Initialize from localStorage
    const saved = localStorage.getItem("isAuthenticated");
    return saved === "true";
  });
  const [authView, setAuthView] = useState<"login" | "signup">("login");

  // Persist authentication state
  useEffect(() => {
    localStorage.setItem("isAuthenticated", String(isAuthenticated));
  }, [isAuthenticated]);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleSignup = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem("isAuthenticated");
    setAuthView("login");
  };

  // If not authenticated, show login/signup pages
  if (!isAuthenticated) {
    if (authView === "login") {
      return (
        <LoginPage
          onLogin={handleLogin}
          onSwitchToSignup={() => setAuthView("signup")}
        />
      );
    } else {
      return (
        <SignupPage
          onSignup={handleSignup}
          onSwitchToLogin={() => setAuthView("login")}
        />
      );
    }
  }

  const renderPage = () => {
    switch (activePage) {
      case "dashboard":
        return <DashboardPage />;
      case "sales":
        return <SalesAnalyticsPage />;
      case "inventory":
        return <InventoryPage />;
      case "ingredients":
        return <IngredientsPage />;
      case "staff":
        return <StaffManagementPage />;
      case "ai-insights":
        return <AIInsightsPage />;
      case "settings":
        return <SettingsPage />;
      default:
        return <DashboardPage />;
    }
  };

  return (
    <div className="flex h-screen bg-[#f9f5f2] overflow-hidden">
      {/* Sidebar */}
      <Sidebar activePage={activePage} onPageChange={setActivePage} />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header onLogout={handleLogout} />

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto p-6">{renderPage()}</main>
      </div>
    </div>
  );
}

export default App;
