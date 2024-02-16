import React, { useEffect, useState } from "react";
import { makeApiRequest } from './apiUtils';
import UserFeedbackBox from "./UserFeedbackBox";
import "../styles/AdminSupport.css"

function AdminSupportPage() {
    const [feedbackList, setFeedbackList] = useState([])

    // send admin response to Notifications microservice to send email to customer
    const getAllFeedback = async () => {
        try {
            let apiUrl = 'http://localhost:3500/api/notifications/list_all_feedback';
            const apiResponse = await makeApiRequest('GET', apiUrl)
            if (apiResponse.success) {
                setFeedbackList(apiResponse.data)
                // update state for getting all feedback
            } else {
                // no feedback, list is now blank
                setFeedbackList([])
            }
        } catch (err) {
            console.log(err.message)
        }
    };

    // useEffect to poll for new user feedback
    useEffect(() => {
        // Fetch initial list of user feedback
        getAllFeedback();   
        
        // poll for new user feedback every 10 seconds
        const intervalId = setInterval(() => {
            getAllFeedback();
        }, 10000)

        // clean up interval when this JSX component is unmounted / not-rendered
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div style={{ textAlign: 'center' }}>
            <h1>Customer Support Center</h1>
            {/* Fill in a section to get current customer feedback (paginated) */}
            <UserFeedbackBox usersFeedback={feedbackList} />
        </div>
    )
}

export default AdminSupportPage;