<<<<<<< HEAD
# BreastCancer Precision Finder (BC-PF) - Backend



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
├── run.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── patient.py
│   │   ├── trial.py
│   │   └── match.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── patient_routes.py
│   │   ├── trial_routes.py
│   │   └── healthcheck.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── match_service.py
│   │   └── trial_service.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       └── formatters.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_patient_routes.py
│   ├── test_trial_routes.py
│   └── test_matching_engine.py
│
├── scripts/
│   ├── init_db.py
│   └── load_trials.py


```

=======
# 🧬 CS6440 Group 35 Project  
## **BreastCancer Precision Finder (BC-PF)**  

### 👥 Collaborators  
- **Yixuan Song** – [ysong621@gatech.edu](mailto:ysong621@gatech.edu)  
- **Panfeng Yu** – [pyu301@gatech.edu](mailto:pyu301@gatech.edu)  
- **Ahemaitijiang Yaxiaer** – [ayaxiaer3@gatech.edu](mailto:ayaxiaer3@gatech.edu)  
- **Zijing He** – [zijingh@gatech.edu](mailto:zijingh@gatech.edu)  

---

## 🩺 Project Overview  

**BreastCancer Precision Finder (BC-PF)** is a **patient-centered web platform** that democratizes access to clinical trials through **AI-powered trial matching** and a **simplified, intuitive interface**.  

The platform empowers breast cancer patients to:
- Upload their **pathology reports** or manually enter **biomarker data** (ER/PR/HER2, genomic mutations).  
- Automatically receive **personalized matches** to relevant **clinical trials** based on their molecular subtype, demographics, and treatment history.  

---

## 🎯 Project Goals  

Deliver a **functional patient-facing prototype** that:  

1. **Accepts patient input**  
   - Allows uploading of pathology reports (PDF/text).  
   - Enables manual entry of key biomarkers (ER, PR, HER2, mutation info).  

2. **Extracts key biomarkers**  
   - Uses text analysis to identify and parse ER/PR/HER2 status.  

3. **Classifies patient subtype**  
   - Determines breast cancer subtype (e.g., HER2+, TNBC, Luminal A/B).  

4. **Fetches live clinical trial data**  
   - Integrates with **ClinicalTrials.gov API** to retrieve current trials.  

5. **Performs intelligent matching**  
   - Applies rule-based logic to match by subtype, age, location, and gender.  

6. **Displays results transparently**  
   - Presents matched trials with **confidence scores** and **clear explanations** of why each trial was selected.  

---

## 💡 Vision  

BC-PF aims to **bridge the gap between patients and clinical research** — providing clarity, empowerment, and timely opportunities for individuals navigating complex treatment landscapes.  

---

## ⚙️ Technologies (Planned / Used)  
- **Frontend:** 
- **Backend:**  
- **AI & NLP:**  
- **Data:**  
- **Storage:** 
- **Deployment:** Openshift 

---
>>>>>>> dc380ff6445a888dea09f2d07b5dee084e247dbd
