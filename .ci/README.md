# CI

## Local Development

You can currently get Enterprise Search running locally with docker-compose,
run `docker-compose up` from this directory to get everything set up.
You need to set the value of `STACK_VERSION` in your environment:

```bash
$ STACK_VERSION=7.7.0 docker-compose up
```

You can check it's working with:
```bash
curl http://localhost:8080/swiftype-app-version
```

or you can start everything and wait for it to become available
with one bash script:

```bash
$ STACK_VERSION=7.7.0 .ci/start-stack.sh
```

and stop everything when you're done:

```bash
$ STACK_VERSION=7.7.0 .ci/stop-stack.sh
```
