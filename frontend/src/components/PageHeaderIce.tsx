function PageHeaderIce() {
  return (
    <div className="page-header-ice" aria-hidden="true">
      <svg
        className="page-header-ice-svg"
        viewBox="0 0 1200 180"
        preserveAspectRatio="none"
      >
        <defs>
          {/* Ice pane refractions */}
          <linearGradient
            id="header-ice-pane-a"
            x1="0%"
            y1="0%"
            x2="100%"
            y2="100%"
          >
            <stop offset="0%" stopColor="#bfdbfe" stopOpacity="0.08" />
            <stop offset="100%" stopColor="#22d3ee" stopOpacity="0.045" />
          </linearGradient>

          <linearGradient
            id="header-ice-pane-b"
            x1="100%"
            y1="0%"
            x2="0%"
            y2="100%"
          >
            <stop offset="0%" stopColor="#c4b5fd" stopOpacity="0.075" />
            <stop offset="100%" stopColor="#93c5fd" stopOpacity="0.035" />
          </linearGradient>

          <linearGradient
            id="header-ice-pane-c"
            x1="0%"
            y1="100%"
            x2="100%"
            y2="0%"
          >
            <stop offset="0%" stopColor="#67e8f9" stopOpacity="0.07" />
            <stop offset="100%" stopColor="#a5b4fc" stopOpacity="0.035" />
          </linearGradient>
        </defs>

        {/* ====================================================== */}
        {/* ICE PLANES                                              */}
        {/* ====================================================== */}

        <path
          d="M-40 28 L150 0 L285 65 L235 145 L50 125 Z"
          fill="url(#header-ice-pane-a)"
        />

        <path
          d="M150 0 L365 28 L430 95 L285 65 Z"
          fill="url(#header-ice-pane-b)"
        />

        <path
          d="M235 145 L430 95 L560 155 L470 185 L300 170 Z"
          fill="#94a3b8"
          fillOpacity="0.045"
        />

        <path
          d="M430 95 L620 35 L735 80 L690 150 L560 155 Z"
          fill="url(#header-ice-pane-c)"
        />

        <path
          d="M620 35 L835 0 L925 55 L735 80 Z"
          fill="url(#header-ice-pane-b)"
        />

        <path
          d="M690 150 L925 55 L1045 100 L1000 180 L805 170 Z"
          fill="url(#header-ice-pane-a)"
        />

        <path
          d="M925 55 L1120 15 L1240 60 L1045 100 Z"
          fill="#93c5fd"
          fillOpacity="0.045"
        />

        <path
          d="M1045 100 L1240 60 L1210 180 L1000 180 Z"
          fill="url(#header-ice-pane-b)"
        />

        {/* ====================================================== */}
        {/* FRACTURE NETWORK                                        */}
        {/* ====================================================== */}

        <g
          id="header-main-cracks"
          fill="none"
          stroke="#475569"
          strokeOpacity="0.18"
          strokeWidth="1.2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path id="crack-1" d="M0 40 L150 78 L235 145" />
          <path id="crack-2" d="M150 78 L205 38 L150 0" />
          <path id="crack-3" d="M150 78 L95 110 L50 125" />

          <path id="crack-4" d="M235 145 L300 110 L365 30" />
          <path id="crack-5" d="M300 110 L285 65" />
          <path id="crack-6" d="M300 110 L430 95" />

          <path id="crack-7" d="M430 95 L500 55 L620 35" />
          <path id="crack-8" d="M500 55 L560 155" />
          <path id="crack-9" d="M560 155 L690 150 L735 80" />

          <path id="crack-10" d="M620 35 L675 55 L735 80" />
          <path id="crack-11" d="M735 80 L835 45 L925 55" />

          <path id="crack-12" d="M690 150 L805 120 L1000 180" />
          <path id="crack-13" d="M805 120 L835 45" />

          <path id="crack-14" d="M925 55 L980 78 L1045 100" />
          <path id="crack-15" d="M980 78 L1060 48 L1120 15" />

          <path id="crack-16" d="M1045 100 L1085 135 L1000 180" />
          <path id="crack-17" d="M1085 135 L1160 115 L1210 180" />
        </g>

        {/* ====================================================== */}
        {/* COLORED REFRACTION — EXACT SAME CRACK GEOMETRY         */}
        {/* ====================================================== */}

        {/* Cyan */}
        <g
          fill="none"
          stroke="#0891b2"
          strokeOpacity="0.18"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <use href="#crack-1" />
          <use href="#crack-6" />
          <use href="#crack-9" />
          <use href="#crack-14" />
        </g>

        {/* Violet */}
        <g
          fill="none"
          stroke="#7c3aed"
          strokeOpacity="0.15"
          strokeWidth="1.6"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <use href="#crack-2" />
          <use href="#crack-7" />
          <use href="#crack-11" />
          <use href="#crack-16" />
        </g>

        {/* Pale blue refraction */}
        <g
          fill="none"
          stroke="#60a5fa"
          strokeOpacity="0.12"
          strokeWidth="1.4"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <use href="#crack-4" />
          <use href="#crack-8" />
          <use href="#crack-12" />
          <use href="#crack-17" />
        </g>

        {/* ====================================================== */}
        {/* FINE SECONDARY FRACTURES                                */}
        {/* ====================================================== */}

        <g
          fill="none"
          stroke="#64748b"
          strokeOpacity="0.12"
          strokeWidth="0.7"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M95 110 L120 88 L150 78" />
          <path d="M205 38 L225 65 L195 92" />
          <path d="M300 110 L325 82 L365 95" />

          <path d="M500 55 L480 82 L505 110" />
          <path d="M560 155 L595 120 L620 140" />
          <path d="M675 55 L700 35 L735 80" />

          <path d="M805 120 L840 100 L875 115" />
          <path d="M925 55 L950 35 L980 78" />
          <path d="M980 78 L1005 60 L1020 85" />

          <path d="M1085 135 L1105 105 L1135 120" />
          <path d="M1160 115 L1180 90 L1200 100" />
        </g>

        {/* Colored fine refraction */}
        <g
          fill="none"
          stroke="#22d3ee"
          strokeOpacity="0.10"
          strokeWidth="0.7"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M95 110 L120 88 L150 78" />
          <path d="M500 55 L480 82 L505 110" />
          <path d="M805 120 L840 100 L875 115" />
          <path d="M1085 135 L1105 105 L1135 120" />
        </g>

        <g
          fill="none"
          stroke="#8b5cf6"
          strokeOpacity="0.09"
          strokeWidth="0.7"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M205 38 L225 65 L195 92" />
          <path d="M675 55 L700 35 L735 80" />
          <path d="M925 55 L950 35 L980 78" />
        </g>
      </svg>
    </div>
  );
}

export default PageHeaderIce;