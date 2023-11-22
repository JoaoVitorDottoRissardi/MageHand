import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, Button, Stack, Alert, Snackbar, Paper, Divider } from '@mui/material';
import Slider from '@mui/material/Slider';
import {app} from '../firebase/config'
import { getAuth } from "firebase/auth";
import { getDatabase, ref, get, child, update} from "firebase/database";
import CheckIcon from '@mui/icons-material/Check';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CircularProgress from '@mui/material/CircularProgress';
import ThumbsUpAltIcon from '@mui/icons-material/ThumbUpAlt';
import '../assets/CustomFonts.css'

function ReplenishCandy() {
  const navigate = useNavigate();
  const auth = getAuth(app);
  const dbRef = ref(getDatabase(app));

  const maxVolume = 3000.0;

  const [addCandy1Volume, setaddCandy1Volume] = useState(0);
  const [addCandy2Volume, setaddCandy2Volume] = useState(0);
  const [candy1Volume, setCandy1Volume] = useState(0);
  const [candy2Volume, setCandy2Volume] = useState(0);
  const [candy1Name, setCandy1Name] = useState(null);
  const [candy2Name, setCandy2Name] = useState(null);
  const [replenish1, setReplenish1] = useState(null);
  const [replenish2, setReplenish2] = useState(null);
  const [open, setOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [loginTimeout, setLoginTimeout] = useState(false);
  const [updateSuccessful, setUpdateSuccessful] = useState(true);
  const [loading, setLoading] = useState(true);
  const [warningMessage, setWarningMessage] = useState(null);

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
        setCandy1Volume(snapshot.val().Candy1.Volume + snapshot.val().Candy1.Replenish);
        setCandy2Volume(snapshot.val().Candy2.Volume + snapshot.val().Candy2.Replenish);
        setReplenish1(snapshot.val().Candy1.Replenish);
        setReplenish2(snapshot.val().Candy2.Replenish);
        setCandy1Name(snapshot.val().Candy1.Name);
        setCandy2Name(snapshot.val().Candy2.Name);
        if(snapshot.val().Candy1.Volume + snapshot.val().Candy1.Replenish === 0  || 
          snapshot.val().Candy2.Volume + snapshot.val().Candy2.Replenish === 0){
          setWarningMessage(true);
        }
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
  }, [auth.currentUser, dbRef]);

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
    updates['/' + uid + '/candyInformation/Candy1/Replenish'] = replenish1 + addCandy1Volume;
    updates['/' + uid + '/candyInformation/Candy2/Replenish'] = replenish2 + addCandy2Volume;

    setCandy1Volume(candy1Volume + addCandy1Volume);
    setCandy2Volume(candy2Volume + addCandy2Volume);
    setaddCandy1Volume(0);
    setaddCandy2Volume(0);

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
          <Typography variant="h4" style={{fontFamily: 'AbrilFatface'}}>
            Replenish Candy&nbsp; 
            <img
            src="/assets/windows-11-emojis/package_1f4e6.png"
            alt="📦"
            style={{ width: '1.4em', height: '1.4em', verticalAlign: 'top' }}
            />
          </Typography>
          {!loading && !warningMessage &&<>
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
              <Typography variant="h5" style={{fontFamily: 'PlaypenSans'}}>
                <u>Candy #1:</u> {candy1Name}
                <img
                  src="/assets/windows-11-emojis/backhand-index-pointing-down_1f447.png"
                  alt="👇"
                  style={{ width: '1em', height: '1em', verticalAlign: 'middle' }}
                />
              </Typography>
              <Divider style={{marginTop: '3%', marginBottom: '3%'}}/>
              <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>
                Current volume: {candy1Volume ? candy1Volume : 0} ml
              </Typography>
              <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>
                <img
                  src="/assets/windows-11-emojis/plus_2795.png"
                  alt="➕"
                  style={{ width: '1em', height: '1em', verticalAlign: 'middle' }}
                />
              </Typography>
              <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>Volume to add(mL): {addCandy1Volume} ml</Typography>
              <Slider 
                defaultValue={0} 
                aria-label="Default" 
                valueLabelDisplay="auto"
                value={addCandy1Volume}
                onChange={(e) => setaddCandy1Volume(e.target.value)}
                min={0} 
                max={maxVolume - candy1Volume}
              />
              <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>
                <img
                  src="/assets/windows-11-emojis/heavy-equals-sign_1f7f0.png"
                  alt="🟰"
                  style={{ width: '1em', height: '1em', verticalAlign: 'top' }}
                />
              </Typography>
              <Stack
                spacing={2}
                direction="row"
              >
                <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>
                  New Volume: {addCandy1Volume ? parseFloat(candy1Volume) + parseFloat(addCandy1Volume) : parseFloat(candy1Volume)} ml       
                </Typography>
                <Typography variant="h6" style={{fontFamily: 'PlaypenSans', color: 'red'}}>
                  {parseFloat(candy1Volume) + parseFloat(addCandy1Volume) === maxVolume ? <>  
                  Full!
                  <img
                    src="/assets/windows-11-emojis/warning_26a0-fe0f.png"
                    alt="⚠️"
                    style={{ width: '0.8em', height: '0.8em', verticalAlign: 'middle' }}
                  />
                  </> : ''}
                </Typography>
              </Stack>

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
              <Typography variant="h5" style={{fontFamily: 'PlaypenSans'}}>
                <u>Candy #2:</u> {candy2Name}
                <img
                  src="/assets/windows-11-emojis/backhand-index-pointing-down_1f447.png"
                  alt="👇"
                  style={{ width: '1em', height: '1em', verticalAlign: 'middle' }}
                />
              </Typography>
              <Divider style={{marginTop: '3%', marginBottom: '3%'}}/>
              <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>
                Current volume: {candy2Volume ? candy2Volume : 0} ml
              </Typography>
              <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>
                <img
                  src="/assets/windows-11-emojis/plus_2795.png"
                  alt="➕"
                  style={{ width: '1em', height: '1em', verticalAlign: 'middle' }}
                />
              </Typography>
              <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>Volume to add(mL): {addCandy2Volume} ml</Typography>
              <Slider 
                defaultValue={0} 
                aria-label="Default" 
                valueLabelDisplay="auto"
                value={addCandy2Volume}
                onChange={(e) => setaddCandy2Volume(e.target.value)}
                min={0} 
                max={maxVolume - candy2Volume}
              />
              <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>
                <img
                  src="/assets/windows-11-emojis/heavy-equals-sign_1f7f0.png"
                  alt="🟰"
                  style={{ width: '1em', height: '1em', verticalAlign: 'top' }}
                />
              </Typography>
              <Stack
                spacing={2}
                direction="row"
              >
                <Typography variant="h6" style={{fontFamily: 'PlaypenSans'}}>
                  New Volume: {addCandy2Volume ? parseFloat(candy2Volume) + parseFloat(addCandy2Volume) : parseFloat(candy2Volume)} ml       
                </Typography>
                <Typography variant="h6" style={{fontFamily: 'PlaypenSans', color: 'red'}}>
                  {parseFloat(candy2Volume) + parseFloat(addCandy2Volume) === maxVolume ? 
                  <>  
                  Full!
                  <img
                    src="/assets/windows-11-emojis/warning_26a0-fe0f.png"
                    alt="⚠️"
                    style={{ width: '0.8em', height: '0.8em', verticalAlign: 'middle' }}
                  />
                  </> : ''}
                </Typography>
              </Stack>
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
            </>}
            {loading && <CircularProgress />}
            {!loading && warningMessage && 
                <>
                  <Typography variant="h6" style={{fontFamily: 'PlaypenSans', color: 'red'}}>
                    Warning!
                  </Typography>
                  <Typography variant="h7" style={{fontFamily: 'PlaypenSans'}}>
                    One of your storages is empty!
                  </Typography>
                  <Typography variant="h7" style={{fontFamily: 'PlaypenSans'}}>
                    You need to fill the mechanisms. 
                  </Typography>
                  <Typography variant="h7" style={{fontFamily: 'PlaypenSans'}}>
                    To do so, you just need to make an order.
                  </Typography>
                  <Typography variant="h7" style={{fontFamily: 'PlaypenSans'}}>
                    Make sure to at least pour some candy.
                  </Typography>
                  <Typography variant="h7" style={{fontFamily: 'PlaypenSans'}}>
                    Reject the order at the end.
                  </Typography>
                  <Typography variant="h7" style={{fontFamily: 'PlaypenSans'}}>
                    Put the candy back at the storage.
                  </Typography>
                  <Typography variant="h7" style={{fontFamily: 'PlaypenSans'}}>
                    Then, the volume will be correct!
                  </Typography>
                  <Button 
                    variant="contained"
                    fullWidth 
                    onClick={() => setWarningMessage(false) }
                    sx={{fontFamily: 'PlaypenSans'}}  
                    endIcon={<ThumbsUpAltIcon />}
                  >
                      OK
                  </Button>
                </>
              }
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
