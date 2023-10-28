import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, Paper, Stack, Button } from '@mui/material';
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
import '../assets/CustomFonts.css';
import '../utils/scrollable.css';
import dayjs from 'dayjs';

function SeePurchaseHistory() {

  const navigate = useNavigate();

  const [purchaseHistory, setPurchaseHistory] = useState([
    {
      id: 1,
      timestamp: 'timestamp',
      name1: 'name1',
      name2: 'name2',
      quantity1: 100,
      quantity2: 30,
      price1: 1.99,
      price2: 2.01,
      status: 'rejected',
      rejectionReason: 'customer left'
    },
    {
      id: 2,
      timestamp: 'timestamp',
      name1: 'name1',
      name2: 'name2',
      quantity1: 100,
      quantity2: 30,
      price1: 1.99,
      price2: 2.01,
      status: 'accepted',
      rejectionReason: 'reason'
    },
    {
      id: 3,
      timestamp: 'timestamp',
      name1: 'name1',
      name2: 'name2',
      quantity1: 100,
      quantity2: 30,
      price1: 1.99,
      price2: 2.01,
      status: 'accepted',
      rejectionReason: 'reason'
    },
    {
      id: 4,
      timestamp: 'timestamp',
      name1: 'name1',
      name2: 'name2',
      quantity1: 100,
      quantity2: 30,
      price1: 1.99,
      price2: 2.01,
      status: 'rejected',
      rejectionReason: 'customer left'
    },
  ]);

  const currentDate = dayjs();
  const [date, setDate] = useState(currentDate);

  useEffect(() => {
    // const user = firebase.auth().currentUser;

    // if (user) {
    //   const userId = user.uid;
    //   // Replace 'your/database/path' with the actual path to your purchase history data
    //   const dbRef = firebase.database().ref(`users/${userId}/purchaseHistory`);

    //   dbRef.on('value', snapshot => {
    //     const data = snapshot.val();
    //     if (data) {
    //       // Convert the data into an array for sorting
    //       const purchaseArray = Object.values(data);

    //       // Sort the purchases by timestamp (most recent first)
    //       purchaseArray.sort((a, b) => b.timestamp - a.timestamp);

    //       setPurchaseHistory(purchaseArray);
    //     }
    //   });
    // }
  }, []);

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
        <div className="scrollable-container" style={{maxHeight: 'calc(100vh - 300px)', overflowY: 'auto', paddingLeft: '5%', minWidth: '350px'}}>
        {purchaseHistory.map((purchase, index) => (
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
                <Typography variant="h5" sx={{fontFamily: 'PlaypenSans'}}><u>Order #{purchase.id}</u> 🍭</Typography>
                <Typography variant="h7" sx={{fontFamily: 'PlaypenSans'}}>{new Date(purchase.timestamp).toLocaleString()}</Typography>
              </Stack>
              <Table size='small' aria-label="a dense table">
                <TableBody>
                  <TableRow>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>{purchase.name1}: </Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>{purchase.quantity1} ml</Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>👉</Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>R$ {purchase.price1.toFixed(2)}</Typography></TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>{purchase.name2}: </Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>{purchase.quantity2} ml</Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>👉</Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>R$ {purchase.price2.toFixed(2)}</Typography></TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>Total: </Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>{purchase.quantity2 + purchase.quantity1} ml</Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>👉</Typography></TableCell>
                    <TableCell><Typography sx={{fontFamily: 'PlaypenSans'}}>R$ {(purchase.price2 + purchase.price1).toFixed(2)}</Typography></TableCell>
                  </TableRow>
                </TableBody>
              </Table>
              <Stack
                spacing={2}
                direction="row"
              >
                <Typography sx={{fontFamily: 'PlaypenSans'}} >Order Status: </Typography>
                <Typography sx={{fontFamily: 'PlaypenSans'}}  style={{color: purchase.status === 'rejected' ? 'red' : 'green'}}>
                  {purchase.status}{purchase.status === 'rejected' ? ' ⛔' : ' ✅'}
                </Typography>
              </Stack>
              { purchase.status === 'rejected' &&
                <Stack
                  spacing={0.5}
                  direction="row"
                >
                  <SubdirectoryArrowRightIcon />
                  <Typography sx={{fontFamily: 'PlaypenSans'}}>Rejection reason: {purchase.rejectionReason}</Typography> 
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
      </Stack>
    </Container>
  );
}

export default SeePurchaseHistory;
