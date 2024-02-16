import React from 'react';
import { useNavigate } from 'react-router-dom';
import { makeApiRequest } from './apiUtils';
import '../styles/UserProfile.css';

// page for users to upate their information 
function UserProfilePage () {
    // navigator to update page state and trigger router
    const navigate = useNavigate();

    // if user wants to update their email address or account password
    async function updateInfo(type){
        let newInput;
        let newInputValue;
        if (type == "username") {
             // get new email address
            newInput = document.querySelector('.update-username');
            newInputValue = newInput.value;
        } else {
            // get new password
            newInput = document.querySelector('.password');
            newInputValue = newInput.value;
        }
 
        // define body params, endpoint, and make request
        let bodyParams = { 
            update_type: type,
            update_value: newInputValue,
        };
        let apiUrl = 'http://localhost:3500/api/accounts/update'
        const apiResponse = await makeApiRequest('POST', apiUrl, bodyParams)
        if (apiResponse.success) {
            if (type == "username") {
                sessionStorage.setItem("username", newInputValue)
            }
            // clear out input values
            newInput.value = '';
            alert ("Your update was successful.")
        } else {
            console.log(apiResponse.error)
        }
    }

    // if user wants to suspend their own account
    async function suspendAccount(){
        let apiUrl = 'http://localhost:3500/api/accounts/user/suspend'
        const apiResponse = await makeApiRequest('POST', apiUrl)
        if (apiResponse.success) {
            alert ("You've successfully suspended your account.")
            // log the user out
            // Clear all items in session storage
            sessionStorage.clear();
            // Replace the current state in the session history
            window.history.replaceState(null, "", "/login");
            navigate('/login')
        } else {
            console.log(apiResponse.error)
        }
    }

    // if user watns to delete their own account
    async function deleteAccount(){
        // navigate to registration page
        //navigate("/register")
    }

    return (
        <div className="accessSite">
            <h2>Welcome to your User Profile!</h2>
            <span>This is where you can manage information related to your ChronoMarket account, such as updating your
                username and/or password, or suspending your account.</span>
            <div className="update-info">
                <label>Update Username: </label>
                <input className="update-username" name="update-username"></input>
                <button key="update-username-button" onClick={() => updateInfo("username")}>Update</button>
                <label>Update Account Password: </label>
                <input className="password" type="password" name="password"/>
                <button key="update-password-button" onClick={() => updateInfo("password")}>Update</button>
            </div>
            <button id="suspendAccount" onClick={suspendAccount}>Suspend Account</button>
            <button id="deleteAccount" onClick={deleteAccount}>Delete Account</button>
        </div>
    )
}

export default UserProfilePage;