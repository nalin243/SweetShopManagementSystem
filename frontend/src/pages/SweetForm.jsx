import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/apiClient";

export default function SweetForm() {
  const [form, setForm] = useState({
    name: "",
    category: "",
    price: "",
    quantity: "",
  });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.post("/sweet", form);
    navigate("/");
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded-xl shadow-md w-96"
      >
        <h2 className="text-2xl font-bold mb-4 text-center">Add New Sweet</h2>
        {Object.keys(form).map((key) => (
          <input
            key={key}
            className="w-full p-2 border rounded mb-3"
            placeholder={key.charAt(0).toUpperCase() + key.slice(1)}
            value={form[key]}
            onChange={(e) => setForm({ ...form, [key]: e.target.value })}
          />
        ))}
        <button className="w-full bg-blue-600 text-white py-2 rounded">
          Add Sweet
        </button>
      </form>
    </div>
  );
}
