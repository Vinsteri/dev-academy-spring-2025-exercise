# --------
# Stage 1: Build
# --------
    FROM node:18-alpine AS build

    # Create and switch to the working directory
    WORKDIR /app
    
    # Copy package.json and package-lock.json OR yarn.lock first
    # (This ensures we only re-run npm install when dependencies change)
    COPY package*.json ./
    # COPY yarn.lock ./
    
    # Install dependencies
    RUN npm install
    
    # Copy the rest of your app’s source code
    COPY . .
    
    # Build the React + Vite app
    RUN npm run build
    
    # --------
    # Stage 2: Serve with Nginx
    # --------
    FROM nginx:1.23-alpine
    
    # Copy built files from previous stage to Nginx html folder
    COPY --from=build /app/dist /usr/share/nginx/html
    
    # Expose port 80 to the outside world
    EXPOSE 80
    
    # Start Nginx when the container launches
    CMD ["nginx", "-g", "daemon off;"]
    