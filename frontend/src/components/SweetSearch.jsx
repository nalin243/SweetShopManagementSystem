import { useState } from "react";

export default function SweetSearch({ onSearch }) {
  const [filters, setFilters] = useState({
    name: "",
    category: "",
    minPrice: "",
    maxPrice: "",
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(filters);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-wrap gap-3 justify-center mb-6"
    >
      <input
        type="text"
        placeholder="Name"
        value={filters.name}
        onChange={(e) => setFilters({ ...filters, name: e.target.value })}
        className="p-2 border rounded-lg w-40"
      />
      <input
        type="text"
        placeholder="Category"
        value={filters.category}
        onChange={(e) => setFilters({ ...filters, category: e.target.value })}
        className="p-2 border rounded-lg w-40"
      />
      <input
        type="number"
        placeholder="Min ₹"
        value={filters.minPrice}
        onChange={(e) => setFilters({ ...filters, minPrice: e.target.value })}
        className="p-2 border rounded-lg w-28"
      />
      <input
        type="number"
        placeholder="Max ₹"
        value={filters.maxPrice}
        onChange={(e) => setFilters({ ...filters, maxPrice: e.target.value })}
        className="p-2 border rounded-lg w-28"
      />
      <button
        type="submit"
        className="bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2 rounded-xl"
      >
        Search
      </button>
    </form>
  );
}
