# AWSome kubernetes dashboard with AWS Docker Registry tag resolving

Since we have here a number of clusters and environments, I manage to build a little python dashboard. It just generate a static html file with all interesting things running around. You can instantly see what is going on like:

- who is restarting
- what is the reason (OOM killed etc...)
- docker image names
- other docker tags pointing on the same checksum (work only with AWS docker registry)

## How to run

- modify config.yml
- make sure your host is connected to kubernetes (check ~/.kube)
- also connected to aws (~./aws)
- pip3 install poetry
- poetry install
- poetry shell
- ./fetch > out.json
- ./render html.pug < out.json > status.html
- open status.html

## Screens

![screen with aws](https://raw.githubusercontent.com/atolia/awsome/oss/aws.png)
![screen with no aws](https://raw.githubusercontent.com/atolia/awsome/oss/no-aws.png)
