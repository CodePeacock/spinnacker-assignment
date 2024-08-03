import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';

const Navbar = ({ isLoggedIn, handleLogout }) => {
    const navigate = useNavigate();

    const logout = () => {
        handleLogout();
        navigate('/login');
    };

    return (
        <nav className="navbar">
            <NavLink to="/" activeclassname="active-link">Home</NavLink>
            <div className="navbar-right">
                {isLoggedIn ? (
                    <>
                        <NavLink to="/add-contact" activeclassname="active-link">Add Contact</NavLink>
                        <NavLink to="/contacts" activeclassname="active-link">Contacts</NavLink>
                        <NavLink to="/search" activeclassname="active-link">Search</NavLink>
                        <button onClick={logout}>Logout</button>
                    </>
                ) : (
                    <>
                        <NavLink to="/register" activeclassname="active-link">Register</NavLink>
                        <NavLink to="/login" activeclassname="active-link">Login</NavLink>
                    </>
                )}
            </div>
        </nav>
    );
};

export default Navbar;