import React, { useEffect, useState } from 'react';
import { listContacts, markSpam, deleteContact, addContact } from '../../services/api';
import { toast } from 'react-toastify';
import RequireAuth from '../Auth/RequireAuth';

const ContactList = () => {
    const [contacts, setContacts] = useState([]);
    const [spam, setSpam] = useState([]);
    const [error, setError] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [, setDeletedContact] = useState(null);

    useEffect(() => {
        const fetchContacts = async () => {
            try {
                const user_id = sessionStorage.getItem('user_id');
                if (!user_id) {
                    return;
                }

                const response = await listContacts(user_id);
                if (response.data.length === 0) {
                    setContacts([]);
                    setSpam([]);
                } else {
                    console.log('response.data:', response.data);
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
            const user_id = sessionStorage.getItem('user_id');
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

    const handleDeleteContact = async (contact_id) => {
        try {
            const contactToDelete = contacts.find(contact => contact.id === contact_id);
            await deleteContact(contact_id);
            setContacts(prevContacts => prevContacts.filter(contact => contact.id !== contact_id));
            setDeletedContact(contactToDelete);
            toast.success('Contact deleted. Click me to Undo?', {
                onClick: () => handleUndoDelete(contactToDelete),
                autoClose: 5000,
                style: { cursor: 'pointer', fontWeight: 'bold' }
            });
        } catch (error) {
            setError('Error deleting contact');
        }
    };

    const handleUndoDelete = async (contact) => {
        try {
            const user_id = sessionStorage.getItem('user_id');
            await addContact({ ...contact, user_id });
            setContacts(prevContacts => [...prevContacts, contact]);
            setDeletedContact(null);
            toast.success('Contact restored');
        } catch (error) {
            setError('Error restoring contact');
        }
    };

    const handleSearch = (event) => {
        setSearchQuery(event.target.value);
    };

    const filteredContacts = contacts.filter(contact =>
        contact.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        contact.phone_number.includes(searchQuery)
    );

    return (
        <RequireAuth>
            <div className="contact-list-container">
                <header className="contact-list-header">
                    <h1>Contact List</h1>
                    <input
                        type="text"
                        placeholder="Search contacts..."
                        value={searchQuery}
                        onChange={handleSearch}
                        className="search-input"
                    />
                </header>
                <br />
                {error && <p className="error-message">{error}</p>}
                {contacts.length === 0 ? (
                    <p>No contacts found.</p>
                ) : (
                    <div className="contact-cards">
                        {filteredContacts.map((contact) => (
                            <div key={contact.phone_number} className="contact-card">
                                <h3>{contact.name}</h3>
                                <p>{contact.phone_number}</p>
                                <button
                                    className={`spam-button ${spam.includes(contact.phone_number) ? 'not-spam' : 'spam'}`}
                                    onClick={() => handleMarkSpam(contact.phone_number, !spam.includes(contact.phone_number))}>
                                    {spam.includes(contact.phone_number) ? 'Mark as Not Spam' : 'Mark as Spam'}
                                </button>
                                <button
                                    className="delete-button"
                                    onClick={() => handleDeleteContact(contact.id)}>
                                    ❌
                                </button>
                            </div>
                        ))}
                    </div>
                )}
                <footer className="contact-list-footer">
                    <b><p>&copy; 2024 Contact List App</p></b>
                </footer>
            </div>
        </RequireAuth>
    );
};

export default ContactList;