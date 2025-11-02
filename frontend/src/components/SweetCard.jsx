import api from "../api/apiClient"
import React from "react"//for testing

export default function SweetCard({ sweet, user, onUpdate, onEdit }) {
  const handlePurchase = async () => {
    try {
      await api.post(`/sweets/${sweet.id}/purchase`)
      onUpdate();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async () => {
    try {
      await api.delete(`/sweets/${sweet.id}`);
      onUpdate();
    } catch (err) {
      console.error(err);
    }
  };

const handleRestock = async () => {
  try {
    const amount = prompt("Enter amount to restock:", 10);
    if (!amount) return;

    await api.post(`/sweets/${sweet.id}/restock`, { amount: parseInt(amount) });
    onUpdate();
  } catch (err) {
    console.error("Error restocking sweet:", err);
  }
};


  return (
    <div className="bg-white/80 border border-white/30 rounded-2xl p-5 shadow-md hover:shadow-lg transition">
      <h2 className="text-xl font-semibold text-pink-600">{sweet.name}</h2>
      <p className="text-gray-500">{sweet.category}</p>
      <p className="text-lg font-medium">₹{sweet.price}</p>
      <p className="text-sm text-gray-600 mb-4">Stock: {sweet.quantity}</p>

      {user?.role === "admin" ? (
        <div className="space-y-2">
          <button
            onClick={() => onEdit(sweet)}
            className="w-full bg-indigo-500 hover:bg-indigo-600 text-white py-2 rounded-xl"
          >
            Edit
          </button>
          <button
            onClick={handleRestock}
            className="w-full bg-green-500 hover:bg-green-600 text-white py-2 rounded-xl"
          >
            Restock
          </button>
          <button
            onClick={handleDelete}
            className="w-full bg-red-500 hover:bg-red-600 text-white py-2 rounded-xl"
          >
            Delete
          </button>
        </div>
      ) : (
        <button
          onClick={handlePurchase}
          disabled={sweet.quantity === 0}
          className={`w-full py-2 rounded-xl text-white transition ${
            sweet.quantity > 0
              ? "bg-indigo-500 hover:bg-indigo-600"
              : "bg-gray-300 cursor-not-allowed"
          }`}
        >
          {sweet.quantity > 0 ? "Purchase" : "Out of Stock"}
        </button>
      )}
    </div>
  );
}
