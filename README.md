# Song Translator – Backend

🚧 **Status:** Work in Progress

Backend of the **Song Translator** web application.  
It is responsible for fetching song lyrics, translating them, and storing the results in the database.

The backend exposes REST APIs used by the Flutter frontend.

---

## Tech Stack

- **Flask** – Python web framework
- **Firebase** – database for storing translations and metadata
- **Redis** – message broker for background tasks
- **RQ (Redis Queue)** – task queue for handling translation jobs
- **OpenAI API (ChatGPT)** – used for automatic song translation

---

## Architecture

The translation process is handled asynchronously:

User request  
→ Flask API  
→ Redis Queue (RQ worker)  
→ Background worker processes translation  
→ OpenAI API generates translation  
→ Result stored in Firebase

---

## Deployment

The project includes a dedicated **`render` branch**, which contains a lightweight version of the API.

This version is deployed on **Render (free tier)** and only exposes the REST API endpoints for data access.

---

## Work in Progress

The current limitation is the deployment environment:

- The Render free tier does **not support full background processing with Redis + RQ workers**
- Because of this, only the API layer is deployed on Render

### Planned improvements:

- [ ] Self-host the full backend locally or on a VPS
- [ ] Enable full Redis + RQ worker support
- [ ] Unify API + background processing in a single deployment
- [ ] Improve scalability of translation pipeline
- [ ] Add authentication system for users

---

## Project Status

This backend is currently split between:

- A full local development version (with background workers)
- A production API-only version deployed on Render
