import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, TextField, Button, Stack, Alert, Snackbar, InputAdornment, IconButton } from '@mui/material';
import {app, authErrorCodes} from '../firebase/config'
import { getAuth, updatePassword } from "firebase/auth";
import CheckIcon from '@mui/icons-material/Check';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import VisibilityIcon from '@mui/icons-material/Visibility'; 
import CircularProgress from '@mui/material/CircularProgress';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff'; 
import '../assets/CustomFonts.css'

function ReplenishCandy() {
  const navigate = useNavigate();
  const [candy1Volume, setCandy1Volume] = useState(null);
  const [candy2Volume, setCandy2Volume] = useState(null);
  const [open, setOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [loginTimeout, setLoginTimeout] = useState(false);
  const [updateSuccessful, setUpdateSuccessful] = useState(true);

  useEffect(() => {
    if (loginTimeout) {
      const timeout = setTimeout(() => {
        navigate('/'); 
      }, 5000); 

      return () => clearTimeout(timeout); 
    }
  }, [loginTimeout, navigate]);

  const saveReplenishCandy = () => {
    
  };

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setOpen(false);
  };

  return (
    <Container maxWidth="xs" style={{padding: '20px'}}>
        <Stack
            spacing={2}
            direction="column"
            justifyContent="center"
            alignItems="center"
            height="100vh" 
            display="flex" 
            flexDirection="column" 
        >
          <Typography variant="h4" style={{fontFamily: 'AbrilFatface'}}>Replenish Candy 📦</Typography>
          <TextField
            label="Candy 1 volume (mL)"
            variant="standard"
            fullWidth
            type='number'
            sx={{fontFamily: 'PlaypenSans'}} 
            value={candy1Volume}
            onChange={(e) => setCandy1Volume(e.target.value)}
            margin="normal"
          />
          <TextField
            label="Candy 2 volume (mL)"
            variant="standard"
            fullWidth
            type='number'
            sx={{fontFamily: 'PlaypenSans'}} 
            value={candy2Volume}
            onChange={(e) => setCandy2Volume(e.target.value)}
            margin="normal"
          />
            <Button 
              variant="contained" 
              fullWidth
              sx={{fontFamily: 'PlaypenSans'}}  
              onClick={saveReplenishCandy} 
              endIcon={<CheckIcon />}
            >
                Replenish Candy
            </Button>
            <Button 
              variant="contained"
              fullWidth 
              onClick={() => navigate('/main') }
              sx={{fontFamily: 'PlaypenSans'}}  
              endIcon={<ArrowBackIcon />}
            >
                Back
            </Button>
            {loginTimeout && <CircularProgress />}
        </Stack>
        <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
        <Alert onClose={handleClose} severity={updateSuccessful ? 'success' : "error"} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default ReplenishCandy;
