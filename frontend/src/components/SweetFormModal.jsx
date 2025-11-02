import { useState, useEffect } from "react";
import api from "../api/apiClient";

export default function SweetFormModal({ sweet, onClose, onSuccess }) {
  const [form, setForm] = useState({
    name: "",
    category: "",
    price: "",
    quantity: "",
  });

  useEffect(() => {
    if (sweet) setForm(sweet);
  }, [sweet]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (sweet) {
        await api.put(`/sweets/${sweet.id}`, form);
      } else {
        await api.post("/sweet", form);
      }
      onSuccess();
      onClose();
    } catch (err) {
      console.error("Error saving sweet:", err);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex justify-center items-center">
      <div className="bg-white p-6 rounded-xl w-full max-w-md shadow-xl">
        <h2 className="text-2xl font-semibold text-center mb-4 text-indigo-600">
          {sweet ? "Edit Sweet" : "Add New Sweet"}
        </h2>

        <form onSubmit={handleSubmit} className="space-y-3">
          {["name", "category", "price", "quantity"].map((key) => (
            <input
              key={key}
              type={key === "price" || key === "quantity" ? "number" : "text"}
              placeholder={key[0].toUpperCase() + key.slice(1)}
              value={form[key]}
              onChange={(e) => setForm({ ...form, [key]: e.target.value })}
              className="w-full p-2 border rounded-lg"
            />
          ))}

          <div className="flex justify-end gap-2 mt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-gray-300 rounded-lg"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-indigo-500 hover:bg-indigo-600 text-white rounded-lg"
            >
              {sweet ? "Update" : "Add"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
