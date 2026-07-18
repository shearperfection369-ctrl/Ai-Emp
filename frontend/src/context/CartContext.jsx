import { createContext, useContext, useEffect, useState } from "react";

const CartContext = createContext(null);
export const useCart = () => useContext(CartContext);

const KEY = "emporium_cart";

export function CartProvider({ children }) {
  const [items, setItems] = useState(() => {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; }
  });

  useEffect(() => {
    localStorage.setItem(KEY, JSON.stringify(items));
  }, [items]);

  const addItem = (tool) => {
    setItems((prev) => {
      if (prev.find((i) => i.slug === tool.slug)) return prev;
      return [...prev, {
        slug: tool.slug, name: tool.name, price: tool.price,
        lookup_key: tool.lookup_key, icon: tool.icon, quantity: 1,
      }];
    });
  };

  const removeItem = (slug) => setItems((prev) => prev.filter((i) => i.slug !== slug));
  const clear = () => setItems([]);
  const has = (slug) => items.some((i) => i.slug === slug);
  const total = items.reduce((s, i) => s + i.price * i.quantity, 0);

  return (
    <CartContext.Provider value={{ items, addItem, removeItem, clear, has, total, count: items.length }}>
      {children}
    </CartContext.Provider>
  );
}
