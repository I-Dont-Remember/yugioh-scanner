# Yu Gi Oh Deck Tool API

When using `pipenv`, it's easiest to run `pipenv shell` to get inside a virtual environment and be able to run all commands within that shell.

## Deployment

Environment variables will be in `env.yml`.

Uses the serverless framework, so deployment is quite simple.  First install it with `npm i -g serverless`.
Then to deploy the full stack:
```
make
```

To redeploy the single main function:
```
make main
```

