import {
  Home,
  TrendingUp,
  Package,
  Users,
  Sparkles,
  Settings,
  LogOut,
  Coffee,
  Wheat,
} from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Button } from "../ui/button";

const menuItems = [
  { icon: Home, label: "Dashboard", id: "dashboard" },
  { icon: TrendingUp, label: "Sales Analytics", id: "sales" },
  { icon: Package, label: "Inventory", id: "inventory" },
  { icon: Wheat, label: "Ingredients", id: "ingredients" },
  { icon: Users, label: "Staff Management", id: "staff" },
  { icon: Sparkles, label: "AI Insights", id: "ai-insights" },
  { icon: Settings, label: "Settings", id: "settings" },
];

interface SidebarProps {
  activePage: string;
  onPageChange: (pageId: string) => void;
  onLogout?: () => void;
  isOpen?: boolean;
  onClose?: () => void;
}

export function Sidebar({ activePage, onPageChange, onLogout, isOpen = false, onClose }: SidebarProps) {
  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <div className={`
        fixed lg:static inset-y-0 left-0 z-50
        w-64 h-screen bg-[#fffaf3] border-r border-[#d8c3a5]/30 flex flex-col
        transform transition-transform duration-300 ease-in-out lg:transform-none
        ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
      {/* Logo */}
      <div className="p-6 flex items-center gap-3">
        <div className="w-10 h-10 bg-gradient-to-br from-[#8b5e3c] to-[#b08968] rounded-xl flex items-center justify-center">
          <Coffee className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-[#8b5e3c]">DataBrew</h1>
          <p className="text-xs text-[#8b5e3c]/60">Analytics</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onPageChange(item.id)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl mb-1 transition-all ${
              activePage === item.id
                ? "bg-[#8b5e3c] text-white shadow-lg shadow-[#8b5e3c]/20"
                : "text-[#8b5e3c]/70 hover:bg-[#d8c3a5]/20 hover:text-[#8b5e3c]"
            }`}
          >
            <item.icon className="w-5 h-5" />
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      {/* Profile Section */}
      <div className="p-4 border-t border-[#d8c3a5]/30">
        <div className="flex items-center gap-3 mb-3">
          <Avatar>
            <AvatarImage src="https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah" />
            <AvatarFallback>SA</AvatarFallback>
          </Avatar>
          <div className="flex-1">
            <p className="text-sm text-[#8b5e3c]">Sarah Ahmed</p>
            <p className="text-xs text-[#8b5e3c]/60">Owner</p>
          </div>
        </div>
        <Button
          variant="outline"
          className="w-full border-[#d8c3a5] text-[#8b5e3c] hover:bg-[#d8c3a5]/20"
          onClick={onLogout}
        >
          <LogOut className="w-4 h-4 mr-2" />
          Logout
        </Button>
      </div>
    </div>
    </>
  );
}
