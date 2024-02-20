# Use an official lightweight Nginx image
FROM nginx:alpine

# Copy static resources and templates
COPY static /usr/share/nginx/html/static
COPY templates /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx and keep it running
CMD ["nginx", "-g", "daemon off;"]
