## How To Run (Docker)

1. Install Docker
2. Add Alpha Vantage API key as text file named `alpha_vantage_api_key.txt` under secrets directory
3. Run `docker compose up`
4. Visit `localhost:8000/docs` for API docs
5. Try one out using curl. ie `curl localhost:8000/lookup/AAPL/2023-05-26`


## How To Run (Local)

1. Install Python v3.11.2 and pip
2. Run `pip install -r requirements.txt`
2. Add Alpha Vantage API key to an .env file with key `ALPHA_VANTAGE_API_KEY`
3. Run `uvicorn app.main:app --host 0.0.0.0 --port 8000`
4. Visit `localhost:8000/docs` for API docs
5. Try one out using curl. ie `curl localhost:8000/lookup/AAPL/2023-05-26`


## Discussion
- What compromises did you make due to time constraints?
  - No tests. No error handling with proper status codes. Code comments. API Docs. Set up mypy/flake8/isort/black config files
- What would you do differently if this software was meant for production use?
  - Monitoring. Adjusting cache size/ttl. Auth. Rate Limiting. Unit/Integration Tests
- Propose how you might implement authentication, such that only authorized users may hit these endpoints.
  - https://fastapi.tiangolo.com/tutorial/security/
- How much time did you spend on this exercise?
  - ~3 hours.
- Please include any other comments about your implementation.
  - Cached sorted results from AlphaVantage. Docker secrets. Docker development.
- Please include any general feedback you have about the exercise.
  - It was enjoyable as far as case studies go.