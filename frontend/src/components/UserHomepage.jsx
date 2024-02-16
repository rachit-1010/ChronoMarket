import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import SearchBar from "./SearchBar";
import Items from "./Items";
import { makeApiRequest } from "./apiUtils.js";
import "../styles/UserHomePage.css";
import BrandBox from "./BrandBox";
import NavigationBar from "./NavigationBar";

function UserHomePage() {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);

  const brands = [
    "Rolex",
    "Patek Philippe",
    "Audemars Piguet",
    "Omega",
    "Cartier",
    "TAG Heuer",
    "Breitling",
    "Hublot",
    "IWC Schaffhausen",
    "Jaeger-LeCoultre",
    "Panerai",
    "Vacheron Constantin",
  ];
  const handleSelectBrand = async (brand) => {
    try {
      const endpoint = `http://localhost:3500/api/item/search?query=${brand}`;
      const response = await makeApiRequest("GET", endpoint);

      if (response.success) {
        setItems(response.data);
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleSearchSubmit = async () => {
    try {
      const endpoint = `http://localhost:3500/api/item/search?query=${searchQuery}`;
      const response = await makeApiRequest("GET", endpoint);

      if (response.success) {
        setItems(response.data);
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleClick = () => {
    navigate("/user/createItemAuction");
  };

  return (
    <div className="home-page">
      <NavigationBar />
      <h1>Welcome to ChronoMarket!</h1>
      <div className="brands-container">
        {brands.map((brand, index) => (
          <BrandBox
            key={index}
            brand={brand}
            onSelectBrand={handleSelectBrand}
          />
        ))}
      </div>
      <SearchBar
        searchQuery={searchQuery}
        handleSearchChange={handleSearchChange}
        handleSearchSubmit={handleSearchSubmit}
      />
      <Items items={items} error={error} />
    </div>
  );
}

export default UserHomePage;
