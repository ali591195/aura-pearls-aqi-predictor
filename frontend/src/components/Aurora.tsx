import {
  useEffect,
  useState,
} from "react";
import "./Aurora.css";

const AURORA_HEIGHT = 1000;

function AuroraWave() {
  return (
    <svg
      className="aurora-svg"
      viewBox="0 0 1600 1000"
      preserveAspectRatio="none"
    >
      <defs>
        <filter
          id="aurora-blur"
          x="-50%"
          y="-50%"
          width="200%"
          height="200%"
        >
          <feGaussianBlur stdDeviation="27" />
        </filter>
        <linearGradient
          id="green-gradient"
          x1="0%"
          y1="0%"
          x2="100%"
          y2="100%"
        >
          <stop
            offset="0%"
            stopColor="#10ea94"
            stopOpacity="0.5"
          />
          <stop
            offset="100%"
            stopColor="#34d399"
            stopOpacity="0.35"
          />
        </linearGradient>
        <linearGradient
          id="violet-gradient"
          x1="100%"
          y1="0%"
          x2="0%"
          y2="100%"
        >
          <stop
            offset="0%"
            stopColor="#8b5cf6"
            stopOpacity="0.38"
          />
          <stop
            offset="100%"
            stopColor="#8b5cf6"
            stopOpacity="0.2"
          />
        </linearGradient>
        <linearGradient
          id="cyan-gradient"
          x1="0%"
          y1="0%"
          x2="100%"
          y2="0%"
        >
          <stop
            offset="0%"
            stopColor="#22d3ee"
            stopOpacity="0.42"
          />
          <stop
            offset="50%"
            stopColor="#22d3ee"
            stopOpacity="0.32"
          />
          <stop
            offset="100%"
            stopColor="#22d3ee"
            stopOpacity="0.2"
          />
        </linearGradient>
        <linearGradient
          id="magenta-gradient"
          x1="0%"
          y1="100%"
          x2="100%"
          y2="0%"
        >
          <stop
            offset="0%"
            stopColor="#f472b6"
            stopOpacity="0.2"
          />
          <stop
            offset="100%"
            stopColor="#f472b6"
            stopOpacity="0.08"
          />
        </linearGradient>
      </defs>
      <g className="aurora-whole">
        <g
          className="aurora-waves"
          filter="url(#aurora-blur)"
        >
          <path
            className="aurora-wave aurora-wave-green"
            fill="url(#green-gradient)"
            d="M-500 -80
               C-150 180, 120 -40, 450 130
               C760 300, 980 40, 1260 180
               C1530 320, 1780 80, 2100 220
               L2100 520
               C1770 400, 1530 570, 1240 430
               C950 290, 720 550, 430 400
               C130 250, -170 470, -500 330 Z"
          />
          <path
            className="aurora-wave aurora-wave-emerald"
            fill="url(#green-gradient)"
            d="M-500 100
               C-160 340, 120 100, 450 290
               C760 470, 970 180, 1260 340
               C1530 490, 1780 220, 2100 370
               L2100 680
               C1780 550, 1510 730, 1230 590
               C940 440, 720 700, 420 560
               C100 400, -180 620, -500 470 Z"
          />
          <path
            className="aurora-wave aurora-wave-cyan"
            fill="url(#cyan-gradient)"
            d="M-500 290
               C-150 520, 120 290, 440 470
               C750 640, 970 370, 1250 520
               C1530 680, 1780 400, 2100 550
               L2100 900
               C1780 720, 1510 900, 1220 770
               C930 630, 700 880, 410 740
               C100 600, -180 800, -500 690 Z"
          />
          <path
            className="aurora-wave aurora-wave-violet"
            fill="url(#violet-gradient)"
            d="M-500 470
               C-150 700, 120 470, 430 650
               C730 820, 960 550, 1240 700
               C1530 850, 1780 580, 2100 730
               L2100 1030
               C1780 900, 1510 1080, 1220 950
               C930 810, 700 1050, 410 920
               C100 780, -180 1000, -500 840 Z"
          />
          <path
            className="aurora-wave aurora-wave-magenta"
            fill="url(#magenta-gradient)"
            d="M-500 650
               C-150 860, 120 650, 420 820
               C710 970, 940 730, 1220 870
               C1510 1010, 1780 760, 2100 900
               L2100 1200
               C1770 1080, 1500 1200, 1190 1090
               C900 980, 680 1150, 390 1020
               C100 900, -180 1120, -500 970 Z"
          />
        </g>
      </g>
    </svg>
  );
}

function Aurora() {
  const [auroraCount, setAuroraCount] = useState(1);

  useEffect(() => {
    function updateAuroraCount() {
      const documentHeight =
        document.documentElement.scrollHeight;
      const count = Math.max(
        1,
        Math.ceil(documentHeight / AURORA_HEIGHT),
      );
      setAuroraCount(count);
    }
    updateAuroraCount();
    const resizeObserver =
      new ResizeObserver(updateAuroraCount);
    resizeObserver.observe(
      document.documentElement,
    );
    window.addEventListener(
      "resize",
      updateAuroraCount,
    );
    return () => {
      resizeObserver.disconnect();
      window.removeEventListener(
        "resize",
        updateAuroraCount,
      );
    };
  }, []);

  return (
    <div className="aurora" aria-hidden="true">
      <div
        className="aurora-background"
        style={{
          height: `${auroraCount * AURORA_HEIGHT}px`,
        }}
      >
        {Array.from(
          { length: auroraCount },
          (_, index) => (
            <div
              className={`aurora-instance${
                index % 2 === 1
                  ? " aurora-instance-flipped"
                  : ""
              }`}
              key={index}
            >
              <AuroraWave />
            </div>
          ),
        )}
      </div>
    </div>
  );
}

export default Aurora;