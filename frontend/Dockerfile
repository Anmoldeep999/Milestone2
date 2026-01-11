FROM alpine:3.20

# Install lighttpd
RUN apk add --no-cache lighttpd

# Copy website
COPY index.html /var/www/localhost/htdocs/index.html

# (optioneel) zorg dat document root klopt
RUN sed -i 's#server.document-root = ".*"#server.document-root = "/var/www/localhost/htdocs"#' /etc/lighttpd/lighttpd.conf

EXPOSE 80

CMD ["lighttpd", "-D", "-f", "/etc/lighttpd/lighttpd.conf"]
