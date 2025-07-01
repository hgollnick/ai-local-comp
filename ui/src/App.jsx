import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, CircularProgress } from '@mui/material';
import ModelSelector from './components/ModelSelector';
import SaveButton from './components/SaveButton';
import MessageAlert from './components/MessageAlert';

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
    setConfig({ ...config, [e.target.name]: e.target.value });
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

  if (!config) return (
    <Box display="flex" justifyContent="center" mt={8}>
      <CircularProgress />
    </Box>
  );

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Typography variant="h5" gutterBottom>
        AI Local Config
      </Typography>
      <Box component="form" onSubmit={handleSubmit} noValidate autoComplete="off">
        <ModelSelector config={config} models={models} handleChange={handleChange} />
        <SaveButton saving={saving} />
      </Box>
      <MessageAlert message={message} />
    </Container>
  );
}

export default App;
