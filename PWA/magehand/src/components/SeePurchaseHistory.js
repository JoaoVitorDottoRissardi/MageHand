import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, Paper, Stack, Button, Alert, Snackbar } from '@mui/material';
import {app} from '../firebase/config'
import { getAuth } from "firebase/auth";
import { getDatabase, ref, get, child} from "firebase/database";
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableRow from '@mui/material/TableRow';
import SubdirectoryArrowRightIcon from '@mui/icons-material/SubdirectoryArrowRight';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CircularProgress from '@mui/material/CircularProgress';
import '../assets/CustomFonts.css';
import '../utils/scrollable.css';
import dayjs from 'dayjs';

function SeePurchaseHistory() {

  const navigate = useNavigate();
  const auth = getAuth(app);
  const dbRef = ref(getDatabase(app));

  const [noOrders, setNoOrders] = useState(false);
  const [open, setOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [loginTimeout, setLoginTimeout] = useState(false);
  const [updateSuccessful, setUpdateSuccessful] = useState(true);

  const [purchaseHistory, setPurchaseHistory] = useState({});

  const currentDate = dayjs();
  const [date, setDate] = useState(currentDate);

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
      
    get(child(dbRef, uid + '/OrderHistory/' + date.format('YYYY-MM-DD'))).then( (snapshot) => {
      if(snapshot.exists()){
        console.log(snapshot.val());
        setPurchaseHistory(snapshot.val());  
        setNoOrders(false);
        // setCandy1Volume(snapshot.val().Candy1.Volume);
        // setCandy2Volume(snapshot.val().Candy2.Volume);
        // setCandy1Name(snapshot.val().Candy1.Name);
        // setCandy2Name(snapshot.val().Candy2.Name);
      }
      else {
        setNoOrders(true);
        setPurchaseHistory({});
      }
    }).catch((error) => {
      setUpdateSuccessful(false);
      setOpen(true);
      setSnackbarMessage(error.code);
    })
  }, [date, auth.currentUser, dbRef]);

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
        <Typography variant="h4" style={{fontFamily: 'AbrilFatface'}}>Order History 📜</Typography>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DemoContainer components={['DatePicker']}>
            <DatePicker 
              label="Filter the orders per date" 
              sx={{width: '350px'}}
              onChange={(newValue) => setDate(newValue)}
              value={date}
            />
          </DemoContainer>
        </LocalizationProvider>
        {noOrders && <Typography variant="h5" style={{fontFamily: 'PlaypenSans', color: 'grey'}}>No Orders found for this date!</Typography>}
        <div className="scrollable-container" style={{maxHeight: 'calc(100vh - 300px)', overflowY: 'auto', paddingLeft: '5%', minWidth: '350px'}}>
        {Object.keys(purchaseHistory).map((key, index) => (
          <Paper 
            key={index} 
            elevation={3} 
            style={{ 
              padding: '1rem', 
              margin: '1rem 0', 
              width: '85%', 
              borderRadius: '5%',
              overflow: 'hidden',
            }}
          >
            <Stack
              spacing={1.5}
              direction="column"
            >
              <Stack
                spacing={2}
                direction="row"
                justifyContent="space-between"
              >
                <Typography variant="h5" sx={{fontFamily: 'PlaypenSans'}}><u>Order #{purchaseHistory[key].Index}</u> 🍭</Typography>
                <Typography variant="h7" sx={{fontFamily: 'PlaypenSans'}}>{key}</Typography>
              </Stack>
              <Table size='small' aria-label="a dense table">
                <TableBody>
                  <TableRow>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>{purchaseHistory[key].Candy1Name}: </Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>{purchaseHistory[key].Quantity1} ml</Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>👉</Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>R$ {purchaseHistory[key].Price1.toFixed(2)}</Typography></TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>{purchaseHistory[key].Candy2Name}: </Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>{purchaseHistory[key].Quantity2} ml</Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>👉</Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>R$ {purchaseHistory[key].Price2.toFixed(2)}</Typography></TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>Total: </Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>{purchaseHistory[key].Quantity2 + purchaseHistory[key].Quantity1} ml</Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>👉</Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>R$ {(purchaseHistory[key].Price2 + purchaseHistory[key].Price1).toFixed(2)}</Typography></TableCell>
                  </TableRow>
                </TableBody>
              </Table>
              <Stack
                spacing={2}
                direction="row"
              >
                <Typography sx={{fontFamily: 'PlaypenSans'}} >Order Status: </Typography>
                <Typography sx={{fontFamily: 'PlaypenSans'}}  style={{color: purchaseHistory[key].Status === 'Rejected' ? 'red' : 'green'}}>
                  {purchaseHistory[key].Status}{purchaseHistory[key].Status === 'Rejected' ? ' ⛔' : ' ✅'}
                </Typography>
              </Stack>
              { purchaseHistory[key].Status === 'Rejected' &&
                <Stack
                  spacing={0.5}
                  direction="row"
                >
                  <SubdirectoryArrowRightIcon />
                  <Typography sx={{fontFamily: 'PlaypenSans'}}>Rejection reason: {purchaseHistory[key].RejectionReason}</Typography> 
                </Stack>
              }
            </Stack> 
          </Paper>
        ))}
        </div>
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

export default SeePurchaseHistory;
