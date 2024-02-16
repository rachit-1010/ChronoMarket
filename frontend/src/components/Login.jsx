import React from 'react';
import '../styles/login.css';
import { useNavigate } from 'react-router-dom';
import { makeApiRequest } from './apiUtils';

// login page
function LoginPage ({onSuspendedUser, onLoginClick, onAdminLogin}) {
    // navigator to update page state and trigger router
    const navigate = useNavigate();
    const [suspended, setSuspended] = React.useState(false)

    async function login(){
        // get the input username and password 
        const username = document.querySelector('.username');
        const password = document.querySelector('.password');

        // make API request to check if valid username/password credentials
        const requestParams = {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value,
              }),
        };
        try {
            // make login request to API gateway
            const apiResponse = await fetch('http://localhost:3500/api/accounts/login', requestParams);
            const data = await apiResponse.json();
            // successful login
            if (apiResponse.status === 200) {
                if (data["status"] === "suspended") {
                    // store API token so user can make unsuspend request
                    sessionStorage.setItem("apiKey", data["api_key"])
                    // navigate user to the suspended page
                    setSuspended(true)
                    return
                }
                console.log('Success:', data);
                let user_id = data["user_id"]
                let email = data["email"]
                let admin_status = data["admin_status"]
                let api_key = data["api_key"]
                let username = data["username"]
                
                // store element in session storage
                sessionStorage.setItem('adminStatus', admin_status);
                sessionStorage.setItem('userId', user_id);
                sessionStorage.setItem('email', email);
                sessionStorage.setItem('apiKey', api_key);
                sessionStorage.setItem('username', username);

                // update admin state if user is an admin
                if (admin_status == "1") {
                    onAdminLogin();
                    onLoginClick();
                    // navigate to admin home page
                    navigate("/admin/home")
                }
                else {
                    // update parent/inhereted state for log in
                    onLoginClick();
                    // navigate to user home page
                    navigate("/user/home")
                }
            // error logging in
            } else {
                // if user is blocked
                if (data["status"] === "blocked") {
                    console.error('Error:', data);
                    alert ("That email address is blocked.")
                }
                else{
                    // username or password is wrong
                    console.error('Error:', data);
                    alert ("Your username or password is incorrect, please try again!")
                }
                return;
            }
        } catch (e) {
            console.log(e)
            return e;
        }
    }

    // if user wants to suspend their own account
    async function unsuspendAccount(){
        let apiUrl = 'http://localhost:3500/api/accounts/user/unsuspend'
        const apiResponse = await makeApiRequest('POST', apiUrl)
        if (apiResponse.success) {
            alert ("You've successfully unsuspended your account.")
            setSuspended(false)
            navigate("/login")
        } else {
            console.log(apiResponse.error)
        }
    }

    // if user wants to register, need to push that route to the browser
    async function register(){
        // navigate to registration page
        navigate("/register")
    }

    return (
        <div className="accessSite">
            {/* user is suspended */}
            {suspended ? (
                <div>
                    <p>Your account is currently suspended.</p>
                    <button key="unsuspendButton" onClick={unsuspendAccount}>Unsuspend Account</button>
                </div>
            ) : 
            (
                <div>
                    <h1>ChronoMarkets</h1>
                    <img id="logo-image" src="/images/logo.JPG" alt="ChronoMarket Logo"></img>
                    <br/>
                    <span>
                        We are the premier marketplace for watch enthusiasts around the globe. You've been waiting for this, so it's Time to 
                        stop by and see what we can offer you.
                    </span>
                    <h4>Enter your username and password to log in:</h4>
                    <div className="login">
                        <label>Username</label>
                        <input className="username" name="username"></input>
                        <button key="loginButton" onClick={login}>Login</button>
                        <label>Password</label>
                        <input className="password" type="password" name="password"/>
                        <button key="registerButton" onClick={register}>Register</button>
                    </div>
                </div>
            )}
        </div>
    )
}

export default LoginPage;