import React, { useState } from 'react';
import { addContact } from '../../services/api';

const AddContact = () => {
    const [formData, setFormData] = useState({
        name: '',
        phone_number: '',
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
            await addContact({ ...formData, user_id: localStorage.getItem('user_id') });
            alert('Contact added successfully');
        } catch (error) {
            alert('Error adding contact');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" name="name" placeholder="Name" onChange={handleChange} required />
            <input type="text" name="phone_number" placeholder="Phone Number" onChange={handleChange} required />
            <button type="submit">Add Contact</button>
        </form>
    );
};

export default AddContact;
