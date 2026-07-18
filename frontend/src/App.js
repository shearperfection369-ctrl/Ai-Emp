import "@/App.css";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { CartProvider } from "./context/CartContext";
import { Toaster } from "@/components/ui/sonner";

import StarField from "./components/StarField";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import AriaAssistant from "./components/AriaAssistant";
import AuthCallback from "./components/AuthCallback";
import ProtectedRoute from "./components/ProtectedRoute";

import Home from "./pages/Home";
import Marketplace from "./pages/Marketplace";
import ToolDetail from "./pages/ToolDetail";
import CartPage from "./pages/CartPage";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Library from "./pages/Library";
import AdminDashboard from "./pages/AdminDashboard";
import PaymentSuccess from "./pages/PaymentSuccess";
import PaymentCancel from "./pages/PaymentCancel";
import Branding from "./pages/Branding";

function AppRouter() {
  const location = useLocation();
  // Handle Emergent Google OAuth callback synchronously before anything else.
  if (location.hash?.includes("session_id=")) {
    return <AuthCallback />;
  }
  return (
    <div className="relative min-h-screen">
      <StarField />
      <div className="fixed inset-0 z-0 hud-grid pointer-events-none opacity-40" />
      <Navbar />
      <main className="relative z-10 pt-16">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/marketplace" element={<Marketplace />} />
          <Route path="/tool/:slug" element={<ToolDetail />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/branding" element={<Branding />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/payment/success" element={<PaymentSuccess />} />
          <Route path="/payment/cancel" element={<PaymentCancel />} />
          <Route path="/library" element={<ProtectedRoute><Library /></ProtectedRoute>} />
          <Route path="/admin" element={<ProtectedRoute admin><AdminDashboard /></ProtectedRoute>} />
        </Routes>
      </main>
      <Footer />
      <AriaAssistant />
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <AuthProvider>
        <CartProvider>
          <BrowserRouter>
            <AppRouter />
            <Toaster position="top-right" />
          </BrowserRouter>
        </CartProvider>
      </AuthProvider>
    </div>
  );
}

export default App;
