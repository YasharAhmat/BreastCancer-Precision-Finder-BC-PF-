# BreastCancer Precision Finder (BC-PF) - Backend

## Project Overview

BreastCancer Precision Finder is a patient-centered web platform that democratizes access to clinical trials through intelligent matching and simplified presentation. The backend serves as the core intelligence layer, implementing the matching algorithms, business logic, and data persistence that power the application.

## High-Level Architecture

```
┌─────────────────┐
│   Patient/User  │
└─────────┬───────┘
          │
┌─────────▼───────┐
│ React.js        │
│ Frontend        │
└─────────┬───────┘
          │
┌─────────▼───────┐
│ Python Backend  │  ← YOUR RESPONSIBILITY
│ API (Flask)     │
└──┬────┬────┬───┘
   │    │    │
   ▼    ▼    ▼
┌──────┐ ┌────────┐ ┌──────────┐
│Match │ │PostgreSQL│ │External  │
│Logic │ │Database  │ │APIs      │
│      │ │          │ │(Data Lead)│
└──────┘ └────────┘ └──────────┘
```

## Core Functionality

The backend provides four primary capabilities:

### 1. Patient Profile Management
- Store patient demographics (age, location, gender)
- Manage biomarker data (ER, PR, HER2 status)
- Automatically classify patients into molecular subtypes
- Maintain patient history and preferences

### 2. Clinical Trial Matching Engine
- **Rule-based matching algorithm** (core backend responsibility)
- Match patients to trials based on:
  - Molecular subtype (Triple-Negative, Luminal A/B, HER2+)
  - Age and demographic criteria
  - Geographic location
  - Treatment history and contraindications
- Generate confidence scores (0-100%) for each match
- Provide plain-language explanations for match results

### 3. Trial Data Access
- Query stored clinical trial data (populated by Data/API team)
- Filter trials by phase, location, and enrollment status
- Retrieve detailed trial information
- Cache frequently accessed data for performance

### 4. API Layer
- RESTful API endpoints for frontend consumption
- Request validation and error handling
- Consistent response formatting
- Authentication and session management

## Technology Stack

### Core Framework
- **Python 3.9+**: Primary programming language
- **Flask 3.0+**: Lightweight web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Relational database

### Key Libraries
- **Flask-RESTful**: REST API development
- **Flask-CORS**: Cross-origin resource sharing
- **python-dotenv**: Environment variable management
- **pytest**: Testing framework
- **gunicorn**: Production WSGI server

### External Integrations (Handled by Data/API Team)
- ClinicalTrials.gov API v2.0
- Synthea FHIR Server
- HAPI FHIR Test Server

## Project Structure

```
┌─────────────────┐
│  Data/API Lead  │  ← UPSTREAM (Data Source)
│  (Upstream)     │
└────────┬────────┘
         │ Provides data to...
         ▼
┌────────────────┐
│  Backend Lead  │  ← YOU (Data Consumer & Processor)
│  (YOU)         │
└────────┬───────┘
         │ Provides APIs to...
         ▼
┌────────────────┐
│ Frontend Lead  │  ← DOWNSTREAM (Data Consumer)
│ (Downstream)   │
└────────────────┘


bc_pf_backend/
│
├── app/                                    # Core application package
│   ├── __init__.py                         # App factory & initialization
│   ├── config.py                           # Environment configurations
│   ├── extensions.py                       # Flask extensions (DB, CORS)
│   │
│   ├── models/                             # Database ORM models
│   │   ├── __init__.py                     # Model package exports
│   │   ├── patient.py                      # Patient schema & methods
│   │   ├── trial.py                        # Trial schema & methods
│   │   └── match.py                        # Match results schema
│   │
│   ├── routes/                             # API endpoint definitions
│   │   ├── __init__.py                     # Routes package init
│   │   ├── patient_routes.py               # Patient CRUD endpoints
│   │   ├── trial_routes.py                 # Trial & matching endpoints
│   │   └── healthcheck.py                  # Health monitoring endpoint
│   │
│   ├── services/                           # Business logic layer
│   │   ├── __init__.py                     # Services package init
│   │   ├── match_service.py                # ⭐ Core matching algorithm
│   │   └── trial_service.py                # ⏳ Trial data population (Data/API)
│   │
│   └── utils/                              # Helper utilities
│       ├── __init__.py                     # Utils package init
│       ├── validators.py                   # Input validation functions
│       └── formatters.py                   # Response formatting functions
│
├── tests/                                  # Test suite
│   ├── __init__.py                         # Tests package init
│   ├── conftest.py                         # Pytest fixtures & config
│   ├── test_patient_routes.py              # Patient API endpoint tests
│   ├── test_trial_routes.py                # Trial API endpoint tests
│   └── test_matching_engine.py             # Matching algorithm tests
│
├── scripts/                                # Utility scripts
│   ├── init_db.py                          # Database initialization
│   └── load_trials.py                      # CSV trial loader (backup)
│
├── .env                                    # Environment variables (NOT IN GIT)
├── .env.example                            # Example env template
├── .gitignore                              # Git ignore rules
├── requirements.txt                        # Python dependencies
├── run.py                                  # Application entry point
└── README.md                               # Project documentation


```

## API Endpoints

### Patient Management
```
POST   /api/patient          Create new patient profile
GET    /api/patient/<id>     Retrieve patient by ID
PUT    /api/patient/<id>     Update patient information
DELETE /api/patient/<id>     Delete patient profile
```

### Trial Matching
```
GET    /api/trials                  List all available trials
POST   /api/trials/match            Match patient to trials
GET    /api/trials/<nct_id>         Get detailed trial information
GET    /api/trials/filter           Filter trials by criteria
```

### System Health
```
GET    /api/health                  Backend service health check
```

## Matching Algorithm

The core matching engine (`services/match_service.py`) implements a rule-based algorithm that:

1. **Classifies Patient Subtype**
   - Triple-Negative (ER-/PR-/HER2-)
   - HER2-Positive (HER2+)
   - Luminal A/B (ER+ and/or PR+)

2. **Filters Eligible Trials**
   - Matches molecular subtype
   - Checks age eligibility
   - Validates demographic requirements

3. **Calculates Confidence Scores**
   - Subtype match: 40 points
   - Age eligibility: 20 points
   - Location proximity: 20 points
   - Additional criteria: 20 points
   - **Total: 0-100% confidence**

4. **Generates Explanations**
   - Plain-language reasons for each match
   - Highlights why patient is eligible
   - Identifies potential barriers

## Database Schema

### Patient Model
```python
- id (Primary Key)
- age (Integer)
- location (String)
- gender (String)
- er_status (String: Positive/Negative)
- pr_status (String: Positive/Negative)
- her2_status (String: Positive/Negative)
- subtype (String: Computed from biomarkers)
- created_at (DateTime)
```

### Trial Model
```python
- id (Primary Key)
- nct_id (String: Unique identifier)
- title (String)
- phase (String: I, II, III, IV)
- status (String: Recruiting, Active, etc.)
- target_subtype (String)
- eligibility_criteria (JSON)
- locations (JSON: Array of sites)
- min_age / max_age (Integer)
- last_updated (DateTime)
```

### Match Model
```python
- id (Primary Key)
- patient_id (Foreign Key)
- trial_id (Foreign Key)
- confidence_score (Float: 0.0-100.0)
- match_reasons (JSON: Array of explanations)
- created_at (DateTime)
```

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- PostgreSQL 12 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd bc_pf_backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Initialize database**
```bash
flask db upgrade
```

6. **Run development server**
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage report:
```bash
pytest --cov=app tests/
```

## Development Workflow

### Backend Lead Responsibilities
1. **Design and implement API endpoints** in `routes/`
2. **Define database schemas** in `models/`
3. **Build core matching algorithm** in `services/match_service.py`
4. **Create validation logic** in `utils/validators.py`
5. **Write comprehensive tests** in `tests/`
6. **Document API contracts** for frontend team
7. **Optimize database queries** and performance

### Collaboration Points

**With Data/API Lead:**
- Receive cleaned trial data for database population
- Consume parsed pathology report data
- Define data format requirements

**With Frontend Lead:**
- Provide API documentation and examples
- Define request/response schemas
- Coordinate on error handling

**With Integration/QA Lead:**
- Support integration testing
- Fix bugs identified in testing
- Optimize deployment configuration

## API Request/Response Examples

### Create Patient
**Request:**
```json
POST /api/patient
{
  "age": 45,
  "location": "Philadelphia, PA",
  "gender": "Female",
  "biomarkers": {
    "er_status": "Negative",
    "pr_status": "Negative",
    "her2_status": "Negative"
  }
}
```

**Response:**
```json
{
  "id": 1,
  "age": 45,
  "location": "Philadelphia, PA",
  "subtype": "Triple-Negative",
  "created_at": "2025-10-19T16:00:00Z"
}
```

### Match Patient to Trials
**Request:**
```json
POST /api/trials/match
{
  "patient_id": 1,
  "max_distance_miles": 50,
  "preferred_phases": ["Phase II", "Phase III"]
}
```

**Response:**
```json
{
  "count": 3,
  "matches": [
    {
      "trial": {
        "nct_id": "NCT12345678",
        "title": "KEYNOTE-522 Extension Study",
        "phase": "Phase III",
        "status": "Recruiting",
        "location": "Penn Medicine - 8 miles"
      },
      "confidence": 92.0,
      "reasons": [
        "Trial targets Triple-Negative breast cancer",
        "Age 45 within trial range (18-75)",
        "Trial site within 8 miles of patient location"
      ],
      "recommendation": "Excellent match - highly recommended"
    }
  ]
}
```

## Environment Variables

```bash
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/bcpf_db

# Flask Configuration
FLASK_ENV=development
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True

# Application Settings
MAX_CONTENT_LENGTH=5242880  # 5MB file upload limit
```

## Performance Considerations

- **Database indexing** on frequently queried fields (subtype, age, location)
- **Query optimization** for trial matching operations
- **Response caching** for static trial data
- **Pagination** for large result sets
- **Connection pooling** for database efficiency

## Security Considerations

- **Input validation** on all API endpoints
- **SQL injection prevention** via SQLAlchemy ORM
- **CORS configuration** restricted to frontend domain
- **Environment variable protection** (.env not in version control)
- **Rate limiting** (future implementation)

## Future Enhancements

- Advanced AI-powered pathology parsing integration
- Historical outcomes analysis and prediction
- SMART on FHIR provider integration
- Enhanced geographic filtering with travel time
- Multi-language support
- Real-time trial status notifications

## Contributing

Backend development follows these principles:
- **Clean Code**: PEP 8 style guidelines
- **Documentation**: Docstrings for all functions
- **Testing**: Minimum 80% code coverage
- **Git Workflow**: Feature branches with pull requests
- **Code Review**: Required before merging to main

## Team Contact

**Backend Lead**: [Your Name]
**Data/API Lead**: [Team Member Name]
**Frontend Lead**: [Team Member Name]
**Integration/QA Lead**: [Team Member Name]

## License

This project is developed as part of a healthcare informatics course at Georgia Institute of Technology.

---

**Last Updated**: October 19, 2025