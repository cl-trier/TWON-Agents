# TWON: API - Generative Agent

The repository contains a REST API to inference with generative agents in a social media thread. The agents are powered by large language models through Hugging Face and OpenAi.

Note: Currently, the work is an alpha version and will undergo breaking changes during the development.

## Project Setup

```sh
# install Python requirements
make install

# update local repository and restart server
make update
```

## dotenv

The API assumes a valid Hugging Face and OpenAi API token inside the project repository in a dotenv file.

```toml
HUGGINGFACEHUB_API_TOKEN="hf_XXXXXXXXXXXXXXXXX"
OPENAI_API_KEY="sk-XXXXXXXXXXXXXXXXX"
```

### Start with Hot-Reload for Development

```sh
make dev
```

### Start for Production

```sh
make serve
```

### Unit Tests

```sh
make test
```
