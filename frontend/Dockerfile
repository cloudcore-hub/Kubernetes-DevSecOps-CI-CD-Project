FROM nginx:1.25.4-alpine3.18
RUN rm -rf /usr/share/nginx/html/*
COPY ./static /usr/share/nginx/html/static
COPY ./templates /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
