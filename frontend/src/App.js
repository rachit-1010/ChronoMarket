import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import React from "react";
// login and register imports
import LoginPage from "./components/Login";
import RegisterPage from "./components/Register";
// user page imports
import UserHomePage from "./components/UserHomepage";
import CreateItemAuction from "./components/CreateItemAuction";
import CheckoutPage from "./components/CheckoutPage";
import CustomerSupport from "./components/CustomerSupport";
import UserProfilePage from "./components/UserProfile";
// admin page imports
import AdminHomePage from "./components/AdminHomepage";
import AdminAuctionPage from "./components/AdminAuctions";
import AdminSupportPage from "./components/AdminSupport";

// bidding
import Bidding from "./components/Bidding";

const AppRouter = () => {
  // state for if user is logged in or not
  const [userLoggedIn, setLoggedIn] = React.useState(
    () => sessionStorage.getItem("userId") != null
  );
  const [isAdmin, setAdminState] = React.useState(false);

  // handler for logged in or registered users
  function SetLogin() {
    setLoggedIn(true);
  }

  // handler for admin state
  function SetAdmin() {
    setAdminState(true);
  }

  return (
    <Router>
      <Routes>
        {/* Public routes accessible to all users */}
        <Route
          path="/"
          element={
            <LoginPage
              onLoginClick={SetLogin}
              onAdminLogin={SetAdmin}
            />
          }
        />
        <Route
          path="/login"
          element={
            <LoginPage
              onLoginClick={SetLogin}
              onAdminLogin={SetAdmin}
            />
          }
        />
        {
          // routes for non-logged in users
          !userLoggedIn ? (
            <>
              <Route
                path="/login"
                element={
                  <LoginPage
                    // onSuspendedUser={SetSuspended}
                    onLoginClick={SetLogin}
                    onAdminLogin={SetAdmin}
                  />
                }
              />
              <Route
                path="/register"
                element={
                  <RegisterPage
                    onLoginClick={SetLogin}
                    onAdminLogin={SetAdmin}
                  />
                }
              />
              {/* Redirect any other route to the login page */}
              <Route path="*" element={<Navigate to="/login" />} />
            </>
          ) : /////////////////// ADD SUSPENDED STATE /////////////////////

          // if user is logged in, check if they are admin or non-admin
          !isAdmin ? (
            <>
              {/* Additional routes or components for non-admin users */}
              <Route path="/user/home" element={<UserHomePage />} />
              <Route
                path="/user/createItemAuction"
                element={<CreateItemAuction />}
              />

              {/* Link item ID into URL */}
              <Route path="/user/bid/:item_id" element={<Bidding />} />
              <Route path="/user/checkout" element={<CheckoutPage />} />

              {/* Customer support page to leave feedback*/}
              <Route path="/user/support" element={<CustomerSupport />} />

              {/* User profile page to manage account */}
              <Route path="/user/profile" element={<UserProfilePage />} />
            </>
          ) : (
            <>
              {/* Additional routes or components for admin users */}
              <Route path="/admin/home" element={<AdminHomePage />} />
              <Route path="/admin/support" element={<AdminSupportPage />} />
              <Route path="/admin/auctions" element={<AdminAuctionPage />} />
            </>
          )
        }
      </Routes>
    </Router>
  );
};

export default AppRouter;
