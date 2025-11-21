# Breast Cancer Patient Finder Frontend

**Built with Streamlit**

## Quickstart

1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

2. Ensure your backend Flask server is running at `http://localhost:5000`.

3. Launch Streamlit app:
    ```
    streamlit run app.py
    ```

4. Open your browser to `http://localhost:8501`.

## Configuration

- To point at a remote/deployed backend, change `API_BASE` in `utils/api_client.py`.

- Customize form fields and results display as needed for your users.

## Folders

- `app.py`          — Main Streamlit UI
- `utils/`          — API client code
- `.streamlit/`     — Optional Streamlit config

## Notes

- Keep your backend and frontend running in separate terminals.
- For production, consider securing the backend API and using HTTPS.

