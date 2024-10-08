import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../../services/api';
import { toast } from 'react-toastify';

const Login = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    const navigate = useNavigate();

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
            const response = await loginUser(formData);
            if (response.access_token && response.user_id) {
                sessionStorage.setItem('token', response.access_token);
                sessionStorage.setItem('user_id', response.user_id);
                navigate('/');
                window.location.reload(); // Reload to update the navbar
            } else {
                toast.error('Invalid login response');
            }
        } catch (error) {
            toast.error('Error logging in');
        }
    };

    return (
        <div className='div-container'>
            <form onSubmit={handleSubmit} className='form'>
                <center><h1>Login Page</h1></center>
                <input type="email" name="email" placeholder="Email" onChange={handleChange} required className='form-input' autoComplete='email' />
                <input type="password" name="password" placeholder="Password" onChange={handleChange} required className='form-input' />
                <button type="submit" className='form-button'> Login</button>
            </form>
        </div>
    );
};

export default Login;