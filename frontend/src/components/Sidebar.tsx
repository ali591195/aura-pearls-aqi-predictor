import type { ReactNode } from "react";
import { NavLink } from "react-router-dom";
import "./Sidebar.css";
import IceTexture from "./IceTexture";

type NavItemProps = {
  label: string;
  icon: ReactNode;
  to?: string;
  disabled?: boolean;
};

function NavItem({
  label,
  icon,
  to,
  disabled = false,
}: NavItemProps) {
  if (disabled) {
    return (
      <button
        className="sidebar-nav-item disabled"
        type="button"
        disabled
      >
        <span className="nav-icon">{icon}</span>

        <span className="nav-label">{label}</span>

        <span className="nav-lock" aria-label="Coming soon">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <rect
              x="5"
              y="10"
              width="14"
              height="10"
              rx="2"
            />
            <path d="M8 10V7a4 4 0 0 1 8 0v3" />
          </svg>
        </span>
      </button>
    );
  }

  return (
    <NavLink
      to={to!}
      className={({ isActive }) =>
        `sidebar-nav-item ${isActive ? "active" : ""}`
      }
    >
      <span className="nav-icon">{icon}</span>

      <span className="nav-label">{label}</span>
    </NavLink>
  );
}

function PredictionIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="8" />
      <path d="M12 8v4l3 2" />
    </svg>
  );
}

function StatsIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M5 19V9" />
      <path d="M12 19V5" />
      <path d="M19 19v-7" />
    </svg>
  );
}

function CityIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M4 20h16" />
      <path d="M6 20V9l6-4 6 4v11" />
      <path d="M9 12h1" />
      <path d="M14 12h1" />
      <path d="M9 16h1" />
      <path d="M14 16h1" />
    </svg>
  );
}

function BackfillIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M4 12a8 8 0 0 1 13.3-6" />
      <path d="M20 5v5h-5" />
      <path d="M20 12a8 8 0 0 1-13.3 6" />
      <path d="M4 19v-5h5" />
    </svg>
  );
}

function Sidebar() {
  return (
    <aside className="sidebar">
      <IceTexture />

      <div className="sidebar-inner">
        <NavLink className="sidebar-brand" to="/">
          <img
            className="sidebar-logo"
            src="/logo.png"
            alt="Aura logo"
          />

          <span className="sidebar-brand-text">
            <span className="sidebar-brand-name">AURA</span>
            <span className="sidebar-brand-subtitle">
              Pearls AQI Predictor
            </span>
          </span>
        </NavLink>

        <nav className="sidebar-navigation" aria-label="Main navigation">
            <NavItem
              label="Prediction"
              icon={<PredictionIcon />}
              to="/"
            />

            <NavItem
              label="Stats"
              icon={<StatsIcon />}
              to="/stats"
            />

            <NavItem
              label="City"
              icon={<CityIcon />}
              disabled
            />

            <NavItem
              label="Backfill"
              icon={<BackfillIcon />}
              disabled
            />
        </nav>
      </div>
    </aside>
  );
}

export default Sidebar;