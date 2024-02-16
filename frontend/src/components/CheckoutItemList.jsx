import React from "react";
import CheckoutItem from "./CheckoutItem";
import "../styles/CheckoutItemList.css";

function CheckoutItemList({ items }) {
  return (
    <div className="checkout-items-list">
      {items.map((item) => (
        <CheckoutItem key={item.id} item={item} />
      ))}
    </div>
  );
}

export default CheckoutItemList;
