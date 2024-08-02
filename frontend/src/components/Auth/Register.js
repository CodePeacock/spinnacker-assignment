import React, { useState } from 'react';
import { registerUser } from '../../services/api';

const Register = () => {
    const [formData, setFormData] = useState({
        name: '',
        phone_number: '',
        password: '',
        email: '',
        city: '',
        country: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await registerUser(formData);
            alert('User registered successfully. Please verify your email.');
        } catch (error) {
            alert('Error registering user');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" name="name" placeholder="Name" onChange={handleChange} required />
            <input type="text" name="phone_number" placeholder="Phone Number" onChange={handleChange} required />
            <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
            <input type="email" name="email" placeholder="Email" onChange={handleChange} required />
            <input type="text" name="city" placeholder="City" onChange={handleChange} />
            <input type="text" name="country" placeholder="Country" onChange={handleChange} />
            <button type="submit">Register</button>
        </form>
    );
};

export default Register;
