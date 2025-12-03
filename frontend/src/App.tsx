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
    // Initialize from localStorage - check if token exists
    const token = localStorage.getItem("authToken");
    return !!token;
  });
  const [authView, setAuthView] = useState<"login" | "signup">("login");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const handleLogin = (token: string, user: any) => {
    // Store token and user info
    localStorage.setItem("authToken", token);
    localStorage.setItem("user", JSON.stringify(user));
    setIsAuthenticated(true);
  };

  const handleSignup = (token: string, user: any) => {
    // Store token and user info
    localStorage.setItem("authToken", token);
    localStorage.setItem("user", JSON.stringify(user));
    setIsAuthenticated(true);
  };

  const handleLogout = async () => {
    const token = localStorage.getItem("authToken");

    // Call backend logout API
    if (token) {
      try {
        await fetch("http://localhost:8080/logout", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
      } catch (error) {
        console.error("Logout error:", error);
      }
    }

    // Clear local storage and state
    localStorage.removeItem("authToken");
    localStorage.removeItem("user");
    setIsAuthenticated(false);
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
      <Sidebar
        activePage={activePage}
        onPageChange={(pageId) => {
          setActivePage(pageId);
          setIsSidebarOpen(false); // Close sidebar on mobile after selection
        }}
        onLogout={handleLogout}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header 
          onLogout={handleLogout}
          onMenuClick={() => setIsSidebarOpen(!isSidebarOpen)}
        />

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6">{renderPage()}</main>
      </div>
    </div>
  );
}

export default App;
