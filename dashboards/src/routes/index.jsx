import { createBrowserRouter, Navigate } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout";
import DashboardLayout from "../layouts/DashboardLayout";
import GuestRoute from "../components/common/GuestRoute";
import ProtectedRoute from "../components/common/ProtectedRoute";
import LoginPage from "../pages/auth/LoginPage";
import OverviewPage from "../pages/dashboard/OverviewPage";
import OrdersPage from "../pages/dashboard/OrdersPage";
import InventoryPage from "../pages/dashboard/InventoryPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="/login" replace />,
  },
  {
    element: (
      <GuestRoute>
        <AuthLayout />
      </GuestRoute>
    ),
    children: [
      {
        path: "/login",
        element: <LoginPage />,
      },
    ],
  },
  {
    element: (
      <ProtectedRoute>
        <DashboardLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        path: "/dashboard",
        element: <Navigate to="/dashboard/overview" replace />,
      },
      {
        path: "/dashboard/overview",
        element: <OverviewPage />,
      },
      {
        path: "/dashboard/orders",
        element: <OrdersPage />,
      },
      {
        path: "/dashboard/inventory",
        element: <InventoryPage />,
      },
    ],
  },
]);

export default router;