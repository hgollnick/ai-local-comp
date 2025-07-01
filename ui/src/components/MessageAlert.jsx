import { Alert } from '@mui/material';

function MessageAlert({ message }) {
  if (!message) return null;
  return (
    <Alert severity={message.includes('Error') ? 'error' : 'success'} sx={{ mt: 2 }}>
      {message}
    </Alert>
  );
}

export default MessageAlert;
