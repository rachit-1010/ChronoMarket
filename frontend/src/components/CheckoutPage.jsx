import React, { useState, useEffect } from "react";
import CheckoutItemList from "./CheckoutItemList";
import { makeApiRequest } from "./apiUtils.js";
import "../styles/CheckoutPage.css";
import NavigationBar from "./NavigationBar";
function CheckoutPage() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchItems();
  }, []);

  const handleCheckout = async () => {
    if (items.length) {
      try {
        const itemIds = items.map((item) => item.id);

        const response = await makeApiRequest(
          "POST",
          "http://localhost:3500/api/item/update_purchase",
          { itemIds }
        );

        if (response.success) {
          console.log("Checkout successful");
          setItems([]);
        } else {
          setError(response.error);
        }
      } catch (err) {
        setError(err.message);
      }
    }
  };

  const fetchItems = async () => {
    try {
      const userId = sessionStorage.getItem("userId");
      const response = await makeApiRequest(
        "GET",
        `http://localhost:3500/api/item/${userId}/purchases`
      );
      if (response.success) {
        setItems(response.data);
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="checkout-page">
      <NavigationBar />
      <h1>Your Checkout</h1>
      <CheckoutItemList items={items} />
      <button onClick={handleCheckout}>Checkout</button>
    </div>
  );
}

export default CheckoutPage;
