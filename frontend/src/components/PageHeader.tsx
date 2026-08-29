import PageHeaderIce from "./PageHeaderIce";
import "./PageHeader.css";

type PageHeaderProps = {
  title: string;
  subtitle?: string;
};

function PageHeader({ title, subtitle }: PageHeaderProps) {
  return (
    <header className="page-header">
      <PageHeaderIce />

      <div className="page-header-text">
        <h1 className="page-header-title">{title}</h1>

        {subtitle && (
          <p className="page-header-subtitle">
            {subtitle}
          </p>
        )}
      </div>
    </header>
  );
}

export default PageHeader;