import React from "react";
import "../styles/CheckoutItem.css";

function CheckoutItem({ item }) {
  return (
    <div className="checkout-item">
      <img src={item.item_image} alt={item.item_name} className="item-image" />
      <h3>{item.item_name}</h3>
      <p>Price: ${item.purchase_amount}</p>
    </div>
  );
}

export default CheckoutItem;
