import React, { useState } from 'react';
import { searchByName, searchByPhone } from '../../services/api';

const Search = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = async (e) => {
        e.preventDefault();
        try {
            const nameResults = await searchByName(query);
            const phoneResults = await searchByPhone(query);
            setResults([...nameResults.data, ...phoneResults.data]);
        } catch (error) {
            alert('Error searching');
        }
    };

    return (
        <div>
            <form onSubmit={handleSearch}>
                <input type="text" placeholder="Search by name or phone" value={query} onChange={(e) => setQuery(e.target.value)} />
                <button type="submit">Search</button>
            </form>
            <ul>
                {results.map((result) => (
                    <li key={result.phone_number}>
                        {result.name} - {result.phone_number} (Spam Likelihood: {result.spam_likelihood})
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Search;
