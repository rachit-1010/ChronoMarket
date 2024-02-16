import "../styles/SearchBar.css";

function SearchBar({ searchQuery, handleSearchChange, handleSearchSubmit }) {
  return (
    <div className="search-bar">
      <input type="text" value={searchQuery} onChange={handleSearchChange} />
      <button onClick={handleSearchSubmit}>Search</button>
    </div>
  );
}

export default SearchBar;
