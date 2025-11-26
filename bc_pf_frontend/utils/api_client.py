import requests

API_BASE = "https://bc-pf-backend-eraeasb6cfbhc7f6.canadacentral-01.azurewebsites.net/api/health"  # Update if your backend is deployed elsewhere


def match_patient_to_trials(patient_data):
    """
    Send patient data to the backend matching endpoint.

    Args:
        patient_data: Dictionary containing patient information

    Returns:
        Dictionary with match results or error information
    """
    try:
        resp = requests.post(
            f"{API_BASE}/trials/match",
            json=patient_data,
            timeout=10
        )

        if resp.status_code != 200:
            return {
                "error": True,
                "message": f"Backend error: {resp.status_code} - {resp.text}"
            }

        return resp.json()

    except requests.exceptions.ConnectionError:
        return {
            "error": True,
            "message": "Cannot connect to backend. Is the server running?"
        }
    except requests.exceptions.Timeout:
        return {
            "error": True,
            "message": "Request timed out. Backend may be overloaded."
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"API Error: {str(e)}"
        }
