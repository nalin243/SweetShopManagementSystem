import { useEffect, useState } from "react";
import api from "../api/apiClient";
import { useAuth } from "../context/AuthContext";
import SweetCard from "../components/SweetCard";
import SweetSearch from "../components/SweetSearch";
import SweetFormModal from "../components/SweetFormModal";
import Navbar from "../components/Navbar";

export default function Dashboard() {
  const { user } = useAuth();
  const [sweets, setSweets] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editSweet, setEditSweet] = useState(null);

  // fetch sweets
  const fetchSweets = async (query = "") => {
    try {
      const res = await api.get(`/sweets${query}`);
      setSweets(res.data);
    } catch (error) {
      console.error("Error fetching sweets:", error);
    }
  };

  useEffect(() => {
    fetchSweets();
  }, []);

  const handleSearch = async (filters) => {
    const params = new URLSearchParams(filters).toString();
    fetchSweets(`/search?${params}`);
  };

  const handleEdit = (sweet) => {
    setEditSweet(sweet);
    setShowForm(true);
  };

  const handleCloseForm = () => {
    setEditSweet(null);
    setShowForm(false);
    fetchSweets();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 to-blue-50">
      <Navbar />
      <div className="max-w-7xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-center text-indigo-600 mb-8">
        Sweet Shop Dashboard
        </h1>

        <SweetSearch onSearch={handleSearch} />

        {
          <div className="flex justify-end mb-4">
            <button
              onClick={() => setShowForm(true)}
              className="bg-pink-500 hover:bg-pink-600 text-white px-5 py-2 rounded-xl transition"
            >
              + Add Sweet
            </button>
          </div>
        }

        {/* Sweet Cards */}
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {sweets.map((sweet) => (
            <SweetCard
              key={sweet.id}
              sweet={sweet}
              user={user}
              onUpdate={fetchSweets}
              onEdit={handleEdit}
            />
          ))}
        </div>
      </div>

      {showForm && (
        <SweetFormModal
          sweet={editSweet}
          onClose={handleCloseForm}
          onSuccess={fetchSweets}
        />
      )}
    </div>
  );
}
