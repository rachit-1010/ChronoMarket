// generic function to make API requests
async function makeApiRequest(method, apiEndpoint, additionalBodyParams = {}) {
  try {
    let apiKey = sessionStorage.getItem("apiKey");
    const requestParams = {
      method: method,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: apiKey,
      },
    };

    // Add body only if the method is not "GET"
    if (method !== "GET") {
      requestParams.body = JSON.stringify(additionalBodyParams);
    }

    console.log(requestParams.body);

    const apiResponse = await fetch(apiEndpoint, requestParams);
    const data = await apiResponse.json();

    if (apiResponse.status === 200) {
      console.log("Success:", data);
      return { success: true, data: data };
    } else {
      console.error("Error:", data);
      return { success: false, error: data };
    }
  } catch (e) {
    console.log(e);
    return { success: false, error: e };
  }
}

export { makeApiRequest };
