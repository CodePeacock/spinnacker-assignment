import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Register from './components/Auth/Register';
import Login from './components/Auth/Login';
import AddContact from './components/Contacts/AddContact';
import ContactList from './components/Contacts/ContactList';
import Search from './components/Search/Search';
import Navbar from './components/NavBar';
import './App.css';

const Home = () => (
  <div className="home">
    <h1>Welcome to My Application</h1>
    <p>😊This is a simple application to manage your contacts📃</p>
    <div className="buttons">
      <Link to="/register" className="btn register">Register</Link>
      <Link to="/login" className="btn login">Login</Link>
    </div>
  </div>
);

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const user_id = localStorage.getItem('user_id');
    if (user_id) {
      setIsLoggedIn(true);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('user_id');
    setIsLoggedIn(false);
  };

  return (
    <Router>
      <Navbar isLoggedIn={isLoggedIn} handleLogout={handleLogout} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/add-contact" element={<AddContact />} />
        <Route path="/contacts" element={<ContactList />} />
        <Route path="/search" element={<Search />} />
      </Routes>
    </Router>
  );
};

export default App;