# ea-redis EA4 container based package

This package sets up a user specific memcached container.

## Using it

Any thing that can talk to redis can use it via the unix socket `~/<CONTAINER_NAME>/redis.sock`.

## Security

This is secure overall because the unix socket is owned by the user so no other non-root users can get/set data in this redis.

You can add a layer of separation on the app level by installing it more than once to have different containers so that individual apps can have their own redis.
