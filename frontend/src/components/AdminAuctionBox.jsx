import React, {useState} from "react";
import { makeApiRequest } from './apiUtils';
import "../styles/AdminAuctionBox.css";

function UserFeedbackBox({ liveAuctions }) {
    const [auction, setAuction] = useState({});

    // function to toggle the admin window to respond to feedback
    const toggleResponseWindow = async (id, username, email, feedbackBody) => {      
        // Update state by creating a new object
        setFeedbackItem(prevState => {
            return { ...prevState, id: id, username: username, email: email, feedbackBody: feedbackBody };
        });
    };

    return (
        <div className="live-auctions-section">
            <div className="live-auction-container">
                {liveAuctions.map((auction, index) => (
                <div key={index} className="auction-section">
                    <p>Item Name: {auction.item_name}</p>
                    <p>Seller Email: {auction.seller_email}</p>
                    <p>Start Time: <br/> 
                    {auction.start_time}
                    </p><br/>
                    <p>End Time:<br/> 
                    {auction.end_time}</p>
                    <br/>
                    <button className="respondButton">
                        Close Auction
                    </button>
                </div>
                ))}
            </div>
        </div>
      );
}

export default UserFeedbackBox;