import { FormControl, InputLabel, Select, MenuItem, FormControlLabel, Checkbox } from '@mui/material';

function ModelSelector({ config, models, handleChange }) {
  return (
    <>
      <FormControlLabel
        control={
          <Checkbox
            name="use_langchain_router"
            checked={!!config.use_langchain_router}
            onChange={handleChange}
          />
        }
        label="Use LangChain Routing"
      />
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
