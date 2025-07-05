import React, { useState, useEffect } from 'react';
import { Box, Typography, CircularProgress } from '@mui/material';
import ModelSelector from './components/ModelSelector';
import SaveButton from './components/SaveButton';
import MessageAlert from './components/MessageAlert';
import PullModel from './components/PullModel';
import LogViewer from './components/LogViewer';

function App() {
  const [config, setConfig] = useState(null);
  const [models, setModels] = useState([]);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('/config')
      .then(res => {
        if (!res.ok) throw new Error('Failed to load config');
        return res.json();
      })
      .then(setConfig)
      .catch(err => setMessage('Error loading config'));
    fetch('/models')
      .then(res => {
        if (!res.ok) throw new Error('Failed to load models');
        return res.json();
      })
      .then(data => setModels(data.models || []))
      .catch(err => setMessage('Error loading models'));
  }, []);

  const handleChange = e => {
    const { name, type, checked, value } = e.target;
    setConfig({
      ...config,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setSaving(true);
    setMessage('');
    try {
      const res = await fetch('/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
      });
      setMessage(res.ok ? 'Config saved!' : 'Error saving config.');
    } catch (err) {
      setMessage('Error saving config.');
    }
    setSaving(false);
  };

  const refreshModels = () => {
    fetch('/models')
      .then(res => res.json())
      .then(data => setModels(data.models || []));
  };

  if (!config) return (
    <Box display="flex" justifyContent="center" mt={8}>
      <CircularProgress />
    </Box>
  );

  return (
    <div className="main-horizontal-layout">
      <div className="config-panel">
        <Typography variant="h5" gutterBottom>
          AI Local Config
        </Typography>
        <PullModel models={models} onPulled={refreshModels} />
        <Box component="form" onSubmit={handleSubmit} noValidate autoComplete="off">
          <ModelSelector config={config} models={models} handleChange={handleChange} />
          <SaveButton saving={saving} />
        </Box>
        <MessageAlert message={message} />
      </div>
      <div className="logs-panel">
        <LogViewer />
      </div>
    </div>
  );
}

export default App;
