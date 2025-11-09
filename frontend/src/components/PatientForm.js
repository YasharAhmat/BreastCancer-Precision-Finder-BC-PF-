import React, { useState } from 'react';

const PatientForm = () => {
    const [patientData, setPatientData] = useState({
        name: '',
        age: '',
        gender: '',
        symptoms: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setPatientData({
            ...patientData,
            [name]: value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Patient Data Submitted:', patientData);
        // Add logic to handle form submission, e.g., API call
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Name:</label>
                <input type="text" name="name" value={patientData.name} onChange={handleChange} required />
            </div>
            <div>
                <label>Age:</label>
                <input type="number" name="age" value={patientData.age} onChange={handleChange} required />
            </div>
            <div>
                <label>Gender:</label>
                <select name="gender" value={patientData.gender} onChange={handleChange} required>
                    <option value="">Select</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                </select>
            </div>
            <div>
                <label>Symptoms:</label>
                <textarea name="symptoms" value={patientData.symptoms} onChange={handleChange} required />
            </div>
            <button type="submit">Submit</button>
        </form>
    );
};

export default PatientForm;