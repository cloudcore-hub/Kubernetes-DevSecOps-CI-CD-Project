# Use the official Apache HTTPD image
FROM httpd:2.4

# Copy your frontend application files to the document root
COPY ./static /usr/local/apache2/htdocs/static/
COPY ./templates /usr/local/apache2/htdocs/

# The default port for Apache is 80
EXPOSE 80
