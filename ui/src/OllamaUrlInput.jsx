import { TextField } from '@mui/material';

function OllamaUrlInput({ value, handleChange }) {
  return (
    <TextField
      fullWidth
      margin="normal"
      label="Ollama URL"
      name="ollama_url"
      value={value}
      onChange={handleChange}
    />
  );
}

export default OllamaUrlInput;
