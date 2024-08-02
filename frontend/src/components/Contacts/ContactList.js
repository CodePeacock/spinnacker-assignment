import React, { useEffect, useState } from 'react';
import { listContacts } from '../../services/api';

const ContactList = () => {
    const [contacts, setContacts] = useState([]);

    useEffect(() => {
        const fetchContacts = async () => {
            try {
                const response = await listContacts(localStorage.getItem('user_id'));
                setContacts(response.data);
            } catch (error) {
                alert('Error fetching contacts');
            }
        };
        fetchContacts();
    }, []);

    return (
        <ul>
            {contacts.map((contact) => (
                <li key={contact.phone_number}>{contact.name} - {contact.phone_number}</li>
            ))}
        </ul>
    );
};

export default ContactList;
