import React, { useEffect, useState } from 'react';
import { listContacts, markSpam } from '../../services/api';


const ContactList = () => {
    const [contacts, setContacts] = useState([]);
    const [spam, setSpam] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchContacts = async () => {
            try {
                const response = await listContacts(localStorage.getItem('user_id'));
                setContacts(response.data);
            } catch (error) {
                setError('Error fetching contacts');
            }
        };
        fetchContacts();
    }, []);

    const handleMarkSpam = async (phone_number) => {
        try {
            const user_id = localStorage.getItem('user_id');
            const response = await markSpam({ phone_number, user_id });
            setSpam(response.data);
        } catch (error) {
            setError('Error marking spam');
        }
    };

    return (
        <div>
            {error && <p>{error}</p>}
            <ul>
                {contacts.map((contact) => (
                    <li key={contact.phone_number}>
                        {contact.name} - {contact.phone_number}
                        <button onClick={() => handleMarkSpam(contact.phone_number)}>Mark Spam</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ContactList;
