# Developer Mode

Developer mode is extension-oriented and intended to support:

- Plugin system for custom workflows
- Custom AI agents
- Local model backends
- Gemini/OpenAI/Ollama provider adapters

The AI core is structured so provider integrations can be injected in place of
`GeminiClient` while keeping the same `ActionProposal` safety contract.
