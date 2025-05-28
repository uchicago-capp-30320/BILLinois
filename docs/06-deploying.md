# Deployment

We use Docker and the remote `turing` server to deploy our app.

Make sure the most recent `Dockerfile` and `docker-compose.yaml` are updated to the remote server.

Then, from within the server, run:

```
docker-compose build
docker-compose down
docker-compose up --d
```

These commands will take the existing machine down and put a newly built one up.

## Using a custom domain

Cite: James Turk

The person who owns the domain needs to add a DNS record. To do that you login to the interface of the site you bought the domain on, look for DNS and then add a record with these properties this would make it available at yourdomain.org:

```
subdomain/host: @
record type: A
IP: YOUR_IP_ADDRESS
TTL: DEFAULT
```

If you prefer www.yourdomain.org, you could use `subdomain/host: www`.
