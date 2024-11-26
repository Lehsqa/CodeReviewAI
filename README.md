# About

Backend prototype for a Coding Assignment Auto-Review Tool using Python. This tool will help automate the process of 
reviewing coding assignments by leveraging OpenAl's GPT API (or alternative) for code analysis and the GitHub API for 
repository access.

# 🔨 Setup the project locally

## 🚧 Mandatory steps

Clone the project from GitHub

```bash
git clone git@github.com:InfinitePL/relo_quick_backend.git
```

## 🏃‍♂️ Run the application

```bash
# dev
make backend.run
```

## 🔧 Configure the project

The project could be configurable by using the environment variables.

For better development experience - the pydantic Config feature is used (_described in the config.py file_). It means that you can configure any variable that is encapsulated in the `src/config.py:setting` object by setting the environment variable in the session where you run the application.

Read more about [Pydantic Settings](https://docs.pydantic.dev/latest/usage/pydantic_settings/)

#### Using `.env` file

```bash
# create the .env file base on the .env.default file
cp .env.default .env

# export all environment variables on Unix
set -o allexport; source .env; set +o allexport
```

## 📈 What If

#### 🧰 Backend

- `Infrastructure and Scalability`: Deploy the application using container orchestration platforms like Kubernetes or Docker Swarm on cloud services such as AWS, Azure, or Google Cloud. This setup allows horizontal scaling, where multiple instances of the application can run concurrently behind a load balancer to distribute incoming traffic evenly.

- `Asynchronous Processing`: Implement a task queue using systems like Celery with RabbitMQ or Redis as the message broker. When a review request comes in, the API quickly enqueues the task and returns a response acknowledging receipt. Background workers then pick up tasks from the queue to process them asynchronously, which prevents blocking the main thread and improves throughput.

#### 🤖 API Rate Limits and Cost Management

- `GitHub API`: Authenticate all requests using a GitHub App or OAuth tokens to benefit from higher rate limits. Need to consider setting up a middleware to throttle requests and back off when approaching rate limits.

- `OpenAI API`: Optimize prompts to be concise to reduce token usage, thereby lowering costs. Monitor usage patterns and consider batch processing multiple code files in a single API call if it aligns with OpenAI's policies.

- `Monitoring and Alerting`: Set up monitoring tools like Prometheus and Grafana to keep track of system performance, API usage, and error rates. Configure alerts to notify the team when metrics exceed thresholds, enabling proactive scaling or troubleshooting.

- `Reliability and Fault Tolerance`: Use managed services with high availability and automatic failover capabilities. Implement retries with exponential backoff for transient errors when communicating with external APIs. Ensure data is backed up and that the system can recover gracefully from failures.

- `Cost Management`: Regularly review resource utilization and optimize the infrastructure to balance performance and cost. Consider reserved instances or savings plans if using AWS, or equivalent options on other cloud platforms, to reduce long-term costs.