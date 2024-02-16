import React, { useEffect, useState } from "react";
import { makeApiRequest } from './apiUtils';
import AdminAuctionBox from "./AdminAuctionBox";

function AdminAuctionPage() {
    const [liveAuctions, setLiveAuctions] = useState([])

    // send admin response to Notifications microservice to send email to customer
    const getAllAuctions = async () => {
        try {
            let apiUrl = 'http://localhost:3500/api/auction/live';
            const apiResponse = await makeApiRequest('GET', apiUrl)
            if (apiResponse.success) {
                setLiveAuctions(apiResponse.data.live_auctions)
                // update state for getting all live auctions
            } else {
                // no feedback, list is now blank
                setLiveAuctions([])
            }
        } catch (err) {
            console.log(err.message)
        }
    };

    // useEffect to poll for new user feedback
    useEffect(() => {
        // Fetch initial list of user feedback
        getAllAuctions();   
        
        // poll for new user feedback every 10 seconds
        const intervalId = setInterval(() => {
            getAllAuctions();
        }, 5000)

        // clean up interval when this JSX component is unmounted / not-rendered
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div style={{ textAlign: 'center' }}>
            <h1>Live Auctions</h1><br/>
            <p>Here you can see all auctions that are currently live at this moment.</p>
            {/* Fill in a section to get current customer feedback (paginated) */}
            <AdminAuctionBox liveAuctions={liveAuctions} />
        </div>
    )
}

export default AdminAuctionPage;