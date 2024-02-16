# parent image is Node.js runtime
FROM node:14 

# set working directory in the container
WORKDIR /usr/src/app

# copy application code into container
COPY . .

# install dependencies
RUN npm install 
RUN npm install cors
RUN npm install axios

# Expose port 3500 to the outside world (default port for Node.js apps)
EXPOSE 3500

# Command to run the application
CMD ["node", "gateway.js"]
