import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Register from './components/Auth/Register';
import Login from './components/Auth/Login';
import AddContact from './components/Contacts/AddContact';
import ContactList from './components/Contacts/ContactList';
import Search from './components/Search/Search';

const App = () => (
  <Router>
    <Routes>
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />
      <Route path="/add-contact" element={<AddContact />} />
      <Route path="/contacts" element={<ContactList />} />
      <Route path="/search" element={<Search />} />
    </Routes>
  </Router>
);

export default App;
