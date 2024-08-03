import React, { useState } from 'react';
import { addContact } from '../../services/api';

const AddContact = () => {
    const [contactData, setContactData] = useState({
        name: '',
        phone_number: ''
    });

    const handleAddContact = async () => {
        try {
            const user_id = localStorage.getItem('user_id');
            const response = await addContact({ ...contactData, user_id });
            alert(response.data.message);
        } catch (error) {
            alert(error.response.data.message);
        }
    };

    return (
        <div className='div-container'>
            <form onSubmit={handleAddContact} className='form'>
                <center><h2>Add Contact</h2></center>
                <input type="text" placeholder="Name" value={contactData.name} onChange={e => setContactData({ ...contactData, name: e.target.value })} />
                <input type="text" placeholder="Phone Number" value={contactData.phone_number} onChange={e => setContactData({ ...contactData, phone_number: e.target.value })} />
                <center><button onClick={handleAddContact}>Add Contact</button></center>
            </form>
        </div>
    );
};

export default AddContact;

