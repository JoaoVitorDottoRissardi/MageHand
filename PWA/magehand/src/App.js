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
import ProtectedRoute from './components/ProtectedRoute';

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
        <Route path='/main' element={<ProtectedRoute><Main/></ProtectedRoute>}/>
        <Route path="/editcandy" element={<ProtectedRoute><EditCandy/></ProtectedRoute>} />
        <Route path="/editpaymentkeys" element={<ProtectedRoute><EditPaymentKeys/></ProtectedRoute>} />
        <Route path="/purchasehistory" element={<ProtectedRoute><SeePurchaseHistory/></ProtectedRoute>} />
        <Route path="/changepassword" element={<ProtectedRoute><ChangePassword/></ProtectedRoute>} />
        <Route path="/replenishcandy" element={<ProtectedRoute><ReplenishCandy/></ProtectedRoute>} />
      </Routes>
    </Router>
  );
}

export default App;
