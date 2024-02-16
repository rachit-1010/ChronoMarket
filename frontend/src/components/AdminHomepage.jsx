import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/admin_homepage.css';
import { makeApiRequest } from './apiUtils';

function AdminHomePage() {
    // navigator to update page state and trigger router
    const navigate = useNavigate();

    // React state for list of users
    const [listOfUsers, setUsersList] = React.useState(null)
    // React state for blocked users
    const [blockedUsers, setBlockedList] = React.useState(null)
    // React state for item categories
    const [listOfCategories, setCategoriesList] = React.useState(null)
    // React state for items flagged by users
    const [listFlaggeditems, setFlaggedItems] = React.useState(null)

    // React state for timeframe interval
    const [selectedInterval, setSelectedInterval] = useState('last24hours');
    // React state for closed/live auction information for admin metrics
    const [auctionMetrics, setAuctionMetrics] = React.useState(null)

    // function to log the admin out
    const Logout = () => {
        // Clear all items in session storage
        sessionStorage.clear();
        // Replace the current state in the session history
        window.history.replaceState(null, "", "/login");
        navigate('/login')
    }

    // function to block an email addres
    async function blockUser(){
        const emailAddressInput = document.querySelector('.block-email');
        const emailAddress = emailAddressInput.value;

        const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        // do some email validaton
        if (!emailAddress || !emailRegex.test(emailAddress)) {
            alert("The email address you entered isn't valid.");
            return;
        }

        let bodyParams = { email: emailAddress};
        let apiUrl = 'http://localhost:3500/api/accounts/admin/block'
        const apiResponse = await makeApiRequest('POST', apiUrl, bodyParams)
        if (apiResponse.success) {
            console.log("User has been blocked.")
            // clear out input value
            emailAddressInput.value = '';
            // update blocked users state to reflect the newly blocked email
            getBlockedUsers();
        }
    }

    // function for an Admin to get a list of all current blocked email addresses
    const getBlockedUsers = async () => {
        let apiUrl = 'http://localhost:3500/api/accounts/admin/get_blocked';
        const apiResponse = await makeApiRequest('GET', apiUrl)
        // if success
        if (apiResponse.success) {
            console.log(apiResponse.data)
            // if there are currently at least 1 blocked users
            setBlockedList(apiResponse.data);
            return { success: true, message: 'Blocked users retrieved successfully' };
        } else {
            // Handle the case when the API request is not successful
            console.log("API request issue. Error:", apiResponse.error);
            return { success: false, message: 'API request failed.', error: apiResponse.error };
        }
    };

    // function for an Admin to get a list of all current non-admin users
    const listUsers = async () => {
        let apiUrl = 'http://localhost:3500/api/accounts/admin/list';
        const apiResponse = await makeApiRequest('GET', apiUrl)
        // if success
        if (apiResponse.success) {
            // if there is currently at least 1 non-admin user
            setUsersList(apiResponse.data);
            return { success: true, message: 'Non-admin users retrieved successfully.' };
        } else {
            // Handle the case when the API request is not successful, i.e. no users
            console.log("API request issue. Error:", apiResponse.error);
            return { success: false, message: 'API request failed.', error: apiResponse.error };
        }
    };

    // function to get all current item categories
    const getItemCategories = async () => {
        let apiUrl = 'http://localhost:3500/api/item/get_brands'
        const apiResponse = await makeApiRequest('GET', apiUrl);
        if (apiResponse.success) {
            // update React state for current list of brand categories
            setCategoriesList(apiResponse.data);
            return { success: true, message: 'Brand categories retrieved successfully.' };
        } else {
            // Handle the case when the API request is not successful
            console.log("API request issue. Error:", apiResponse.error);
            return { success: false, message: 'API request failed.', error: apiResponse.error };
        }
    }

    // function to add a brand category to categories list
    async function addItemCategory(){
        const newCategoryInput = document.querySelector('.add-category');
        const newCategory = newCategoryInput.value;
        // pass the new brand category through brand_name field
        let bodyParams = { brand_name: newCategory};
        let apiUrl = 'http://localhost:3500/api/item/add_brand'
        const apiResponse = await makeApiRequest('POST', apiUrl, bodyParams)
        if (apiResponse.success) {
            console.log("New brand category has been added.")
            // clear out input value
            newCategoryInput.value = '';
            // update brand categories state to reflect the newly blocked email
            getItemCategories();
        }
    }

    //////////////////////////////////////////////////////////////
    /////////////////// TO FINISH ////////////////////////////////
    //////////////////////////////////////////////////////////////
    // function to get all current items that have been flagged by users
    const getFlaggedItems = async () => {
        // update this url
        let apiURL = 'http://localhost:3500/api/item_microservice/......'
        const apiResponse = await makeApiRequest('GET', apiUrl);
        if (apiResponse.success) {
            setFlaggedItems(apiResponse.data);
        }
    }

    // function to get all auctions closed after a certain date
    const getAdminMetrics = async () => {
        let startDate;
        // Calculate start date based on selected interval
        if (selectedInterval === 'last24hours') {
            startDate = "day"
        } else if (selectedInterval === 'lastWeek') {
            startDate = "week"
        } else if (selectedInterval === 'lastMonth') {
            startDate = "month"
        }

        // call endpoint to get number of closed auctions since currentDate - startDate 
        let apiUrl = `http://localhost:3500/api/auction/closed/count/${startDate}`
        const apiResponse = await makeApiRequest('GET', apiUrl)
        if (apiResponse.success) {
            // if there are closed auctions in the given timeframe,
            // update admin metrics state to show the closed auction data in the specified timeframe
            setAuctionMetrics(apiResponse.data.closed_auctions_count);
            console.log("Updated auction metrics:", auctionMetrics);
            return { success: true, message: 'Blocked users retrieved successfully' };
        } else {
            // Handle the case when the API request is not successful
            console.log("API request issue. Error:", apiResponse.error);
            return { success: false, message: 'API request failed.', error: apiResponse.error };
        }
    }

    // navigate admin to the customer support page
    async function navigateSupport(){
        // navigate to support page
        navigate("/admin/support")
    }

    // navigate admin to see all live auctions
    async function navigateLiveAuctions(){
        // navigate to auction page
        navigate("/admin/auctions")
    }

    // useEffect to poll for updates
    useEffect(() => {
        // Fetch initial user list, blocked user emails, and current brand categoires
        listUsers();   
        getBlockedUsers();
        getItemCategories();
        // add get flagged items call here
        // getFlaggedItems();
        
        // poll for new users every 10 seconds
        const intervalId = setInterval(() => {
            listUsers();
            // getFlaggedItems();
        }, 10000)

        // clean up interval when this JSX component is unmounted / not-rendered
        return () => clearInterval(intervalId);
    }, []);



    return (
        <div className="home-page">
            <h1>Administrators</h1>
            <button id="logout-button" onClick={Logout}>Logout</button>

            <div className="sections">
                <div id="manage-users-div" className="manage-div-1">
                    <h3 className="section-titles">Manage Users</h3>
                    {listOfUsers && (Object.keys(listOfUsers).length !== 0) ? (
                        <div className="list-objects" id="list-users">
                        {Object.keys(listOfUsers).map((key, index) => (
                            <div>
                                <user id={`user-${listOfUsers[key].id}`}>{listOfUsers[key].username}</user>
                                <br key={`br-${index}`} />
                            </div>
                        ))}
                        </div>
                    ) : null}
                </div>

                <div id="manage-blocklist-div" className="manage-div-1">
                    <h3 className="section-titles">Manage Blocklist</h3>
                    {blockedUsers && (Object.keys(blockedUsers).length !== 0) ? (
                        <div className="list-objects" id="list-blocked-users">
                        {Object.keys(blockedUsers).map((key, index) => (
                            <div>
                                <blocked id={`blocked-user-${index}`}>{blockedUsers[key].email}</blocked>
                                <br key={`br-${index}`} />
                            </div>
                        ))}
                        </div>
                    ) : null}
                    <input className="block-email" name="block-email"></input>
                    <button key="blockButton" onClick={blockUser}>Block Email</button>
                </div>
                
                {/* UPDATE THIS SECTION TO APPROPRIATELY SHOW ITEM CATEGORIES */}
                <div id="manage-categories-div" className="manage-div-1">
                    <h3 className="section-titles">Manage Categories (Brands)</h3>
                    {listOfCategories && (Object.keys(listOfCategories).length !== 0) ? (
                        <div className="list-objects" id="list-categories">
                        {Object.keys(listOfCategories).map((key, index) => (
                            <div>
                                <category id={`category-${key}`}>{listOfCategories[key].brand_name}</category>
                                <br key={`br-${index}`} />
                            </div>
                        ))}
                        </div>
                    ) : null}
                    <input className="add-category" name="add-category"></input>
                    <button key="addCategoryButton" onClick={addItemCategory}>Add Brand Category</button>
                </div>
            </div>
            <div className="sections">
                {/* UPDATE THIS SECTION TO APPROPRIATELY SHOW FLAGGED ITEMS INFORMATION */}
                <div id="see-flagged-div" className="manage-div-2">
                    <h3 className="section-titles">Items Flagged by Users</h3>
                    {listFlaggeditems && (Object.keys(listFlaggeditems).length !== 0) ? (
                        <div className="list-objects" id="list-flagged-items">
                        {Object.keys(listFlaggeditems).map((key, index) => (
                            <div>
                                <flagged id={`flagged-item-${listFlaggeditems[key].id}`}>{listFlaggeditems[key].email}</flagged>
                                <br key={`br-${index}`} />
                            </div>
                        ))}
                        </div>
                    ) : null}
                </div>

                {/* UPDATE THIS SECTION TO APPROPRIATELY SHOW ADMIN METRICS */}
                <div id="admin-metrics-div" className="manage-div-2">
                    <h3 className="section-titles">Auction Metrics</h3>
                    {/* Dropdown for selecting time interval */}
                    <select
                        id="metrics-dropdown"
                        value={selectedInterval}
                        onChange={(e) => setSelectedInterval(e.target.value)}
                    >
                        <option value="last24hours">Last 24 hours</option>
                        <option value="lastWeek">Last Week</option>
                        <option value="lastMonth">Last Month</option>
                    </select>

                    {/* Button to trigger API call to get metrics */}
                    <button id="calculate-metrics" onClick={getAdminMetrics}>Calculate</button>

                    <div className="" id="closed-auction-metrics">
                        <metric>There have been {auctionMetrics} auctions closed in the {selectedInterval}</metric>
                    </div>
                </div>
            </div>
            <div className="buttons-section">
                <button key="customerSupportButton" onClick={navigateSupport}>Manage Customer Support Inquiries</button>
                <button key="liveAuctionButton" onClick={navigateLiveAuctions}>Manage Live Auctions</button>
            </div>
        </div>
    )
}

export default AdminHomePage;