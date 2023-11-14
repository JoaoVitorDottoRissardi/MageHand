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

function ChangePassword() {
  const navigate = useNavigate();
  const [newPassword, setNewPassword] = useState('');
  const [confirmedPassword, setConfirmedPassword] = useState('');
  const [open, setOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmedPassword, setShowConfirmedPassword] = useState(false);
  const [loginTimeout, setLoginTimeout] = useState(false);
  const [updateSuccessful, setUpdateSuccessful] = useState(true);
  const auth = getAuth(app);

  useEffect(() => {
    if (loginTimeout) {
      const timeout = setTimeout(() => {
        navigate('/'); 
      }, 5000); 

      return () => clearTimeout(timeout); 
    }
  }, [loginTimeout, navigate]);

  const saveNewPassword = () => {
    if(newPassword === confirmedPassword){
      updatePassword(auth.currentUser, newPassword)
        .then(() => {
          console.log('Senha atualizada!');
          setSnackbarMessage('Password updated successfully!');
          setOpen(true);
          setUpdateSuccessful(true);
        })
        .catch(error => {
          console.error('Error updating password:', error);
          setSnackbarMessage(authErrorCodes[error.code]);
          setOpen(true);
          setUpdateSuccessful(false);
          if(error.code === 'auth/requires-recent-login'){
            setLoginTimeout(true);
          }
        })
    }
    else{
      setSnackbarMessage('Error: passwords don\'t match!');
      setOpen(true);
      setUpdateSuccessful(false);
    }
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
          <Typography variant="h4" style={{fontFamily: 'AbrilFatface'}}>
            Change Password&nbsp; 
            <img
              src="/assets/windows-11-emojis/locked-with-key_1f510.png"
              alt="🔐"
              style={{ width: '1.4em', height: '1.4em', verticalAlign: 'top' }}
            />
          </Typography>
          <TextField
            label="New Password"
            type={showPassword ? 'text' : 'password'} 
            variant="standard"
            fullWidth
            sx={{fontFamily: 'PlaypenSans'}} 
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            margin="normal"
            InputProps={{
              endAdornment: ( 
                <InputAdornment position="end">
                  <IconButton
                    edge="end"
                    onClick={() => setShowPassword(!showPassword)} 
                  >
                    {showPassword ? <VisibilityIcon /> : <VisibilityOffIcon />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />
          <TextField
            label="Confirm New Password"
            type={showConfirmedPassword ? 'text' : 'password'} 
            variant="standard"
            fullWidth
            sx={{fontFamily: 'PlaypenSans'}} 
            value={confirmedPassword}
            onChange={(e) => setConfirmedPassword(e.target.value)}
            margin="normal"
            InputProps={{
              endAdornment: ( 
                <InputAdornment position="end">
                  <IconButton
                    edge="end"
                    onClick={() => setShowConfirmedPassword(!showConfirmedPassword)} 
                  >
                    {showConfirmedPassword ? <VisibilityIcon /> : <VisibilityOffIcon />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />
            <Button 
              variant="contained" 
              fullWidth
              sx={{fontFamily: 'PlaypenSans'}}  
              onClick={saveNewPassword} 
              endIcon={<CheckIcon />}
            >
                Update password
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

export default ChangePassword;
