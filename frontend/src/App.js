import React, { useState, useEffect } from 'react';
import { Search, Users, FileText, Activity, Plus, Edit2, Trash2, Filter, MapPin } from 'lucide-react';

// API helper
const API_BASE = 'http://localhost:5050/api';

const api = {
  get: async (path) => {
    const res = await fetch(`${API_BASE}${path}`);
    if (!res.ok) throw new Error('API Error');
    return res.json();
  },
  post: async (path, data) => {
    const res = await fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error('API Error');
    return res.json();
  },
  put: async (path, data) => {
    const res = await fetch(`${API_BASE}${path}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error('API Error');
    return res.json();
  },
  delete: async (path) => {
    const res = await fetch(`${API_BASE}${path}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('API Error');
  }
};

function App() {
  const [activeTab, setActiveTab] = useState('patients');
  const [patients, setPatients] = useState([]);
  const [trials, setTrials] = useState([]);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showPatientForm, setShowPatientForm] = useState(false);
  const [editingPatient, setEditingPatient] = useState(null);

  useEffect(() => {
    if (activeTab === 'patients') loadPatients();
    if (activeTab === 'trials') loadTrials();
  }, [activeTab]);

  const loadPatients = async () => {
    setLoading(true);
    try {
      // Add your GET /api/patients endpoint when available
      setPatients([]);
    } catch (err) {
      console.error('Error loading patients:', err);
    }
    setLoading(false);
  };

  const loadTrials = async () => {
    setLoading(true);
    try {
      const data = await api.get('/trials/?status=Recruiting');
      setTrials(data.trials || []);
    } catch (err) {
      console.error('Error loading trials:', err);
      setTrials([]);
    }
    setLoading(false);
  };

  const matchPatientToTrials = async (patientId) => {
    setLoading(true);
    try {
      const data = await api.post('/trials/match', { patient_id: patientId });
      setMatches(data.matches || []);
      setActiveTab('matches');
    } catch (err) {
      console.error('Error matching trials:', err);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-indigo-900">BC Clinical Trial Matcher</h1>
              <p className="text-sm text-gray-600 mt-1">Personalized breast cancer clinical trial matching</p>
            </div>
            <div className="flex items-center gap-2">
              <Activity className="text-green-500" size={20} />
              <span className="text-sm text-gray-600">System Active</span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-4 mt-6">
        <div className="flex gap-2 bg-white rounded-lg p-2 shadow">
          <TabButton 
            active={activeTab === 'patients'} 
            onClick={() => setActiveTab('patients')}
            icon={<Users size={18} />}
          >
            Patients
          </TabButton>
          <TabButton 
            active={activeTab === 'trials'} 
            onClick={() => setActiveTab('trials')}
            icon={<FileText size={18} />}
          >
            Clinical Trials
          </TabButton>
          <TabButton 
            active={activeTab === 'matches'} 
            onClick={() => setActiveTab('matches')}
            icon={<Search size={18} />}
          >
            Match Results
          </TabButton>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        {activeTab === 'patients' && (
          <PatientsTab 
            patients={patients}
            onAdd={() => { setEditingPatient(null); setShowPatientForm(true); }}
            onEdit={(p) => { setEditingPatient(p); setShowPatientForm(true); }}
            onDelete={async (id) => {
              if (window.confirm('Delete this patient?')) {
                await api.delete(`/patient/${id}`);
                loadPatients();
              }
            }}
            onMatch={matchPatientToTrials}
            loading={loading}
          />
        )}

        {activeTab === 'trials' && (
          <TrialsTab trials={trials} loading={loading} />
        )}

        {activeTab === 'matches' && (
          <MatchesTab matches={matches} loading={loading} />
        )}
      </div>

      {/* Patient Form Modal */}
      {showPatientForm && (
        <PatientFormModal
          patient={editingPatient}
          onClose={() => { setShowPatientForm(false); setEditingPatient(null); }}
          onSave={async (data) => {
            try {
              if (editingPatient) {
                await api.put(`/patient/${editingPatient.id}`, data);
              } else {
                await api.post('/patient/', data);
              }
              setShowPatientForm(false);
              setEditingPatient(null);
              loadPatients();
            } catch (err) {
              alert('Error saving patient: ' + err.message);
            }
          }}
        />
      )}
    </div>
  );
}

function TabButton({ active, onClick, icon, children }) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-all ${
        active 
          ? 'bg-indigo-600 text-white shadow-md' 
          : 'text-gray-600 hover:bg-gray-100'
      }`}
    >
      {icon}
      {children}
    </button>
  );
}

function PatientsTab({ patients, onAdd, onEdit, onDelete, onMatch, loading }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Patient Registry</h2>
        <button
          onClick={onAdd}
          className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
        >
          <Plus size={20} />
          Add Patient
        </button>
      </div>

      {loading ? (
        <div className="text-center py-12 text-gray-500">Loading patients...</div>
      ) : patients.length === 0 ? (
        <div className="text-center py-12">
          <Users size={48} className="mx-auto text-gray-300 mb-3" />
          <p className="text-gray-500">No patients yet. Add your first patient to get started.</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {patients.map(patient => (
            <PatientCard 
              key={patient.id} 
              patient={patient}
              onEdit={() => onEdit(patient)}
              onDelete={() => onDelete(patient.id)}
              onMatch={() => onMatch(patient.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function PatientCard({ patient, onEdit, onDelete, onMatch }) {
  const subtypeColors = {
    'Luminal A': 'bg-blue-100 text-blue-800',
    'Luminal B': 'bg-purple-100 text-purple-800',
    'HER2-enriched': 'bg-pink-100 text-pink-800',
    'Triple-negative': 'bg-red-100 text-red-800'
  };

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className="text-lg font-semibold text-gray-800">Patient #{patient.id}</h3>
            <span className={`px-3 py-1 rounded-full text-xs font-medium ${subtypeColors[patient.subtype] || 'bg-gray-100 text-gray-800'}`}>
              {patient.subtype}
            </span>
          </div>
          
          <div className="grid grid-cols-2 gap-4 text-sm text-gray-600 mb-3">
            <div><span className="font-medium">Age:</span> {patient.age}</div>
            <div><span className="font-medium">Gender:</span> {patient.gender}</div>
            <div><span className="font-medium">Location:</span> {patient.location || 'Not specified'}</div>
          </div>

          <div className="flex gap-4 text-sm">
            <BiomarkerBadge label="ER" value={patient.biomarkers.er_status} />
            <BiomarkerBadge label="PR" value={patient.biomarkers.pr_status} />
            <BiomarkerBadge label="HER2" value={patient.biomarkers.her2_status} />
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={onMatch}
            className="p-2 text-indigo-600 hover:bg-indigo-50 rounded transition-colors"
            title="Find matching trials"
          >
            <Search size={18} />
          </button>
          <button
            onClick={onEdit}
            className="p-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
            title="Edit patient"
          >
            <Edit2 size={18} />
          </button>
          <button
            onClick={onDelete}
            className="p-2 text-red-600 hover:bg-red-50 rounded transition-colors"
            title="Delete patient"
          >
            <Trash2 size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}

function BiomarkerBadge({ label, value }) {
  const getColor = (val) => {
    if (val === 'Positive') return 'bg-green-100 text-green-800';
    if (val === 'Negative') return 'bg-gray-100 text-gray-800';
    return 'bg-yellow-100 text-yellow-800';
  };

  return (
    <div className={`px-2 py-1 rounded ${getColor(value)}`}>
      <span className="font-medium">{label}:</span> {value}
    </div>
  );
}

function TrialsTab({ trials, loading }) {
  const [filters, setFilters] = useState({ subtype: '', phase: '', searchTerm: '' });

  const filteredTrials = trials.filter(trial => {
    if (filters.subtype && trial.target_subtype !== filters.subtype) return false;
    if (filters.phase && trial.phase !== filters.phase) return false;
    if (filters.searchTerm && !trial.title.toLowerCase().includes(filters.searchTerm.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Available Clinical Trials</h2>

      {/* Filters */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <input
          type="text"
          placeholder="Search trials..."
          value={filters.searchTerm}
          onChange={(e) => setFilters({ ...filters, searchTerm: e.target.value })}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        />
        <select
          value={filters.subtype}
          onChange={(e) => setFilters({ ...filters, subtype: e.target.value })}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        >
          <option value="">All Subtypes</option>
          <option value="Luminal A">Luminal A</option>
          <option value="Luminal B">Luminal B</option>
          <option value="HER2-enriched">HER2-enriched</option>
          <option value="Triple-negative">Triple-negative</option>
        </select>
        <select
          value={filters.phase}
          onChange={(e) => setFilters({ ...filters, phase: e.target.value })}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        >
          <option value="">All Phases</option>
          <option value="Phase 1">Phase 1</option>
          <option value="Phase 2">Phase 2</option>
          <option value="Phase 3">Phase 3</option>
          <option value="Phase 4">Phase 4</option>
        </select>
      </div>

      {loading ? (
        <div className="text-center py-12 text-gray-500">Loading trials...</div>
      ) : filteredTrials.length === 0 ? (
        <div className="text-center py-12">
          <FileText size={48} className="mx-auto text-gray-300 mb-3" />
          <p className="text-gray-500">No trials found matching your criteria.</p>
        </div>
      ) : (
        <div className="space-y-4">
          <p className="text-sm text-gray-600 mb-4">{filteredTrials.length} trials found</p>
          {filteredTrials.map(trial => (
            <TrialCard key={trial.nct_id} trial={trial} />
          ))}
        </div>
      )}
    </div>
  );
}

function TrialCard({ trial }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className="text-lg font-semibold text-gray-800">{trial.title}</h3>
            <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">
              {trial.nct_id}
            </span>
          </div>
          
          <div className="flex gap-3 text-sm text-gray-600 mb-2">
            <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded">{trial.phase}</span>
            <span className="px-2 py-1 bg-green-100 text-green-800 rounded">{trial.status}</span>
            <span className="px-2 py-1 bg-indigo-100 text-indigo-800 rounded">{trial.target_subtype}</span>
          </div>

          {expanded && (
            <div className="mt-4 space-y-3">
              <div>
                <h4 className="font-medium text-gray-700 mb-1">Description:</h4>
                <p className="text-sm text-gray-600">{trial.description || 'No description available'}</p>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-700 mb-1">Eligibility:</h4>
                <div className="text-sm text-gray-600">
                  <p>Age: {trial.eligibility.min_age} - {trial.eligibility.max_age} years</p>
                  <p>Gender: {trial.eligibility.gender}</p>
                </div>
              </div>

              {trial.locations && trial.locations.length > 0 && (
                <div>
                  <h4 className="font-medium text-gray-700 mb-1">Locations:</h4>
                  <div className="flex flex-wrap gap-2">
                    {trial.locations.slice(0, 5).map((loc, i) => (
                      <span key={i} className="flex items-center gap-1 text-xs px-2 py-1 bg-gray-100 rounded">
                        <MapPin size={12} />
                        {loc.city}, {loc.state}
                      </span>
                    ))}
                    {trial.locations.length > 5 && (
                      <span className="text-xs text-gray-500">+{trial.locations.length - 5} more</span>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <button
        onClick={() => setExpanded(!expanded)}
        className="text-sm text-indigo-600 hover:text-indigo-800 font-medium mt-2"
      >
        {expanded ? 'Show less' : 'Show more'}
      </button>
    </div>
  );
}

function MatchesTab({ matches, loading }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Trial Match Results</h2>

      {loading ? (
        <div className="text-center py-12 text-gray-500">Finding matching trials...</div>
      ) : matches.length === 0 ? (
        <div className="text-center py-12">
          <Search size={48} className="mx-auto text-gray-300 mb-3" />
          <p className="text-gray-500">No matches yet. Select a patient and click "Find Matching Trials" to begin.</p>
        </div>
      ) : (
        <div className="space-y-4">
          <p className="text-sm text-gray-600 mb-4">{matches.length} matching trials found</p>
          {matches.map((match, i) => (
            <MatchCard key={i} match={match} />
          ))}
        </div>
      )}
    </div>
  );
}

function MatchCard({ match }) {
  const confidenceColor = match.confidence >= 0.8 ? 'text-green-600' : match.confidence >= 0.6 ? 'text-yellow-600' : 'text-gray-600';
  
  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-800">{match.trial?.title || 'Trial'}</h3>
          <p className="text-sm text-gray-600">{match.trial?.nct_id}</p>
        </div>
        <div className="text-right">
          <div className={`text-2xl font-bold ${confidenceColor}`}>
            {Math.round(match.confidence * 100)}%
          </div>
          <div className="text-xs text-gray-500">Match Score</div>
        </div>
      </div>

      {match.reasons && match.reasons.length > 0 && (
        <div>
          <h4 className="font-medium text-gray-700 mb-2 text-sm">Match Reasons:</h4>
          <ul className="space-y-1">
            {match.reasons.map((reason, i) => (
              <li key={i} className="text-sm text-gray-600 flex items-start gap-2">
                <span className="text-green-500 mt-1">✓</span>
                {reason}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function PatientFormModal({ patient, onClose, onSave }) {
  const [formData, setFormData] = useState({
    age: patient?.age || '',
    location: patient?.location || '',
    gender: patient?.gender || 'Female',
    biomarkers: {
      er_status: patient?.biomarkers?.er_status || 'Positive',
      pr_status: patient?.biomarkers?.pr_status || 'Positive',
      her2_status: patient?.biomarkers?.her2_status || 'Negative'
    }
  });

  const handleSubmit = () => {
    if (!formData.age) {
      alert('Please enter age');
      return;
    }
    onSave(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">
          {patient ? 'Edit Patient' : 'Add New Patient'}
        </h3>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Age *</label>
            <input
              type="number"
              value={formData.age}
              onChange={(e) => setFormData({ ...formData, age: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
            <input
              type="text"
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              placeholder="City, State"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Gender</label>
            <select
              value={formData.gender}
              onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            >
              <option value="Female">Female</option>
              <option value="Male">Male</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div className="border-t pt-4">
            <h4 className="font-medium text-gray-700 mb-3">Biomarkers</h4>
            
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">ER Status</label>
                <select
                  value={formData.biomarkers.er_status}
                  onChange={(e) => setFormData({ 
                    ...formData, 
                    biomarkers: { ...formData.biomarkers, er_status: e.target.value }
                  })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                >
                  <option value="Positive">Positive</option>
                  <option value="Negative">Negative</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">PR Status</label>
                <select
                  value={formData.biomarkers.pr_status}
                  onChange={(e) => setFormData({ 
                    ...formData, 
                    biomarkers: { ...formData.biomarkers, pr_status: e.target.value }
                  })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                >
                  <option value="Positive">Positive</option>
                  <option value="Negative">Negative</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">HER2 Status</label>
                <select
                  value={formData.biomarkers.her2_status}
                  onChange={(e) => setFormData({ 
                    ...formData, 
                    biomarkers: { ...formData.biomarkers, her2_status: e.target.value }
                  })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                >
                  <option value="Positive">Positive</option>
                  <option value="Negative">Negative</option>
                  <option value="Equivocal">Equivocal</option>
                </select>
              </div>
            </div>
          </div>

          <div className="flex gap-3 pt-4">
            <button
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleSubmit}
              className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Save Patient
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;