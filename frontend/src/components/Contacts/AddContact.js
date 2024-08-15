import React, { useState } from 'react';
import { addContact } from '../../services/api';
import { toast } from 'react-toastify';

const AddContact = () => {
    const [contactData, setContactData] = useState({
        name: '',
        phone_number: ''
    });
    const [note, setNote] = useState('');

    const handleAddContact = async (e) => {
        e.preventDefault(); // Prevent form submission
        try {
            const user_id = sessionStorage.getItem('user_id');
            const response = await addContact({ ...contactData, user_id });
            if (response.status === 201) {
                setContactData({
                    name: '',
                    phone_number: ''
                });
            }
            toast.success(String(response.data.message), { icon: <span role="img" aria-label="rocket">🚀</span> });
            if (response.data.message.includes('This user is added by someone already')) {
                setNote('This user is added by someone already');
            } else {
                setNote('');
            }
        } catch (error) {
            if (error.response) {
                toast.error(String(error.response.data.message), { icon: <span role="img" aria-label="sad">😥</span> });
            } else {
                toast.error('An error occurred');
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
                {note && <p>{note}</p>}
            </form>
        </div>
    );
};

export default AddContact;
