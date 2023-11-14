import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, TextField, Button, Stack, Snackbar, Alert, InputAdornment, IconButton, } from '@mui/material';
import {app} from '../firebase/config'
import { getAuth } from "firebase/auth";
import { getDatabase, ref, get, child, update} from "firebase/database";
import CheckIcon from '@mui/icons-material/Check';
import CircularProgress from '@mui/material/CircularProgress';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import VisibilityIcon from '@mui/icons-material/Visibility'; 
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff'; 
import Link from '@mui/material/Link';
import axios from 'axios';
import '../assets/CustomFonts.css'

function EditPaymentKeys() {

  const navigate = useNavigate();
  const auth = getAuth(app);
  const dbRef = ref(getDatabase(app));

  const [paymentToken, setPaymentToken] = useState('');
  const [showToken, setShowToken] = useState(false);
  const [showInstructions, setShowInstructions] = useState(false);

  const [open, setOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [loginTimeout, setLoginTimeout] = useState(false);
  const [updateSuccessful, setUpdateSuccessful] = useState(true);

  const [loading, setLoading] = useState(true);

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
        setPaymentToken(snapshot.val().accessToken);
      }
      else {
        setUpdateSuccessful(false);
        setOpen(true);
        setSnackbarMessage("No data available");
      }
    }).catch((error) => {
      setUpdateSuccessful(false);
      setOpen(true);
      setSnackbarMessage(error.code);
    }).finally(() => {
      setLoading(false);
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

    const instance = axios.create(
      {baseURL: 'https://api.mercadopago.com', headers: {'Content-Type' : 'application/json', 'Authorization' : `Bearer ${paymentToken}`}}
    )
    
    instance.get('v1/payments/search?sort=date_created&criteria=desc&external_reference=ID_REF').then(response => {
      const newKeys = {
        accessToken: paymentToken,
      };
  
      const updates = {};
      updates['/' + uid + '/PaymentKeys'] = newKeys;
  
      update(dbRef, updates).then( (update) => {
        setUpdateSuccessful(true);
        setOpen(true);
        setSnackbarMessage('Update successful!');
      }).catch((error) => {
        setUpdateSuccessful(false);
        setOpen(true);
        setSnackbarMessage(error.code);
      })
    }).catch((error) => {
      setUpdateSuccessful(false);
      setOpen(true);
      setSnackbarMessage('Error: invalid access token!');
    });
    
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
          <Typography variant="h4" style={{fontFamily: 'AbrilFatface'}}>
            Edit Payment Key&nbsp; 
            <img
              src="/assets/windows-11-emojis/old-key_1f5dd-fe0f.png"
              alt="🗝️"
              style={{ width: '1.4em', height: '1.4em', verticalAlign: 'top' }}
            />
          </Typography>
          {!loading && <>
            <TextField
            label="Access Token"
            type={showToken ? 'text' : 'password'} 
            variant="standard"
            fullWidth
            sx={{fontFamily: 'PlaypenSans'}} 
            value={paymentToken}
            onChange={e => setPaymentToken(e.target.value)}
            margin="normal"
            InputProps={{
              endAdornment: ( 
                <InputAdornment position="end">
                  <IconButton
                    edge="end"
                    onClick={() => setShowToken(!showToken)} 
                  >
                    {showToken ? <VisibilityIcon /> : <VisibilityOffIcon />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
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
                {showInstructions ? 'Hide' : 'How do I get this key?'}
            </Button>
            {showInstructions && (
                <Stack mt={2} spacing={1} >
                  <Typography variant="h5" sx={{fontFamily: 'PlaypenSans'}}>
                    Don't have the Mercado Pago token yet?&nbsp;
                    <img
                      src="/assets/windows-11-emojis/backhand-index-pointing-down_1f447.png"
                      alt="👇"
                      style={{ width: '1.4em', height: '1.4em', verticalAlign: 'top' }}
                    />
                  </Typography>
                  <Typography variant="h7" sx={{fontFamily: 'PlaypenSans'}}>
                    1: Enter the&nbsp;
                    <Link href="https://mercadopago.com.br/developers/panel/app">
                      Mercado Pago developers panel
                    </Link>
                  </Typography>
                  <Typography variant="h7" sx={{fontFamily: 'PlaypenSans'}}>
                    2: Hit the blue button to create your application.
                  </Typography>
                  <Typography variant="h7" sx={{fontFamily: 'PlaypenSans'}}>
                    3: When creating the application, select <b>"No"</b> for using an e-commerce 
                    and <b>"CheckoutTransparente"</b> for which product you are integrating.
                  </Typography>
                  <Typography variant="h7" sx={{fontFamily: 'PlaypenSans'}}>
                    4: Select your newly created application.
                  </Typography>
                  <Typography variant="h9" sx={{fontFamily: 'PlaypenSans'}}>
                    5: On the left side bar, click on <u>"Credenciais de Produção"</u>.
                  </Typography>
                  <Typography variant="h9" sx={{fontFamily: 'PlaypenSans'}}>
                    6: Copy your access token and insert it above.
                  </Typography>
                </Stack>
            )}
            {loginTimeout && <CircularProgress />}
          </>}
          {loading &&  <CircularProgress />}
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
