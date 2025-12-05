# LLM Court

LLM Court is an autonomous adversarial system that forces AI to debug its own code before showing it to you.

## The Idea

The idea of this repo is that LLMs are sycophants. If you ask a standard model for a Python script with a specific (but bad) implementation, it will often write insecure or buggy code just to agree with you. The "Yes Man" failure mode creates technical debt.

LLM Court solves this by treating code generation as a judicial process. It orchestrates a closed loop of specialized agents—a **Defense** (builder), a **Prosecution** (critic), and a **Judge** (router). The system debates the code, finds security flaws or complexity issues, and rewrites the solution iteratively until it passes the bar.

It uses **LangGraph** to manage the state machine (it's a cycle, not a chain) and **Groq** to make the multi-turn debate happen in seconds rather than minutes.

## The Architecture

The system is a cyclic graph composed of five distinct agents:

  * **The Archivist (Memory):** Before coding, it queries **PostgreSQL (pgvector)** to see if we've solved similar cases before. It injects successful precedents into the context to prevent amnesia.
  * **The Investigator (Vision):** If you upload a screenshot, **Llama 4 Scout** extracts the structural intent (UI layout, colors) so the code matches the pixels.
  * **The Defense (Builder):** Uses high-throughput models (GPT-OSS-20B) to draft the initial solution rapidly.
  * **The Prosecutor (Critic):** A hostile agent (Llama 3.3 70B) prompted to find security vulns, O(n^2) complexity, and logic errors. It is explicitly forbidden from being "nice."
  * **The Judge (Router):** Reviews the Prosecutor's argument. If valid (`guilty`), it sends the case back to Defense for a rewrite. If trivial (`acquitted`), it returns the final code to the user.

## Speed & Stack Hacks

This isn't a standard RAG app. To make an adversarial loop usable, I had to optimize for extreme low latency.

  * **Inference:** I use **Groq LPUs** instead of GPUs. This allows Llama 3 to run at \~1000 tokens/sec. Without this, waiting for the "courtroom drama" to finish would take too long.
  * **The Monolith:** Instead of a complex microservice DB mess, I use a single Postgres instance for *both* relational data and vector embeddings.
  * **Package Management:** The repo uses `uv` (Rust-based) instead of pip for instant environment setups.

## Setup

1.  **Infrastructure:**

    ```bash
    # Starts the Postgres Monolith (Vector + SQL)
    docker-compose up -d
    ```

2.  **Dependencies:**

    ```bash
    uv sync
    ```

3.  **Run:**

    ```bash
    make up
    ```

4.  **Verdict:**
    Go to `http://localhost:8000` and submit a case (e.g., "Write a secure SQL query function"). Watch the Prosecutor attack the first draft.

## License

MIT