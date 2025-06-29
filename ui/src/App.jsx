import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, CircularProgress } from '@mui/material';
import ModelSelector from './ModelSelector';
import OllamaUrlInput from './OllamaUrlInput';
import SaveButton from './SaveButton';
import MessageAlert from './MessageAlert';

function App() {
  const [config, setConfig] = useState(null);
  const [models, setModels] = useState([]);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('/config').then(res => res.json()).then(setConfig);
    fetch('/models').then(res => res.json()).then(data => setModels(data.models || []));
  }, []);

  const handleChange = e => {
    setConfig({ ...config, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setSaving(true);
    setMessage('');
    const res = await fetch('/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config),
    });
    setMessage(res.ok ? 'Config saved!' : 'Error saving config.');
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
        <OllamaUrlInput value={config.ollama_url} handleChange={handleChange} />
        <SaveButton saving={saving} />
      </Box>
      <MessageAlert message={message} />
    </Container>
  );
}

export default App;
