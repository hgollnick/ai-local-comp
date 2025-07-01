import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';

function ModelSelector({ config, models, handleChange }) {
  return (
    <>
      {['router_model', 'code_model', 'simple_model', 'complex_model'].map(name => (
        <FormControl fullWidth margin="normal" key={name}>
          <InputLabel>{name.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</InputLabel>
          <Select
            name={name}
            value={config[name]}
            label={name}
            onChange={handleChange}
          >
            {models.map(m => (
              <MenuItem key={m} value={m}>{m}</MenuItem>
            ))}
          </Select>
        </FormControl>
      ))}
    </>
  );
}

export default ModelSelector;
