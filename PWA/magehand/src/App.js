import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Alert from '@mui/material/Alert';
// import { initializeApp } from 'firebase/app';
// import { getAuth } from 'firebase/auth';
// import { getDatabase } from 'firebase/database';
import { messaging} from './firebase/config';
import { onMessage } from "firebase/messaging";
import Login from './components/Login';
import Main from './components/Main'; 
import EditPaymentKeys from './components/EditPaymentKeys'; 
import SeePurchaseHistory from './components/SeePurchaseHistory'; 
import ChangePassword from './components/ChangePassword'; 
import EditCandy from './components/EditCandy';
import ReplenishCandy from './components/ReplenishCandy';
import ProtectedRoute from './components/ProtectedRoute';

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export function ErrorMessage({message}){
  return (
    <Alert severity="error" sx={{ width:"40%", margin: "auto"}}>{message}</Alert>
  );
}

function App() {

  onMessage(messaging, (payload) => {
    console.log(payload);
    console.log("Recebido!");
    toast.warn(payload.notification.body, {
      position: "top-center",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "light",
    });
  })

  return (
    <div>
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
      <ToastContainer
        position="top-center"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
        />
    </div>
  );
}

export default App;
