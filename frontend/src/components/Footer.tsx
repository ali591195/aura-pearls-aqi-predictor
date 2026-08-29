import type { ReactNode } from "react";
import "./Footer.css";

type SocialLinkProps = {
  label: string;
  href: string;
  icon: ReactNode;
};

function SocialLink({ label, href, icon }: SocialLinkProps) {
  return (
    <a
      className="footer-social-link"
      href={href}
      target="_blank"
      rel="noreferrer"
      aria-label={label}
    >
      <span className="footer-social-icon">{icon}</span>
      <span>{label}</span>
    </a>
  );
}

function GitHubIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path
        fill="currentColor"
        d="M12 .7a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2.2c-3.3.7-4-1.4-4-1.4-.5-1.3-1.3-1.7-1.3-1.7-1.1-.8.1-.8.1-.8 1.2.1 1.8 1.3 1.8 1.3 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.3-3.2-.1-.3-.6-1.6.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.7 1.6.3 2.9.1 3.2.8.8 1.3 1.9 1.3 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.2c0 .3.2.7.8.6A12 12 0 0 0 12 .7Z"
      />
    </svg>
  );
}

function LinkedInIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path
        fill="currentColor"
        d="M5.2 3.5A2.3 2.3 0 1 1 5.2 8a2.3 2.3 0 0 1 0-4.5ZM3.3 9.7h3.8V21H3.3V9.7Zm6.2 0h3.6v1.5h.1c.5-.9 1.7-1.9 3.6-1.9 3.8 0 4.5 2.5 4.5 5.8V21h-3.8v-5.2c0-1.2 0-2.9-1.8-2.9s-2.1 1.3-2.1 2.8V21H9.5V9.7Z"
      />
    </svg>
  );
}

function HuggingFaceIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle
        cx="12"
        cy="12"
        r="9"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.7"
      />
      <circle cx="8.5" cy="10" r="1.2" fill="currentColor" />
      <circle cx="15.5" cy="10" r="1.2" fill="currentColor" />
      <path
        d="M7.5 14.2c2.3 2.2 6.7 2.2 9 0"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.7"
        strokeLinecap="round"
      />
      <path
        d="M5.5 7.2 4.2 5.8M18.5 7.2l1.3-1.4"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
    </svg>
  );
}

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div className="footer-brand">
          <span className="footer-brand-name">AURA</span>
          <span className="footer-brand-description">
            Pearls AQI Predictor
          </span>
        </div>

        <nav className="footer-socials" aria-label="Social links">
          <SocialLink
            label="GitHub"
            href="https://github.com/ali591195"
            icon={<GitHubIcon />}
          />

          <SocialLink
            label="Hugging Face"
            href="https://huggingface.co/ali591195"
            icon={<HuggingFaceIcon />}
          />

          <SocialLink
            label="LinkedIn"
            href="https://www.linkedin.com/in/ali-hassan-483977245/"
            icon={<LinkedInIcon />}
          />
        </nav>

        <span className="footer-copy">© 2026 Aura</span>
      </div>
    </footer>
  );
}

export default Footer;