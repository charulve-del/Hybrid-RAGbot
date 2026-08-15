# ============================================================
# BUILD STAGE
# ============================================================

FROM node:22-alpine AS builder

WORKDIR /app

# Copy package files first
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy React source
COPY . .

# Build production application
RUN npm run build


# ============================================================
# PRODUCTION STAGE
# ============================================================

FROM nginx:alpine

# Replace default nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy React production build
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]