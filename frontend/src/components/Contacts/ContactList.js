import React, { useEffect, useState } from 'react';
import { listContacts, markSpam } from '../../services/api';

const ContactList = () => {
    const [contacts, setContacts] = useState([]);
    const [spam, setSpam] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchContacts = async () => {
            try {
                const user_id = localStorage.getItem('user_id');
                if (!user_id) {
                    return;
                }

                const response = await listContacts(user_id);
                if (response.data.length === 0) {
                    setContacts([]);
                    setSpam([]);
                } else {
                    setContacts(response.data);
                    const spamContacts = response.data.filter(contact => contact.is_spam).map(contact => contact.phone_number);
                    setSpam(spamContacts);
                }
            } catch (error) {
                setError('Error fetching contacts');
            }
        };
        fetchContacts();
    }, []);

    const handleMarkSpam = async (phone_number, isSpam) => {
        try {
            const user_id = localStorage.getItem('user_id');
            await markSpam({ phone_number, user_id, isSpam });
            if (isSpam) {
                setSpam(prevSpam => [...prevSpam, phone_number]);
            } else {
                setSpam(prevSpam => prevSpam.filter(number => number !== phone_number));
            }
        } catch (error) {
            setError('Error marking spam');
        }
    };

    return (
        <div className="contact-list-container">
            {error && <p className="error-message">{error}</p>}
            {contacts.length === 0 ? (
                <p>No contacts found.</p>
            ) : (
                <div className="contact-cards">
                    {contacts.map((contact) => (
                        <div key={contact.phone_number} className="contact-card">
                            <h3>{contact.name}</h3>
                            <p>{contact.phone_number}</p>
                            <button
                                className={`spam-button ${spam.includes(contact.phone_number) ? 'not-spam' : 'spam'}`}
                                onClick={() => handleMarkSpam(contact.phone_number, !spam.includes(contact.phone_number))}>
                                {spam.includes(contact.phone_number) ? 'Mark as Not Spam' : 'Mark as Spam'}
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ContactList;