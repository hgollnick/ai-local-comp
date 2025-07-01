import React, { useState } from 'react';
import { Box, Button, LinearProgress, TextField, Typography, Alert } from '@mui/material';

function PullModel({ models, onPulled }) {
  const [modelName, setModelName] = useState('');
  const [progress, setProgress] = useState(0);
  const [pulling, setPulling] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handlePull = async () => {
    if (!modelName) return;
    setPulling(true);
    setProgress(0);
    setMessage('');
    setError('');
    try {
      const res = await fetch(`/pull_model/${encodeURIComponent(modelName)}`, { method: 'POST' });
      if (!res.ok) {
        let errorText = await res.text();
        try {
          const json = JSON.parse(errorText);
          errorText = json.detail || errorText;
        } catch {}
        setError(errorText);
        setPulling(false);
        return;
      }
      if (!res.body) throw new Error('No response body');
      const reader = res.body.getReader();
      let received = 0;
      let total = 1; // Unknown size, so just show indeterminate
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        received += value.length;
        setProgress((prev) => prev < 99 ? prev + 1 : 99); // Fake progress
      }
      setProgress(100);
      setMessage('Model pulled successfully!');
      if (onPulled) onPulled();
    } catch (err) {
      setError('Error pulling model.');
    }
    setPulling(false);
  };

  return (
    <Box mt={2} mb={2}>
      <Typography variant="subtitle1">Pull Model from Ollama</Typography>
      <TextField
        label="Model name (e.g. llama3:8b, codellama:instruct)"
        value={modelName}
        onChange={e => setModelName(e.target.value)}
        fullWidth
        disabled={pulling}
        margin="normal"
      />
      <Button variant="contained" onClick={handlePull} disabled={!modelName || pulling} sx={{ mt: 1 }}>
        Pull Model
      </Button>
      {pulling && <LinearProgress variant="indeterminate" sx={{ mt: 2 }} />}
      {progress === 100 && <Typography color="success.main">Done!</Typography>}
      {message && <Typography color="success.main">{message}</Typography>}
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
    </Box>
  );
}

export default PullModel;
