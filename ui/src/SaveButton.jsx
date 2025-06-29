import { Button, Box } from '@mui/material';

function SaveButton({ saving }) {
  return (
    <Box mt={2}>
      <Button type="submit" variant="contained" color="primary" disabled={saving} fullWidth>
        {saving ? 'Saving...' : 'Save Config'}
      </Button>
    </Box>
  );
}

export default SaveButton;
