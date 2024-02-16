{
  /* import modules for express and proxy server*/
}
const express = require("express");
const httpProxy = require("http-proxy");
const cors = require("cors"); // Import the cors middleware
const axios = require("axios");
//const os = require('os');

{
  /* initialize instances */
}
const app = express();
const proxy = httpProxy.createProxyServer();

{
  /* define various backend routes for Flask microservices */
}
const backendRoutes = {
  "/api/accounts": "http://host.docker.internal:3900",
  "/api/bidding": "http://host.docker.internal:9900",
  "/api/notifications": "http://host.docker.internal:7777",
  "/api/auction": "http://host.docker.internal:4000",
  "/api/item": "http://host.docker.internal:3901",
  "/api/message_broker": "http://rabbitmq-flask-server:3750",
}

app.use(cors());
// register middleware function to intercept HTTP requests
app.use(async (request, response, next) => {
  // check if there is a valid backend route configured by the gateway for the incoming request
  const microservice = request.path.split("/")[2];
  const path = "/api/" + microservice;
  const backendURL = backendRoutes[`${path}`];

  // make API request to check if valid username/password credentials
  async function validate() {
    const requestParams = {
      method: "GET",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: request.headers["authorization"],
      },
    };
    try {
      // make login request to API gateway
      const apiResponse = await axios.get(
        "http://host.docker.internal:3900/api/accounts/validate",
        requestParams
      );
      if (apiResponse.status === 200) {
        console.log("Authentication successful.");
        return true;
      } else {
        console.error("Error:", apiResponse.data);
        return false;
      }
    } catch (e) {
      console.error(e);
      return false;
    }
  }
  let shouldValidate = true;
  // if not logging in or registering, validate API token
  // login or register will not provide an Authorization token, every other request must
  if (request.headers["authorization"]) {
    shouldValidate = await validate();
  }
  if (shouldValidate) {
    // if a valid URL, route request accordingly
    if (backendURL) {
      // Add the host IP to the request headers before proxying - this is for RabbitMQ
      // consumer to communicate with local Flask servers
      //request.headers['Host-Ip'] = os.networkInterfaces().eth0[0].address;
      proxy.web(request, response, { target: backendURL });
    } else {
      response.status(404).send("Request URL Not Found.");
    }
  } else {
    response.status(401).send("Invalid API token request.");
  }
});

// deal with proxy errors
proxy.on("error", (err, req, res) => {
  console.error(err);
  res.status(500).send("Proxy Server Error");
});

// listen for proxy server requests on port 3500
const PORT = 3500;
app.listen(PORT, "0.0.0.0", () => {
  console.log(`Gateway server listening on port ${PORT}`);
});
