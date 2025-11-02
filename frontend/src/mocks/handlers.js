import { http, HttpResponse } from "msw";

let sweets = [
  { id: "1", name: "Gulab Jamun", category: "Indian", price: 30, quantity: 5 },
];

export const handlers = [
  // GET sweets
  http.get("http://localhost:8000/api/sweets", () => {
    return HttpResponse.json(sweets, { status: 200 });
  }),

  // POST restock (admin only)
  http.post("http://localhost:8000/api/sweets/:id/restock", async ({ params, request }) => {
    const { id } = params;
    const body = await request.json();

    const sweet = sweets.find((s) => s.id === id);
    if (!sweet) return HttpResponse.json({ detail: "Sweet not found" }, { status: 404 });

    sweet.quantity += body.amount;
    return HttpResponse.json(sweet, { status: 200 });
  }),
];
