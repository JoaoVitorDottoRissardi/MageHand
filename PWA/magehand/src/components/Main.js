import React from 'react';
import { NavLink } from 'react-router-dom';
import { Container, Typography, Button, Stack } from '@mui/material';
import ReceiptLongIcon from '@mui/icons-material/ReceiptLong';
import KeyIcon from '@mui/icons-material/Key';
import BuildIcon from '@mui/icons-material/Build';
import LockIcon from '@mui/icons-material/Lock';
import ArchiveIcon from '@mui/icons-material/Archive';
import { ThemeProvider } from '@mui/material/styles';
import '../assets/CustomFonts.css'
import {theme} from '../utils/themes'

function Main() {
  return (
    <ThemeProvider theme={theme}>
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
                <Typography variant="h4" style={{fontFamily: 'AbrilFatface'}}>
                    Mage Hand&nbsp; 
                    <img
                    src="/assets/windows-11-emojis/waving-hand_1f44b.png"
                    alt="👋"
                    style={{ width: '1.4em', height: '1.4em', verticalAlign: 'top' }}
                    />
                </Typography>
                <Button 
                    variant="contained"  
                    component={NavLink} 
                    to="/editcandy" 
                    endIcon={<BuildIcon />} 
                    sx={{width:'250px', fontFamily: 'PlaypenSans'}} 
                    color="violet"
                >
                    Edit Candies
                </Button>
                <Button 
                    variant="contained"  
                    component={NavLink} 
                    to="/editpaymentkeys" 
                    endIcon={<KeyIcon />} 
                    sx={{width:'250px', fontFamily: 'PlaypenSans'}} 
                    color="red"
                >
                    Edit Payment Key
                </Button>
                <Button 
                    variant="contained"  
                    component={NavLink} 
                    to="/purchasehistory" 
                    endIcon={<ReceiptLongIcon />} 
                    sx={{width:'250px', fontFamily: 'PlaypenSans'}} 
                    color="green"
                >
                    Order History
                </Button>
                <Button 
                    variant="contained"  
                    component={NavLink} 
                    to="/changepassword" 
                    endIcon={<LockIcon />} 
                    sx={{width:'250px', fontFamily: 'PlaypenSans'}} 
                    color="yellow"
                >
                    Change Password     
                </Button>
                <Button 
                    variant="contained"  
                    component={NavLink} 
                    to="/replenishcandy" 
                    endIcon={<ArchiveIcon />} 
                    sx={{width:'250px', fontFamily: 'PlaypenSans'}} 
                    color="orange"
                >
                    Replenish Candy     
                </Button>
            </Stack>
        </Container>
    </ThemeProvider>
  );
}

export default Main;
