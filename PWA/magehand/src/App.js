import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Alert from '@mui/material/Alert';
// import { initializeApp } from 'firebase/app';
// import { getAuth } from 'firebase/auth';
// import { getDatabase } from 'firebase/database';
import Login from './components/Login';
import Main from './components/Main'; 
import EditPaymentKeys from './components/EditPaymentKeys'; 
import SeePurchaseHistory from './components/SeePurchaseHistory'; 
import ChangePassword from './components/ChangePassword'; 
import EditCandy from './components/EditCandy';
import ReplenishCandy from './components/ReplenishCandy';

export function ErrorMessage({message}){
  return (
    <Alert severity="error" sx={{ width:"40%", margin: "auto"}}>{message}</Alert>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login/>} />
        <Route path='/main' element={<Main/>}/>
        <Route path="/editcandy" element={<EditCandy/>} />
        <Route path="/editpaymentkeys" element={<EditPaymentKeys/>} />
        <Route path="/purchasehistory" element={<SeePurchaseHistory/>} />
        <Route path="/changepassword" element={<ChangePassword/>} />
        <Route path="/replenishcandy" element={<ReplenishCandy/>} />
      </Routes>
    </Router>
  );
}

export default App;
