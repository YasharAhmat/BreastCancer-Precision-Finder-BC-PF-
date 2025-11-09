import React from 'react';

const TrialList = ({ trials }) => {
    return (
        <div>
            <h2>Clinical Trials</h2>
            <ul>
                {trials.map((trial) => (
                    <li key={trial.id}>
                        <h3>{trial.title}</h3>
                        <p>{trial.description}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TrialList;