import type { ReactNode } from "react";
import "./SectionHeader.css";

type SectionHeaderProps = {
  title: string;
  subtitle?: string;
  action?: ReactNode;
};

function SectionHeader({
  title,
  subtitle,
  action,
}: SectionHeaderProps) {
  return (
    <div className="section-header">
      <div className="section-header-text">
        <h2>{title}</h2>

        {subtitle && <p>{subtitle}</p>}
      </div>

      {action && (
        <div className="section-header-action">
          {action}
        </div>
      )}
    </div>
  );
}

export default SectionHeader;