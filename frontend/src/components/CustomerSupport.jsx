import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { makeApiRequest } from './apiUtils';
import '../styles/CustomerSupport.css';

// function for a user to leave feedback with customer support
function CustomerSupport() {

    // function to post the user feedback to the Notifications Feedback database
    async function submitFeedback(){
        // get email address and user feedback
        const emailInput = document.querySelector('#return-email');
        const bestReturnEmail = emailInput.value;
        const userInput = document.querySelector('.user-feedback');
        const userFeedback = userInput.value;

        // get users username
        const username = sessionStorage.getItem('username');

        // define body params, endpoint, and make request
        let bodyParams = { 
            email: bestReturnEmail,
            username: username,
            feedback_body: userFeedback,
        };
        let apiUrl = 'http://localhost:3500/api/notifications/add_feedback'
        const apiResponse = await makeApiRequest('POST', apiUrl, bodyParams)
        if (apiResponse.success) {
            console.log("User submitted feedback")
            // clear out input values
            emailInput.value = '';
            userInput.value = '';
            alert ("Your feedback was submitted, thanks!")
        } else {
            console.log(apiResponse.error)
        }
    }

    return (
        <div className="customerSupport">
            <h1>Contact Us</h1>
            <span>
                Please use the below submission form to send our team any feedback you have for our site, or issues
                you're experiencing. 
                <br/>
                <br/>
                Our team will reach out within 48 hours to address your feedback.
                <br/>
                <br/>
                We appreciate your support, and want to make your ChronoMarket experience as 
                amazing as possible!
            </span>
            <div className="feedbackContainer">
                <div className="emailContainer">
                    <label>Best email to reach you at:</label>
                    <input id="return-email" className="return-email" />
                </div>
                <div className="openTextContainer">
                    <textarea className="user-feedback" name="user-feedback" placeholder="Leave your feedback here..."></textarea>
                </div>
                <button onClick={submitFeedback}>Submit Feedback</button>
            </div>
        </div>
    )
}

export default CustomerSupport;