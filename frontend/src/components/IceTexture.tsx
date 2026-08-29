import "./IceTexture.css";

type IceTextureProps = {
  variant?: "dark" | "light";
};

function IceTexture({ variant = "dark" }: IceTextureProps) {
  return (
    <div
      className={`ice-texture ${variant === "light" ? "ice-texture-light" : ""}`}
      aria-hidden="true"
    >
      <svg
        className="ice-texture-svg"
        viewBox="0 0 500 1000"
        preserveAspectRatio="none"
      >
        <defs>
          <linearGradient
            id="ice-surface-gradient"
            x1="0%"
            y1="0%"
            x2="100%"
            y2="100%"
          >
            <stop offset="0%" stopColor="#dcefff" stopOpacity="0.055" />
            <stop offset="45%" stopColor="#8ebbd0" stopOpacity="0.018" />
            <stop offset="100%" stopColor="#22d3ee" stopOpacity="0.035" />
          </linearGradient>
        </defs>

        {/* Large fractured ice planes */}
        <path
          d="M-60 80 L170 0 L290 130 L220 280 L20 230 Z"
          fill="url(#ice-surface-gradient)"
        />

        <path
          d="M170 0 L430 70 L500 230 L290 130 Z"
          fill="#dcefff"
          fillOpacity="0.018"
        />

        <path
          d="M20 230 L220 280 L180 500 L-40 450 Z"
          fill="#b8d9e8"
          fillOpacity="0.018"
        />

        <path
          d="M220 280 L500 230 L440 470 L180 500 Z"
          fill="#7eaec1"
          fillOpacity="0.02"
        />

        <path
          d="M-40 450 L180 500 L120 700 L-70 650 Z"
          fill="#dcefff"
          fillOpacity="0.012"
        />

        <path
          d="M180 500 L440 470 L510 700 L120 700 Z"
          fill="#5f91a8"
          fillOpacity="0.018"
        />

        <path
          d="M120 700 L510 700 L460 1000 L-50 1000 Z"
          fill="#dcefff"
          fillOpacity="0.012"
        />

        {/* Main fracture network */}
        <g
          fill="none"
          stroke="var(--ice-primary)"
          strokeOpacity="0.085"
          strokeWidth="1.2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M165 0 L190 90 L170 180 L220 280" />
          <path d="M190 90 L95 135 L20 230" />
          <path d="M170 180 L75 205 L20 230" />

          <path d="M220 280 L300 340 L440 470" />
          <path d="M300 340 L250 430 L180 500" />
          <path d="M250 430 L335 455 L440 470" />

          <path d="M180 500 L225 590 L120 700" />
          <path d="M225 590 L330 620 L510 700" />

          <path d="M330 620 L385 540 L440 470" />

          <path d="M120 700 L210 785 L250 900 L460 1000" />
          <path d="M210 785 L95 835 L-40 900" />

          <path d="M250 900 L355 820 L510 700" />
        </g>

        {/* Fine secondary fractures */}
        <g
          fill="none"
          stroke="var(--ice-secondary)"
          strokeOpacity="0.035"
          strokeWidth="0.8"
          strokeLinecap="round"
        >
          <path d="M95 135 L125 175 L75 205" />
          <path d="M300 340 L350 300 L430 320" />
          <path d="M335 455 L380 415 L440 470" />
          <path d="M225 590 L180 640 L120 700" />
          <path d="M210 785 L275 760 L330 620" />
          <path d="M355 820 L400 875 L460 1000" />
        </g>
      </svg>
    </div>
  );
}

export default IceTexture;