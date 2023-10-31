import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import {app} from '../firebase/config'
import { getAuth } from "firebase/auth";

const ProtectedRoute = (props) => {
    const navigate = useNavigate();
    const auth = getAuth(app);

    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const checkUserToken = () => {
        if(auth.currentUser === null){
            setIsLoggedIn(false);
            return navigate('/');
          }
        setIsLoggedIn(true);
    }

    useEffect(() => {
        checkUserToken();
    }, [isLoggedIn]);

    return (
        <React.Fragment>
            {
                isLoggedIn ? props.children : null
            }
        </React.Fragment>
    );
}

export default ProtectedRoute;