import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, TextField, Button, Stack, Alert, Snackbar, InputAdornment, IconButton, Paper, Divider } from '@mui/material';
import Slider from '@mui/material/Slider';
import {app, authErrorCodes} from '../firebase/config'
import { getAuth } from "firebase/auth";
import { getDatabase, ref, onValue, get, child, update} from "firebase/database";
import CheckIcon from '@mui/icons-material/Check';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import VisibilityIcon from '@mui/icons-material/Visibility'; 
import CircularProgress from '@mui/material/CircularProgress';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff'; 
import '../assets/CustomFonts.css'

function ReplenishCandy() {
  const navigate = useNavigate();
  const auth = getAuth(app);
  const dbRef = ref(getDatabase(app));

  const maxVolume = 100;

  const [addCandy1Volume, setaddCandy1Volume] = useState(null);
  const [addCandy2Volume, setaddCandy2Volume] = useState(null);
  const [candy1Volume, setCandy1Volume] = useState(0);
  const [candy2Volume, setCandy2Volume] = useState(0);
  const [candy1Name, setCandy1Name] = useState(null);
  const [candy2Name, setCandy2Name] = useState(null);
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
      
    get(child(dbRef, uid + '/candyInformation')).then( (snapshot) => {
      if(snapshot.exists()){
        console.log(snapshot.val());
        setCandy1Volume(snapshot.val().Candy1.Volume);
        setCandy2Volume(snapshot.val().Candy2.Volume);
        setCandy1Name(snapshot.val().Candy1.Name);
        setCandy2Name(snapshot.val().Candy2.Name);
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
    })
  }, []);

  const saveReplenishCandy = () => {
    if(auth.currentUser === null){
      setUpdateSuccessful(false);
      setOpen(true);
      setSnackbarMessage('Error: login timeout. Redirecting to login page!');
      setLoginTimeout(true);
      return;
    }
    
    const uid = auth.currentUser.uid;
  
    const updates = {};
    updates['/' + uid + '/candyInformation/Candy1/Volume'] = candy1Volume + addCandy1Volume;
    updates['/' + uid + '/candyInformation/Candy2/Volume'] = candy2Volume + addCandy2Volume;

    setCandy1Volume(candy1Volume + addCandy1Volume);
    setCandy2Volume(candy2Volume + addCandy2Volume);

    update(dbRef, updates).then( (update) => {
      setUpdateSuccessful(true);
      setOpen(true);
      setSnackbarMessage('Update successful!');
    }).catch((error) => {
      setUpdateSuccessful(false);
      setOpen(true);
      setSnackbarMessage(error.code);
    })
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
            spacing={1}
            direction="column"
            justifyContent="center"
            alignItems="center"
            height="100vh" 
            display="flex" 
            flexDirection="column" 
        >
          <Typography variant="h4" style={{fontFamily: 'AbrilFatface', marginBottom: '2%'}}>Replenish Candy 📦</Typography>
          <Paper
            elevation={3} 
            style={{ 
              padding: '1rem', 
              width: '85%', 
              borderRadius: '5%',
              overflow: 'hidden',
              paddingBottom: '3%'
            }}
          >
            <Typography variant="h5" style={{fontFamily: 'PlaypenSans'}}><u>Candy #1:</u> {candy1Name} 👇</Typography>
            <Divider style={{marginTop: '3%', marginBottom: '3%'}}/>
            <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>
              Current volume: {candy1Volume ? candy1Volume : 0} ml
            </Typography>
            <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>➕</Typography>
            <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>Volume to add (mL)</Typography>
            <Slider 
              defaultValue={0} 
              aria-label="Default" 
              valueLabelDisplay="auto"
              value={addCandy1Volume}
              onChange={(e) => setaddCandy1Volume(e.target.value)}
              min={0} 
              max={maxVolume - candy1Volume}
            />
            <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>🟰</Typography>
            <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>
              New Volume: {addCandy1Volume ? parseFloat(candy1Volume) + parseFloat(addCandy1Volume) : parseFloat(candy1Volume)} ml
            </Typography>
          </Paper>
          <Paper
            elevation={3} 
            style={{ 
              padding: '1rem', 
              width: '85%', 
              borderRadius: '5%',
              overflow: 'hidden',
              paddingBottom: '3%'
            }}
          >
            <Typography variant="h5" style={{fontFamily: 'PlaypenSans'}}><u>Candy #2:</u> {candy2Name} 👇</Typography>
            <Divider style={{marginTop: '3%', marginBottom: '3%'}}/>
            <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>
              Current volume: {candy2Volume ? candy2Volume : 0} ml
            </Typography>
            <Typography variant="h5" style={{fontFamily: 'PlaypenSans'}}>➕</Typography>
            <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>Volume to add (mL)</Typography>
            <Slider 
              defaultValue={0} 
              aria-label="Default" 
              valueLabelDisplay="auto"
              value={addCandy2Volume}
              onChange={(e) => setaddCandy2Volume(e.target.value)}
              min={0} 
              max={maxVolume - candy2Volume}
            />
            <Typography variant="h5" style={{fontFamily: 'PlaypenSans'}}>🟰</Typography>
            <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>
              New Volume: {addCandy2Volume ? parseFloat(candy2Volume) + parseFloat(addCandy2Volume) : parseFloat(candy2Volume)} ml
            </Typography>
          </Paper>
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
