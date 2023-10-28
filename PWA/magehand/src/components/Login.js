import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {app, authErrorCodes} from '../firebase/config'
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
import { Container, Typography, TextField, Button, Stack, Box, InputAdornment, IconButton, Snackbar, Alert } from '@mui/material';
import LoginIcon from '@mui/icons-material/Login';
import VisibilityIcon from '@mui/icons-material/Visibility'; 
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff'; 
import '../assets/CustomFonts.css'
import validator from 'validator'; 

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [validEmail, setValidEmail] = useState(true);
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [open, setOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const auth = getAuth(app);

  const handleLogin = () => {
    // navigate('/main');
    console.log('Trying to login');
    signInWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        navigate('/main');
        console.log('User logged');
      })
      .catch(error => {
        console.error('Login error:', error);
        setSnackbarMessage(authErrorCodes[error.code]);
        setOpen(true);
      });
  };

  const handleEmailChange = (event) => {
    const { value } = event.target;
    setEmail(value);
    if (validator.isEmail(value) || value === "") { 
      setValidEmail(true);
      return;
    }
    setValidEmail(false);
  }

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  };

  return (
    <Container maxWidth="xs">
         <Stack
            spacing={2}
            direction="column"
            justifyContent="center"
            alignItems="center"
            height="100vh" 
            display="flex" 
            flexDirection="column" 
          >
            <Box margin={20}>
                <Typography variant="h4" style={{fontFamily: 'AbrilFatface'}}>Login 🔓</Typography>
            </Box>
            <TextField
                label="Email"
                variant="standard"
                sx={{width:'300px', fontFamily: 'PlaypenSans'}} 
                value={email}
                error={!validEmail}
                onChange={handleEmailChange}
                helperText={!validEmail ? 'Invalid email address' : ''}
                margin="normal"
            />
          <TextField
            label="Password"
            type={showPassword ? 'text' : 'password'} 
            variant="standard"
            sx={{width:'300px', fontFamily: 'PlaypenSans'}} 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
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
            <Button 
              variant="contained" 
              onClick={handleLogin} 
              endIcon={<LoginIcon />} 
              sx={{width:'300px', fontFamily: 'PlaypenSans'}} 
            >
                Login
            </Button>
        </Stack>
        <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="error" sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default Login;
