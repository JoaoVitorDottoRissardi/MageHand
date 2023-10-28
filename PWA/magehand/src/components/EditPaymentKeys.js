import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, TextField, Button, Box, Stack, Snackbar, Alert } from '@mui/material';
import {app, authErrorCodes} from '../firebase/config'
import { getAuth } from "firebase/auth";
import { getDatabase, ref, onValue, get, child, update} from "firebase/database";
import CheckIcon from '@mui/icons-material/Check';
import CircularProgress from '@mui/material/CircularProgress';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import '../assets/CustomFonts.css'

function EditPaymentKeys() {

  const navigate = useNavigate();
  const auth = getAuth(app);
  const dbRef = ref(getDatabase(app));

  const [paymentKey, setPaymentKey] = useState('');
  const [paymentToken, setPaymentToken] = useState('');
  const [showInstructions, setShowInstructions] = useState(false);

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

  useEffect(() => {
    if(auth.currentUser === null){
      setUpdateSuccessful(false);
      setOpen(true);
      setSnackbarMessage('Error: login timeout. Redirecting to login page!');
      setLoginTimeout(true);
      return;
    }
    
    const uid = auth.currentUser.uid;
      
    get(child(dbRef, uid + '/PaymentKeys')).then( (snapshot) => {
      if(snapshot.exists()){
        console.log(snapshot.val());
        setPaymentKey(snapshot.val().publicKey);
        setPaymentToken(snapshot.val().accessToken);
      }
      else {
        console.log("No data available");
      }
    }).catch((error) => {
      console.error(error);
    })
  }, []);

  const toggleInstructions = () => {
    setShowInstructions(!showInstructions);
  };

  const savePaymentKeys = () => {

    if(auth.currentUser === null){
      setUpdateSuccessful(false);
      setOpen(true);
      setSnackbarMessage('Error: login timeout. Redirecting to login page!');
      setLoginTimeout(true);
      return;
    }
    
    const uid = auth.currentUser.uid;
    
    const newKeys = {
      accessToken: paymentToken,
      publicKey: paymentKey,
    };

    const updates = {};
    updates['/' + uid + '/PaymentKeys'] = newKeys;

    update(dbRef, updates).then( (update) => {
      console.log(update);
      setUpdateSuccessful(true);
      setOpen(true);
      setSnackbarMessage('Update successful!');
    }).catch((error) => {
      console.error(error);
      setUpdateSuccessful(false);
      setOpen(true);
      setSnackbarMessage(error);
    })
  };

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setOpen(false);
  };

  return (
    <Container maxWidth='xs' style={{padding: '20px'}}>
        <Stack
            spacing={2}
            direction="column"
            justifyContent="center"
            alignItems="center"
            height="100vh" 
            display="flex" 
            flexDirection="column" 
        >
            <Typography variant="h4" style={{fontFamily: 'AbrilFatface'}}>Edit Payment Keys 🗝️</Typography>
            <TextField
                label="Payment Key"
                variant="standard"
                fullWidth
                sx={{fontFamily: 'PlaypenSans'}} 
                value={paymentKey}
                onChange={e => setPaymentKey(e.target.value)}
                margin="normal"
            />
            <TextField
                label="Payment Token"
                variant="standard"
                fullWidth
                sx={{ fontFamily: 'PlaypenSans'}} 
                value={paymentToken}
                onChange={e => setPaymentToken(e.target.value)}
                margin="normal"
            />
            <Button 
              variant="contained"
              fullWidth 
              onClick={savePaymentKeys}
              sx={{fontFamily: 'PlaypenSans'}}  
              endIcon={<CheckIcon />}
            >
                Save
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
            <Button 
              variant="outlined"  
              fullWidth
              sx={{fontFamily: 'PlaypenSans'}}  
              onClick={toggleInstructions}
            >
                {showInstructions ? 'Hide' : 'How do I get these keys?'}
            </Button>
            {showInstructions && (
                <Box mt={2}>
                Instruction text
                </Box>
            )}
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

export default EditPaymentKeys;
