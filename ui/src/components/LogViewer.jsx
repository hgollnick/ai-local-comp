import React, { useEffect, useRef } from 'react';
import { Box, Typography, Paper } from '@mui/material';

function LogViewer() {
  const logRef = useRef();

  useEffect(() => {
    const eventSource = new EventSource('/logs/stream');
    console.log('[LogViewer] EventSource created for /logs/stream');
    eventSource.onopen = () => {
      console.log('[LogViewer] EventSource connection opened');
    };
    eventSource.onmessage = (e) => {
      console.log('[LogViewer] Received log data:', e.data);
      if (logRef.current) {
        logRef.current.textContent += e.data;
        logRef.current.scrollTop = logRef.current.scrollHeight;
      }
    };
    eventSource.onerror = (err) => {
      console.error('[LogViewer] EventSource error:', err);
    };
    return () => {
      console.log('[LogViewer] Closing EventSource');
      eventSource.close();
    };
  }, []);

  return (
    <Box mt={4}>
      <Typography variant="h6">Backend Logs</Typography>
      <Paper variant="outlined" sx={{ height: 200, overflow: 'auto', p: 1, background: '#111', color: '#0f0', fontFamily: 'monospace', fontSize: 13 }}>
        <pre ref={logRef} style={{ margin: 0 }}></pre>
      </Paper>
    </Box>
  );
}

export default LogViewer;
