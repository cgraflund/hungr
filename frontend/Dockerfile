# Stage 1: Build the frontend with Node
FROM node:20-alpine AS builder
WORKDIR /app

# Copy package.json and package-lock.json first (better caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the code
COPY . .

# Build the app
RUN npm run build


# Stage 2: Serve with Nginx
FROM nginx:alpine
# Copy built frontend into nginx html dir
COPY --from=builder /app/dist /usr/share/nginx/html

# Remove default nginx config & replace with ours
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

# Expose port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
