# Slacks aka SlackSay

This is a small CLI utility that can be used in scripts to send slack messages via Incoming Webhooks. 

See: https://cloud.docker.com/u/hicrondss/repository/docker/hicrondss/slacks

## Usage

### Docker

Pull tha latest image:

```bash
docker pull hicrondss/slacks:latest
```

You only need to pass your Incoming Webhook as environment variable. This will send a message to the channel configured in your Slack webhook:

```
export MY_WEBHOOK_URL=https://hooks.slack.com/services/XXXXXXXXX/YYYYYYYYYYYYYYY
echo "*Hello, world!*" | docker run -e WEBHOOK_URL=${MY_WEBHOOK_URL} -i hicrondss/slacks:latest
```

### CLI Help

```bash
docker run -i hicrondss/slacks:latest -h
```

```txt
usage: slacks.py [-h] [-f [FILE]] [-m [MESSAGE]] [-b] [-t] [-p]

optional arguments:
  -h, --help            show this help message and exit
  -f [FILE], --file [FILE]
                        use contents of a FILE as text message
  -m [MESSAGE], --message [MESSAGE]
                        pass message as string
  -b, --block           Message will be a markdown block
  -t, --test            Use exapmle from example.py
  -p, --plaintext       Format with plaintext instead of markdown
```
