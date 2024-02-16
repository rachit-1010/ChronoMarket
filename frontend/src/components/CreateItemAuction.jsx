import React, { useState, useEffect } from "react";
import "../styles/createItemAuction.css";
import { useNavigate } from "react-router-dom";
import NavigationBar from "./NavigationBar";
import { makeApiRequest } from "./apiUtils";

function CreateItemAuction() {
  // navigator to update page state and trigger router
  const navigate = useNavigate();

  const [data, setData] = useState({
    user_id: sessionStorage.getItem("userId"),
    user_email: sessionStorage.getItem("email"),
    id: "",
    item_name: "",
    bid_amount: "",
    starting_price: "",
    description: "",
    brand: "Rolex",
    watch_year: "",
    watch_model: "",
    watch_reference_number: "",
    item_condition: "",
    auction_won: 0,
    item_image: "",
    auction_start: "Now",
    duration: "6hrs",
    auction_deadline: "",
  });

  let newData = { ...data };

  useEffect(async () => {
    if (newData.id) {
      console.log(newData);
      auctionResponse();
      sendWatchlistNotification();
    }
  }, [newData.id]);

  const [isOther, setIsOther] = useState(false);

  const handleChange = (e) => {
    let value = e.target.value;

    // parseInt for integer values
    if (
      e.target.name === "bid_amount" ||
      e.target.name === "starting_price" ||
      e.target.name === "watch_year"
    ) {
      value = parseInt(value, 10);
    }

    setData({
      ...data,
      [e.target.name]: value,
    });
    console.log(e.target.name);
    console.log(value);

    if (e.target.name === "brand" && e.target.value === "other") {
      setIsOther(true);
    }
  };
  const handleImageChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      if (e.target.files[0].type === "image/jpeg") {
        setData({ ...data, item_image: e.target.files[0] });
      } else {
        alert("Only JPG files are allowed.");
      }
    }
  };
  const handleInputChange = (e) => {
    setData({
      ...data,
      [e.target.name]: e.target.value,
    });
  };

  // function to notify any users that are watching this watch reference number
  async function sendWatchlistNotification() {
    let apiUrl = `http://localhost:3500/api/accounts/watchlist/${data.watch_reference_number}`;
    const apiResponse = await makeApiRequest("GET", apiUrl);
    if (apiResponse.success) {
      // ADD CODE TO PARSE EMAILS FROM RESPONSE AND SEND TO THOMAS NOTIFICATIONS
      const watchlistEmails = [];
      for (const user in apiResponse.data) {
        const email = apiResponse.data[user].email;
        watchlistEmails.push(email);
      }

      // define body params and make request to RabbitMQ broker for Notificiations
      // to send emails to users that an item matching their watchlist was added
      let bodyParams = {
        data: {
          item: data.watch_reference_number,
          email: watchlistEmails,
        },
        topic: "request.notifications.watchlist",
      };
      console.log("This is the user watchlist data: ", bodyParams);
      let rabbitMqUrl = "http://localhost:3500/api/message_broker";
      const rabbitMqResponse = await makeApiRequest(
        "POST",
        rabbitMqUrl,
        bodyParams
      );
      if (rabbitMqResponse.success) {
        console.log("Sent watchlist email(s) successfully.");
      } else {
        console.log("issue sending watchlist emails: ", rabbitMqResponse.error);
      }
    } else {
      // no one is watching this item
      console.log(apiResponse.error);
    }
  }

  const auctionResponse = async () => {
    try {
      const response = await fetch("http://localhost:3500/api/auction", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const auctionData = await response.json();
      console.log("Success:", auctionData);

      // Assuming `navigate` is defined and imported from a routing library (e.g., react-router-dom)
      navigate("/user/home");
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (newData.auction_start === "Now") {
      let date = new Date();
      newData.auction_start =
        date.getFullYear() +
        "-" +
        ("0" + (date.getMonth() + 1)).slice(-2) +
        "-" +
        ("0" + date.getDate()).slice(-2) +
        " " +
        ("0" + date.getHours()).slice(-2) +
        ":" +
        ("0" + date.getMinutes()).slice(-2) +
        ":" +
        ("0" + date.getSeconds()).slice(-2);
    }
    if (newData.duration === "6hrs") {
      let deadline = new Date(
        new Date(newData.auction_start).getTime() + 6 * 60 * 60 * 1000
      );
      newData.auction_deadline =
        deadline.getFullYear() +
        "-" +
        ("0" + (deadline.getMonth() + 1)).slice(-2) +
        "-" +
        ("0" + deadline.getDate()).slice(-2) +
        " " +
        ("0" + deadline.getHours()).slice(-2) +
        ":" +
        ("0" + deadline.getMinutes()).slice(-2) +
        ":" +
        ("0" + deadline.getSeconds()).slice(-2);
    } else if (newData.duration === "12hrs") {
      let deadline = new Date(
        new Date(newData.auction_start).getTime() + 12 * 60 * 60 * 1000
      );
      newData.auction_deadline =
        deadline.getFullYear() +
        "-" +
        ("0" + (deadline.getMonth() + 1)).slice(-2) +
        "-" +
        ("0" + deadline.getDate()).slice(-2) +
        " " +
        ("0" + deadline.getHours()).slice(-2) +
        ":" +
        ("0" + deadline.getMinutes()).slice(-2) +
        ":" +
        ("0" + deadline.getSeconds()).slice(-2);
    } else if (newData.duration === "1min") {
      console.log("ONE MIN");
      let deadline = new Date(
        new Date(newData.auction_start).getTime() + 0.0166 * 60 * 60 * 1000
      );
      newData.auction_deadline =
        deadline.getFullYear() +
        "-" +
        ("0" + (deadline.getMonth() + 1)).slice(-2) +
        "-" +
        ("0" + deadline.getDate()).slice(-2) +
        " " +
        ("0" + deadline.getHours()).slice(-2) +
        ":" +
        ("0" + deadline.getMinutes()).slice(-2) +
        ":" +
        ("0" + deadline.getSeconds()).slice(-2);
    }
    setData(newData); // 使用 setData 更新狀態
    console.log(newData);

    try {
      // send data to item microservice
      const formData = new FormData();
      for (const key in newData) {
        formData.append(key, newData[key]);
      }
      const itemResponse = await fetch(
        "http://localhost:3500/api/item/add_item",
        {
          method: "POST",
          body: formData,
        }
      );
      console.log("itemResponse:", itemResponse);
      const itemData = await itemResponse.json();
      console.log("Success:", itemData);

      // update data with the returned item data
      setData((prevData) => ({
        ...prevData,
        id: itemData.item_id,
      }));

      console.log("data:", newData);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <>
      <NavigationBar />
      <form onSubmit={handleSubmit} className="form">
        <h1>Create Item</h1>
        <label className="label">
          Item Name
          <input
            className="input"
            name="item_name"
            value={data.item_name}
            onChange={handleChange}
            placeholder="Vintage Watch"
          />
        </label>
        <label className="label">
          Bid Amount
          <input
            className="input"
            name="bid_amount"
            value={data.bid_amount}
            onChange={handleChange}
            placeholder="200"
          />
        </label>
        <label className="label">
          Starting Price
          <input
            className="input"
            name="starting_price"
            value={data.starting_price}
            onChange={handleChange}
            placeholder="5000"
          />
        </label>
        <label className="label">
          Description
          <input
            className="input"
            name="description"
            value={data.description}
            onChange={handleChange}
            placeholder="A rare vintage watch from 1950"
          />
        </label>
        <label className="label">
          Brand
          {!isOther ? (
            <select
              className="input"
              name="brand"
              value={data.brand}
              onChange={handleChange}
            >
              {[
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
                "other",
              ].map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          ) : (
            <input
              className="input"
              name="brand"
              value={data.brand}
              onChange={handleInputChange}
              placeholder="Rolex"
            />
          )}
        </label>
        <label className="label">
          Watch Year
          <input
            className="input"
            name="watch_year"
            value={data.watch_year}
            onChange={handleChange}
            placeholder="1950"
          />
        </label>
        <label className="label">
          Watch Model
          <input
            className="input"
            name="watch_model"
            value={data.watch_model}
            onChange={handleChange}
            placeholder="Vintage Classic"
          />
        </label>
        <label className="label">
          Reference Number
          <input
            className="input"
            name="watch_reference_number"
            value={data.watch_reference_number}
            onChange={handleChange}
            placeholder="VN1950"
          />
        </label>
        <label className="label">
          Condition
          <input
            className="input"
            name="item_condition"
            value={data.item_condition}
            onChange={handleChange}
            placeholder="Good"
          />
        </label>
        <label className="label">
          Item Image
          <input
            className="input"
            type="file"
            name="image"
            accept=".jpg, .jpeg"
            onChange={handleImageChange}
            required
          />
        </label>
        <h1>Create Auction</h1>
        <label>Auction Start</label>
        <select name="auction_start" onChange={handleChange}>
          <option value="Now">Now</option>
          <option value="Other">Other</option>
        </select>
        {data.auction_start === "Other" && (
          <>
            <label>Enter Time:</label>
            <input
              type="datetime-local"
              name="auction_start"
              onChange={(e) => {
                handleChange(e);
                e.target.blur();
              }}
            />
          </>
        )}
        <label>Duration</label>
        <select name="duration" onChange={handleChange}>
          <option value="1min">1min</option>
          <option value="6hrs">6hrs</option>
          <option value="12hrs">12hrs</option>
          <option value="24hrs">24hrs</option>
          <option value="48hrs">48hrs</option>
        </select>
        <button type="submit">Submit</button>
      </form>
    </>
  );
}

export default CreateItemAuction;
