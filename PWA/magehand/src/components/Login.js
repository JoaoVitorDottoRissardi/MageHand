import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {app, authErrorCodes} from '../firebase/config'
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
import { Container, Typography, TextField, Button, Stack, Box } from '@mui/material';

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const auth = getAuth(app);

  const handleLogin = () => {
    navigate('/main');
    // console.log('Trying to login');
    // signInWithEmailAndPassword(auth, email, password)
    //   .then((userCredential) => {
    //     navigate('/main');
    //     console.log('User logged');
    //   })
    //   .catch(error => {
    //     console.error('Login error:', error);
    //     // Handle login error (e.g., display an error message)
    //   });
  };

  return (
    <Container maxWidth="xs">
        <Stack spacing={2} direction="column" justifyContent="center" alignItems="center">
            <Box margin={20}>
                <Typography variant="h4">Login Screen</Typography>
            </Box>
            <TextField
                label="Email"
                variant="outlined"
                fullWidth
                value={email}
                onChange={e => setEmail(e.target.value)}
                margin="normal"
            />
            <TextField
                label="Password"
                type="password"
                variant="outlined"
                fullWidth
                value={password}
                onChange={e => setPassword(e.target.value)}
                margin="normal"
            />
            <Button variant="contained" color="primary" fullWidth onClick={handleLogin}>
                Login
            </Button>
        </Stack>
    </Container>
  );
}

export default Login;
