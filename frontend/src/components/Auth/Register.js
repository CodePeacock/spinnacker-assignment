import React, { useState } from 'react';
import { registerUser, verifyOtp } from '../../services/api'; // Assuming these are the API calls
import { Link, useNavigate } from 'react-router-dom';

const Register = () => {
    const [otp, setOtp] = useState('');
    const [formData, setFormData] = useState({
        name: '',
        phone_number: '',
        password: '',
        email: '',
        city: '',
        country: '',
    });
    const [isRegistered, setIsRegistered] = useState(false);
    const navigate = useNavigate();
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleVerifyOtp = async (e) => {
        try {
            e.preventDefault();
            if (otp.length !== 6) {
                alert('Invalid OTP. Please enter a 6-digit OTP.');
                return;
            }

            const response = await verifyOtp({ email: formData.email, otp });
            if (response.success) {
                alert('OTP verified successfully.');
                navigate('/login'); // Redirect to login page on success
            } else {
                alert('Invalid OTP. Please enter the correct OTP.');
            }
        } catch (error) {
            console.error('Error during OTP verification:', error);
            alert('An error occurred. Please try again.');
        }
    };
    const validatePhoneNumber = (phoneNumber) => {
        const phoneNumberRegex = /^[6-9]\d{9}$/;
        return phoneNumberRegex.test(phoneNumber);
    };

    const validateEmail = (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    const validatePassword = (password) => {
        const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
        return passwordRegex.test(password);
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            if (!validatePhoneNumber(formData.phone_number)) {
                alert('Invalid phone number. Please enter a valid 10-digit phone number.');
                return;
            }

            if (!validateEmail(formData.email)) {
                alert('Invalid email. Please enter a valid email address.');
                return;
            }

            if (!validatePassword(formData.password)) {
                alert('Invalid password. Password must be at least 8 characters long and contain a mix of alphanumeric characters.');
                return;
            }

            const response = await registerUser(formData);
            setIsRegistered(true);
            alert(response.message || 'User registered successfully. Please verify your email.');
        } catch (error) {
            console.error('Registration Error:', error);
            alert('Error registering user');
        }
    };

    return (
        <div className='div-container'>
            {isRegistered ?
                <form onSubmit={handleVerifyOtp} className='form'>
                    <center><h1>OTP Verification</h1></center>
                    <input
                        type="text"
                        name="otp"
                        placeholder="Enter OTP"
                        value={otp}
                        onChange={(e) => setOtp(e.target.value)}
                        required
                        className='form-input'
                    />
                    <button type="submit" className='form-button'>Verify OTP</button>
                </form>
                :
                <form onSubmit={handleRegister} className='form'>
                    <center><h1>Registration Page</h1></center>
                    <input type="text" name="name" placeholder="Name" onChange={handleChange} required className='form-input' />
                    <input type="tel" name="phone_number" placeholder="Phone Number" onChange={handleChange} required pattern="[6-9]{1}[0-9]{9}" title="Please enter a valid 10-digit phone number." className='form-input' />
                    <input type="email" name="email" placeholder="Email" onChange={handleChange} required pattern="[^\s@]+@[^\s@]+\.[^\s@]+" title="Please enter a valid email address." className='form-input' />
                    <input type="password" name="password" placeholder="Password" onChange={handleChange} required pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$" title="Password must be at least 8 characters long and contain a mix of alphanumeric characters." className='form-input' />
                    <input type="text" name="city" placeholder="City" onChange={handleChange} className='form-input' />
                    <input type="text" name="country" placeholder="Country" onChange={handleChange} className='form-input' />
                    <button type="submit" className='form-button'>Register</button>
                    Already have an account? {'   '}
                    <b><Link to="/login" className='redirectlogin'>Login</Link></b>
                </form>
            }
        </div>
    );
};

export default Register;
