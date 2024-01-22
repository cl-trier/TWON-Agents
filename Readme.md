# TWON: Agents - Generative Agent through LLMs

The repository contains a REST API to inference with generative agents in a social media thread. The agents are powered by large language models through Hugging Face and OpenAi.

Note: Currently, the work is an alpha version and will undergo breaking changes during the development.

## Project Setup

```sh
# install Python requirements
make install

# update local repository and restart server
make update

# start with hot-reload for development
make dev

# start for production
make serve

# run unit tests
make test
```

### dotenv

The API assumes a valid Hugging Face and OpenAi API token inside the project repository in a dotenv file.

```toml
HF_TOKEN="hf_XXXXXXXXXXXXXXXXX"
OPENAI_API_KEY="sk-XXXXXXXXXXXXXXXXX"
```

## Roadmap

- [x] Setup initial project structure
- [x] Add agents get and post routes
- [ ] Complete unit tests
- [ ] Add recommender route
