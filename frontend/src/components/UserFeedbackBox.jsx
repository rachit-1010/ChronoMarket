import React, {useState} from "react";
import { makeApiRequest } from './apiUtils';
import "../styles/UserFeedbackBox.css";

function UserFeedbackBox({ usersFeedback }) {
    const [respond, toggleRespond] = useState(false);
    const [feedbackItem, setFeedbackItem] = useState({});
    
    // send admin response email to customer, and update user feedback response to track it was replied to
    const sendFeedbackNotification = async (feedbackId, username, email) => {
        // get subject line and body for response
        const subjectLineInput = document.querySelector('.email-subject');
        const subjectVal = subjectLineInput.value;
        const bodyInput = document.querySelector('.email-response');
        const bodyVal = bodyInput.value;

        // send admin email to recipient using RabbitMQ broker
        let notificationsApiUrl = 'http://localhost:3500/api/message_broker';
        let bodyParams = { 
            "data": {
                email: email,
                username: username, 
                subject: subjectVal,
                body: bodyVal
            },
            "topic": "request.notifications.respond_feedback"
        };
        const notificationsResponse = await makeApiRequest('POST', notificationsApiUrl, bodyParams)
        if (notificationsResponse.success) {
            console.log(notificationsResponse.data)
            subjectLineInput.value = '';
            bodyInput.value = '';
            alert ("Email sent to user.")
        } else {
            console.log(notificationsResponse.error)
        }

        // update flag to mark that this piece of user feedback was responded to
        let feedbackUpdateURL = 'http://localhost:3500/api/notifications/update_feedback';
        let feedbackParams = { 
            feedback_id: feedbackId
        };
        const feedbackResponse = await makeApiRequest('PUT', feedbackUpdateURL, feedbackParams)
        if (feedbackResponse.success) {
            console.log(feedbackResponse.data)
        } else {
            console.log(feedbackResponse.error)
        }
    };

    // function to toggle the admin window to respond to feedback
    const toggleResponseWindow = async (id, username, email, feedbackBody) => {      
        // Update state by creating a new object
        setFeedbackItem(prevState => {
            return { ...prevState, id: id, username: username, email: email, feedbackBody: feedbackBody };
        });

        // Toggle the respond state to true
        toggleRespond(true);
    };


    return (
        <div className="customer-support-center">
            <div className="user-feedback-container">
                {usersFeedback.map((feedback, index) => (
                <div key={index} className="user-feedback">
                    <p>Username: {feedback.username}</p>
                    <p>Email: {feedback.email}</p>
                    <p>Feedback: {feedback.feedback_body}</p>
                    <br/>
                    <button
                        className="respondButton"
                        onClick={() => toggleResponseWindow(feedback.id, feedback.username, feedback.email, feedback.feedback_body)}
                    >
                        Respond to Feedback
                    </button>
                </div>
                ))}
            </div>
            {respond && (
                <div className="feedbackContainer">
                    <p>Username: {feedbackItem.username}</p>
                    <p>Email: {feedbackItem.email}</p>
                    <p>Feedback: {feedbackItem.feedbackBody}</p>
                    <br/>
                    <br/>
                    <div className="subjectContainer">
                        <label>Subject Line:</label><br/>
                        <input id="email-subject" className="email-subject" />
                    </div>
                    <br/>
                    <div className="openTextContainer">
                        <textarea className="email-response" placeholder="Enter the body of your email response here..."></textarea>
                    </div>
                    <button className="respondButton" onClick={() => sendFeedbackNotification(feedbackItem.id, feedbackItem.username, feedbackItem.email)}>
                        Send Email
                    </button>
                </div>
            )}
        </div>
      );
}

export default UserFeedbackBox;