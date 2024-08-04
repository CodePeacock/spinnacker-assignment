import React, { useState } from 'react';
import { addContact } from '../../services/api';

const AddContact = () => {
    const [contactData, setContactData] = useState({
        name: '',
        phone_number: ''
    });

    const handleAddContact = async (e) => {
        e.preventDefault(); // Prevent form submission
        try {
            const user_id = localStorage.getItem('user_id');
            // get name of user from database using user_id
            const response = await addContact({ ...contactData, user_id });
            alert(response.data.message);
        } catch (error) {
            if (error.response) {
                alert(error.response.data.message);
            } else {
                alert('An error occurred');
            }
        }
    };
    return (
        <div className='div-container'>
            <form className='form'>
                <center><h2>Add Contact</h2></center>
                <input type="text" placeholder="Name" value={contactData.name} onChange={e => setContactData({ ...contactData, name: e.target.value })} required />
                <input type="text" placeholder="Phone Number" value={contactData.phone_number} onChange={e => setContactData({ ...contactData, phone_number: e.target.value })} required />
                <center><button onClick={handleAddContact}>Add Contact</button></center>
            </form>
        </div>
    );
};

export default AddContact;

