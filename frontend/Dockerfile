# parent image is Node.js runtime
FROM node:14 

# set working directory in the container
WORKDIR /usr/src/app

# copy package files
COPY package*.json ./

# install dependencies
RUN npm install 

# copy application code into container
COPY . .

# Expose port 3000 to the outside world (default port for Node.js apps)
EXPOSE 3000

# Command to run the application
CMD ["npm", "start"]
