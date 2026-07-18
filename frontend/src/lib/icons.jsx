import * as LucideIcons from "lucide-react";

export function Icon({ name, ...props }) {
  const Cmp = LucideIcons[name] || LucideIcons.Box;
  return <Cmp {...props} />;
}
