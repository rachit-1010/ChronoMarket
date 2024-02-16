import React from "react";
import { NavLink, useNavigate} from "react-router-dom";
import "../styles/NavigationBar.css";
import ShoppingCartIcon from "../images/shopping-cart-outline-svgrepo-com.svg";

function NavigationBar() {
  const navigate = useNavigate();

  // function to log the user out
  const Logout = () => {
    // Clear all items in session storage
    sessionStorage.clear();
    // Replace the current state in the session history
    window.history.replaceState(null, "", "/login");
    navigate('/login')
  }

  return (
    <nav className="navigation-bar">
      <NavLink to="/user/home" className="nav-link">
        Home
      </NavLink>
      <NavLink to="/user/createItemAuction" className="nav-link">
        Create Auction
      </NavLink>
      <NavLink to="/user/support" className="nav-link">
        Contact
      </NavLink>
      <NavLink to="/user/checkout" className="nav-link">
        <img src={ShoppingCartIcon} alt="Shopping Cart" />
      </NavLink>
      <NavLink to="/user/profile" className="nav-link">
        Profile
      </NavLink>

      {/* Custom button that calls the Logout function */}
      <button id="logout-button" className="nav-link" onClick={Logout}>
        Logout
      </button>
      <span className="username-text">
        Hi, {sessionStorage.getItem('username')}
      </span>
    </nav>
  );
}

export default NavigationBar;
