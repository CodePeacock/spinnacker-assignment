import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import '../node_modules/react-toastify/dist/ReactToastify.css';
import Register from './components/Auth/Register';
import Login from './components/Auth/Login';
import AddContact from './components/Contacts/AddContact';
import ContactList from './components/Contacts/ContactList';
import Search from './components/Search/Search';
import Navbar from './components/NavBar';
import './App.css';


const Home = () => (
  <div className="home" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '60vh' }}>
    {/* show svg as logo */}
    <img
      src="https://www.svgrepo.com/show/169527/phone-book.svg"
      className='logo rotate'
      alt="logo"
      style={{ width: '100px', height: '100px' }}
    />
    <h1>Welcome to Contact Application</h1>
    <b><h2>😊This is a simple application to manage your contacts📃</h2></b>
    <div className="buttons">
      <Link to="/register" className="btn register">Register</Link>
      <Link to="/login" className="btn login">Login</Link>
    </div>
  </div>
);

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const user_id = sessionStorage.getItem('user_id');
    const token = sessionStorage.getItem('token');
    if (user_id && token) {
      setIsLoggedIn(true);
    }
  }, []);

  const handleLogout = () => {
    sessionStorage.removeItem('user_id');
    sessionStorage.removeItem('token');
    setIsLoggedIn(false);
  };

  return (
    <Router>
      <Navbar isLoggedIn={isLoggedIn} handleLogout={handleLogout} />
      <Routes>
        <Route path="/" element={isLoggedIn ? <Navigate to="/contacts" /> : <Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/add-contact" element={<AddContact />} />
        <Route path="/contacts" element={<ContactList />} />
        <Route path="/search" element={<Search />} />
      </Routes>
      <ToastContainer stacked />
    </Router>
  );
};

export default App;