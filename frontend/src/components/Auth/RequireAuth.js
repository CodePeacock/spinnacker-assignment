import React from 'react';
import { Navigate } from 'react-router-dom';

const RequireAuth = ({ children }) => {
    const user_id = sessionStorage.getItem('user_id');
    const token = sessionStorage.getItem('token');

    if (!user_id || !token) {
        // Redirect to the login page
        return <Navigate to="/login" replace />;
    }

    return children;
};

export default RequireAuth;