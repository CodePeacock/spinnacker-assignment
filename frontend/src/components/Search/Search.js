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
        <div className="search-container">
            <form onSubmit={handleSearch} className="search-form">
                <input
                    type="text"
                    placeholder="Search by name or phone"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="search-input"
                />
                <button type="submit" className="search-button">Search</button>
            </form>
            <div className="results-container">
                {results.map((result) => (
                    <div key={result.phone_number} className="result-card">
                        <h3>{result.name}</h3>
                        <p>Phone: {result.phone_number}</p>
                        <p>Spam Likelihood: {result.spam_likelihood}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Search;