import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "../styles/Bidding.css";
import NavigationBar from "./NavigationBar";
import { formatDate } from "../util.js";
import { makeApiRequest } from "./apiUtils";
import { useNavigate } from 'react-router-dom';


//TODO - Notification to Cole when auction end (send purchase price)

function Bidding() {
  const navigate = useNavigate();

  const [item, setItem] = useState({});
  const { item_id } = useParams();
  const [bidAmount, setBidAmount] = useState(0);
  const [bidIncrement, setBidIncrement] = useState(50);

  const [highBid, setHighBid] = useState(0);
  const [highBidUser, setHighBidUser] = useState("");
  const [highBidUsername, setHighBidUsername] = useState("");
  const [highBidEmail, setHighBidEmail] = useState('');

  const [auctionName, setAuctionName] = useState("");
  const [seller, setSeller] = useState("");
  const [sellerName, setSellerName] = useState("");
  const [sellerEmail, setSellerEmail] = useState("");
  const [buyNowPrice, setBuyNow] = useState(0);

  const [isButtonDisabled, setIsButtonDisabled] = useState(false);
  const [purchased, setPurchased] = useState(false);
  const [expired, setExpired] = useState(false);

  const user = sessionStorage.getItem("userId");
  const username = sessionStorage.getItem("username");
  const user_email = sessionStorage.getItem("email");

  const [timeLeft, setTimeLeft] = useState("");

  //Gets the highest bidder and amount for the item
  useEffect(() => {
    // Fetch highest bidder details
    fetchHighestBidder();

    // Fetch item details
    fetchItemDetails();

    //Check if purchased
    checkPurchase();
  }, [item_id]);

  //Gets the time left for the auction
  useEffect(() => {
    // Setup timer
    const interval = setInterval(() => {
      if (item && item.auction_deadline) {
        const deadline = new Date(item.auction_deadline);
        const now = new Date();
        const timeLeftMilliseconds = deadline - now;

        if (timeLeftMilliseconds <= 0) {
          clearInterval(interval);
          setTimeLeft("Auction has ended");
          setIsButtonDisabled(true);
        } else {
          const timeLeftString =
            convertMillisecondsToTime(timeLeftMilliseconds);
          setTimeLeft(timeLeftString);
        }
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  /*
  useEffect(() => {
    const fetchDataInterval = setInterval(() => {
      fetchHighestBidder();
      fetchItemDetails();
    }, 1000); // 1000 milliseconds = 1 second

    return () => clearInterval(fetchDataInterval);
  }, []);
*/

  function checkPurchase() {
    // Fetch information if the item has been purchased
    fetch(`http://localhost:3500/api/item/get_purchase?item_id=${item_id}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);

        if (data.item_id) {
          setPurchased(true);
          setIsButtonDisabled(true);
          console.log("Item has been purchased");
        } else {
          console.log("Item has not been purchased");
        }
      })
      .catch((error) =>
        console.error("Error fetching purchase details:", error)
      );
  }

  function fetchItemDetails() {
    fetch(`http://localhost:3500/api/item/get_item?id=${item_id}`)
      .then((response) => response.json())
      .then((data) => {
        setItem(data);
        setBidIncrement(data.bid_amount);
        setBuyNow(data.starting_price * 4);
        setSeller(data.user_id);
        setAuctionName(data.item_name);

        console.log("Item details:", data);
        console.log("Seller: ", data.user_id);

        if (String(user) === String(data.user_id)) {
          setIsButtonDisabled(true);
        }

        //Handle if the auction has ended
        const deadline = new Date(data.auction_deadline);
        const now = new Date();
        const timeLeftMilliseconds = deadline - now;
        if (timeLeftMilliseconds > 0) {
          const timeLeftString =
            convertMillisecondsToTime(timeLeftMilliseconds);
          setTimeLeft(timeLeftString);
        } else {
          setTimeLeft("Auction has ended");
          setIsButtonDisabled(true);
        }

        //Handle when the auction is scheduled in the future
        const start = new Date(data.auction_start);
        const timeStartMilliseconds = start - now;
        if (timeStartMilliseconds > 0) {
          setTimeLeft("Auction has not started yet");
          setIsButtonDisabled(true);
        }

        //Get the seller email
        fetch(`http://localhost:3500/api/accounts/user/email/${data.user_id}`)
          .then((response) => response.json())
          .then((data) => {
            console.log(data);
            setSellerName(data.seller_username);
            setSellerEmail(data.seller_email);
          })
          .catch((error) =>
            console.error("Error fetching purchase details:", error)
          );
      })
      .catch((error) => console.error("Error fetching item details:", error));
  }

  async function fetchHighestBidder() {
    let high_bid = 0;

    const response = await fetch(
      `http://localhost:3500/api/bidding/highestbid/${item_id}`,
      {}
    );
    const data = await response.json();

    setHighBid(data.bid_amount);
    setHighBidUser(data.user_id);
    setHighBidUsername(data.username);
    setHighBidEmail(data.user_email);

    console.log("Highest bidder details:", data);

    if (String(user) === String(data.user_id)) {
      setIsButtonDisabled(true);
    }

    return data.bid_amount;
  }

  //Convert milliseconds to time
  function convertMillisecondsToTime(milliseconds) {
    const minutes = Math.floor((milliseconds / (1000 * 60)) % 60);
    const hours = Math.floor((milliseconds / (1000 * 60 * 60)) % 24);
    const days = Math.floor(milliseconds / (1000 * 60 * 60 * 24));

    return `${days}d ${hours}h ${minutes}m`;
  }

  function handleBid() {
    checkPurchase();
    const bid_amount = fetchHighestBidder();

    //const minBidIncrement = 10; // Set minimum bid increment
    const bidAmountNumber = parseFloat(bidAmount); // Convert bid amount to a number

    // Check if highBid is a number
    const currentHighBid = parseFloat(bid_amount);

    // Will return False if its a string and True if its a number
    const isHighBidNumber = !isNaN(currentHighBid);

    if (!isHighBidNumber && bidAmountNumber < item.starting_price) {
      alert(
        `Your bid must be at least the starting price of \$${item.starting_price}.`
      );
      return;
    }

    // Check if bid is at least higher than current high bid
    if (isHighBidNumber && bidAmountNumber <= currentHighBid) {
      alert(
        `Your bid must be at least \$${bidIncrement} higher than the current bid.`
      );
      return;
    } else if (
      isHighBidNumber &&
      bidAmountNumber - currentHighBid < bidIncrement
    ) {
      alert(
        `Your bid must be at least \$${bidIncrement} higher than the current bid.`
      );
      return;
    } else if (isHighBidNumber && bidAmountNumber > buyNowPrice) {
      alert(`Your bid is currently higher than the Buy Now price.`);
      return;
    }

    // Make POST request to bidding endpoint to track high bid
    fetch("http://localhost:3500/api/bidding/bid", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: user,
        username: username,
        amount: bidAmount,
        item_id: item_id,
        user_email: user_email,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        setHighBid(bidAmount);
        setHighBidUser(user);
        setHighBidUsername(username);

        fetchHighestBidder();

        console.log("Bid submitted successfully", data);

        //Calls notifications only if there is a previous high bidder email
        //SENDS NOTIF to previous high bidder letting them know of their outbid
        if (highBidEmail === '') {
            console.log("No previous high bidder...no email sent");
        } else {
          console.log("...Sending notification to previous high bidder");

          // Make POST request to notifications endpoint
          fetch("http://localhost:3500/api/notifications/high_bid", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: highBidEmail,
              auction: auctionName,
            }),
          })
            .then((notificationResponse) => notificationResponse.json())
            .then((notificationData) => {
              console.log("Notification sent successfully", notificationData);
            })
            .catch((notificationError) => {
              console.error("Error sending notification:", notificationError);
            });
        }

        //SENDS NOTIF to seller whenever a bid goes through
        console.log("...Sending notification to seller");
        fetch("http://localhost:3500/api/notifications/seller_new_bid", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: sellerEmail,
            auction: auctionName,
          }),
        })
          .then((notificationResponse) => notificationResponse.json())
          .then((notificationData) => {
            console.log("Notification sent successfully", notificationData);
          })
          .catch((notificationError) => {
            console.error("Error sending notification:", notificationError);
          });

        setHighBidEmail(user_email);
      })
      .catch((error) => console.error("Error submitting bid:", error));
  }

  function handleBuyNow() {
    const purchase_date = new Date();
    purchase_date.setHours(0, 0, 0, 0);
    fetch("http://localhost:3500/api/bidding/bid", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: user,
        username: username,
        amount: buyNowPrice,
        item_id: item_id,
        user_email: user_email,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        setIsButtonDisabled(true);
        setTimeLeft("Auction has ended");
        setPurchased(true);

        fetchItemDetails();

        console.log("Buy Now submitted successfully", data);
      });
    

    //Make POST to Auction endpoint, signaling a buy and end of auction
    fetch("http://localhost:3500/api/auction/buy_now", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: item_id,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Buy Now status sent to Auction for item: ", item_id);
      })
      .catch((error) => console.error("Error submitting buy:", error));
  }

  // function to add this watch reference number to the logged-in users watchlist
  async function addToWatchList() {
    let bodyParams = {
      reference_num: item.watch_reference_number,
      email: sessionStorage.getItem("email"),
    };
    let apiUrl = "http://localhost:3500/api/accounts/watchlist/add";
    const apiResponse = await makeApiRequest("POST", apiUrl, bodyParams);
    if (apiResponse.success) {
      alert("You've added this watch reference number to your watchlist.");
    } else {
      console.log(apiResponse.error);
    }
  }

  // function to allow a user to give feedback on flagging an item
  async function flagItem() {
    navigate('/user/support')
  }

  return (
    <div className="page-container">
      <NavigationBar />
      <div className="watch-details">
        <div className="image-container">
          <img
            src={
              item.item_image
                ? `data:image/jpg;base64,${item.item_image}`
                : "https://dehayf5mhw1h7.cloudfront.net/wp-content/uploads/sites/1075/2019/03/16192350/No-Photo-Provided.png"
            }
            alt={item.name}
            className="watch-image"
          />
          <button
            onClick={addToWatchList}
            className="watchlist-button"
            disabled={isButtonDisabled}
          >
            Add to Watchlist
          </button>
          <button onClick={flagItem} className="watchlist-button">
            Flag Item
          </button>
        </div>
        <div class="watch-info">
          <h2>{item.item_name}</h2>
          {purchased && (
            <p className="purchase-status">This item has been purchased</p>
          )}
          {expired && (
            <p className="purchase-status">
              The timer for this auction has expired
            </p>
          )}
          <div className="info-row">
            <span>Brand:</span> {item.brand}
          </div>
          <div className="info-row">
            <span>Model:</span> {item.watch_model}
          </div>
          <div className="info-row">
            <span>Year:</span> {item.watch_year}
          </div>
          <div className="info-row">
            <span>Description:</span> {item.description}
          </div>
          <div className="info-row">
            <span>Reference Number:</span> {item.watch_reference_number}
          </div>
          <div className="info-row">
            <span>Condition:</span> {item.item_condition}
          </div>
          <div className="info-row">
            <span>Quantity:</span> 1
          </div>
          <div className="info-row">
            <span>Starting Price:</span> ${item.starting_price}
          </div>
          <div className="info-row">
            <span>Seller:</span> {sellerName}
          </div>
          <div className="info-row"></div>
          <div className="auction-details">
            <div className="info-row">
              <span>Auction Start:</span> {item.auction_start}
            </div>
            <div className="info-row">
              <span>Time Left:</span> {timeLeft}
            </div>
          </div>
        </div>
      </div>

      <div className="bidding-section">
        <h3>Bidding Details</h3>
        <p>
          <strong>Current bid: </strong>
          {highBid}
        </p>
        <p>
          <i>
            Any bids made to this item must be at least {bidIncrement}$ over the
            current bid
          </i>
        </p>
        <p>
          <strong>Bidder Name: </strong>
          {highBidUsername}
        </p>
        <input
          type="number"
          value={bidAmount}
          onChange={(e) => setBidAmount(e.target.value)}
          className="bid-input"
        />
        <button
          onClick={handleBid}
          className="bid-button"
          disabled={isButtonDisabled}
        >
          Place bid
        </button>
      </div>

      <div className="buy-now-section">
        <h3>Buy Now</h3>
        <p>
          <i>
            Clicking on Buy Now will place this item in your cart and end the
            auction
          </i>
        </p>
        <p>
          <strong>Buy Now Price: </strong>${buyNowPrice}
        </p>
        <button
          onClick={handleBuyNow}
          className="buy-now-button"
          disabled={isButtonDisabled}
        >
          Buy Now
        </button>
      </div>
    </div>
  );
}

export default Bidding;
