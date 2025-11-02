import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import SweetCard from "../src/components/SweetCard";
import api from "../src/api/apiClient";

// Mock the API client so it doesn’t actually call your backend
jest.mock("../src/api/apiClient", () => ({
  post: jest.fn(),
  delete: jest.fn(),
}));

describe("SweetCard Component", () => {
  const mockSweet = {
    id: "1",
    name: "Gulab Jamun",
    category: "Indian",
    price: 30,
    quantity: 5,
  };

  const mockUpdate = jest.fn();
  const mockEdit = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders sweet details correctly for customer", () => {
    render(<SweetCard sweet={mockSweet} user={{ role: "user" }} onUpdate={mockUpdate} />);
    expect(screen.getByText("Gulab Jamun")).toBeInTheDocument();
    expect(screen.getByText("Stock: 5")).toBeInTheDocument();
    expect(screen.getByText("Purchase")).toBeInTheDocument();
  });

  test("renders admin controls", () => {
    render(
      <SweetCard sweet={mockSweet} user={{ role: "admin" }} onUpdate={mockUpdate} onEdit={mockEdit} />
    );
    expect(screen.getByText("Edit")).toBeInTheDocument();
    expect(screen.getByText("Restock")).toBeInTheDocument();
    expect(screen.getByText("Delete")).toBeInTheDocument();
  });

  test("calls purchase API and updates UI", async () => {
    api.post.mockResolvedValueOnce({});
    render(<SweetCard sweet={mockSweet} user={{ role: "user" }} onUpdate={mockUpdate} />);

    const button = screen.getByText("Purchase");
    fireEvent.click(button);

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith("/sweets/1/purchase");
      expect(mockUpdate).toHaveBeenCalled();
    });
  });

  test("calls restock API and updates UI", async () => {
    api.post.mockResolvedValueOnce({});
    window.prompt = jest.fn().mockReturnValue("10"); // simulate entering 10 in prompt

    render(
      <SweetCard sweet={mockSweet} user={{ role: "admin" }} onUpdate={mockUpdate} onEdit={mockEdit} />
    );

    const restockBtn = screen.getByText("Restock");
    fireEvent.click(restockBtn);

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith("/sweets/1/restock", { amount: 10 });
      expect(mockUpdate).toHaveBeenCalled();
    });
  });

  test("calls delete API and updates UI", async () => {
    api.delete.mockResolvedValueOnce({});
    render(
      <SweetCard sweet={mockSweet} user={{ role: "admin" }} onUpdate={mockUpdate} onEdit={mockEdit} />
    );

    const deleteBtn = screen.getByText("Delete");
    fireEvent.click(deleteBtn);

    await waitFor(() => {
      expect(api.delete).toHaveBeenCalledWith("/sweets/1");
      expect(mockUpdate).toHaveBeenCalled();
    });
  });
});
