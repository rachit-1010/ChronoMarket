import React from 'react';
import '../styles/login.css';
import { useNavigate } from 'react-router-dom';

// login page
function RegisterPage ({onLoginClick, onAdminLogin}) {
    // navigator to update page state and trigger router
    const navigate = useNavigate();

    async function register(admin_status){
        // get the input username and password 
        const username = document.querySelector('.username');
        const password = document.querySelector('.password');
        const email = document.querySelector('.email');

        const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        // do some email validaton
        if (!email.value || !emailRegex.test(email.value)) {
            alert("The email address you entered isn't valid.");
            return;
        }

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
                email: email.value,
              }),
        };
        try {
            // make login request to API gateway
            let api_url = ""
            if (admin_status == 1){
                api_url = "http://localhost:3500/api/accounts/admin/register"
            } else {
                api_url = "http://localhost:3500/api/accounts/user/register"
            }
            const apiResponse = await fetch(api_url, requestParams);
            const data = await apiResponse.json();
            // successful login
            if (apiResponse.status === 200) {
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
            // error registering
            } else {
                // if user is blocked
                if (data["status"] === "blocked") {
                    console.error('Error:', data);
                    alert ("That email address is blocked.")
                }
                else if (data["status"] === "duplicate") {
                    console.error('Error:', data);
                    alert ("That username is taken, please choose another.")
                }
                else{
                    // username or password is wrong
                    console.error('Error:', data);
                }
                return;
            }
        } catch (e) {
            console.log(e)
            return e;
        }
    }

    return (
        <div className="accessSite">
            <h3>Enter your username, password, and email to create an account:</h3>
            <div className="login">
                <label>Username</label>
                <input className="username" name="username"></input><br/>
                <label>Password</label>
                <input className="password" type="password" name="password"/><br/>
                <label>Email</label>
                <input className="email" name="email"></input><br/>
                <button key="registerButtonAdmin" onClick={() => register(1)}>Register Admin</button>
                <button key="registerButtonUser" onClick={() => register(0)}>Register User</button>
            </div>
        </div>
    )
}

export default RegisterPage;