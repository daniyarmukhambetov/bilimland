FROM nginx:1.25

# Remove default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create directory for static files
RUN mkdir -p /app/staticfiles