import "./BackfillIceTexture.css";

export function BackfillIceTexture() {
  return (
    <div className="backfill-ice-texture" aria-hidden="true">
      <svg
        className="backfill-ice-texture-svg"
        viewBox="0 0 900 520"
        preserveAspectRatio="none"
      >
        <defs>
          <linearGradient
            id="backfill-fragment-a"
            x1="0%"
            y1="100%"
            x2="100%"
            y2="0%"
          >
            <stop offset="0%" stopColor="#08171d" stopOpacity="0.58" />
            <stop offset="100%" stopColor="#182d36" stopOpacity="0.16" />
          </linearGradient>

          <linearGradient
            id="backfill-fragment-b"
            x1="100%"
            y1="100%"
            x2="0%"
            y2="0%"
          >
            <stop offset="0%" stopColor="#0b1d24" stopOpacity="0.52" />
            <stop offset="100%" stopColor="#203943" stopOpacity="0.12" />
          </linearGradient>
        </defs>

        {/* Bottom-left cluster */}

        <g>
          <polygon
            points="0,520 0,430 82,378 126,455 76,520"
            fill="url(#backfill-fragment-a)"
          />

          <polygon
            points="42,405 118,340 178,394 126,455"
            fill="#0b1d24"
            fillOpacity="0.46"
          />

          <polygon
            points="86,520 126,455 202,482 248,520"
            fill="#07161c"
            fillOpacity="0.56"
          />

          <polygon
            points="118,340 172,278 238,346 178,394"
            fill="url(#backfill-fragment-b)"
          />

          <polygon
            points="172,278 252,310 238,346"
            fill="#29434d"
            fillOpacity="0.22"
          />

          <polygon
            points="178,394 238,346 318,414 248,520 202,482"
            fill="#0d222a"
            fillOpacity="0.48"
          />

          <polygon
            points="252,310 318,242 374,320 318,414 238,346"
            fill="url(#backfill-fragment-a)"
          />

          <polygon
            points="318,242 390,286 374,320"
            fill="#29434d"
            fillOpacity="0.22"
          />

          <polygon
            points="318,414 374,320 452,382 418,470"
            fill="#0a1c23"
            fillOpacity="0.46"
          />

          <polygon
            points="374,320 452,264 518,330 452,382"
            fill="url(#backfill-fragment-b)"
          />

          <polygon
            points="452,264 536,222 518,330"
            fill="#213b45"
            fillOpacity="0.24"
          />

          <polygon
            points="418,470 452,382 526,414 500,500"
            fill="#0c2028"
            fillOpacity="0.44"
          />
        </g>

        {/* Medium fragments */}

        <g>
          <polygon
            points="0,390 28,348 62,372 42,405"
            fill="#29434d"
            fillOpacity="0.22"
          />

          <polygon
            points="28,348 76,330 82,378 62,372"
            fill="#0a1b22"
            fillOpacity="0.44"
          />

          <polygon
            points="76,330 118,340 82,378"
            fill="#29434d"
            fillOpacity="0.19"
          />

          <polygon
            points="132,300 158,250 190,270 172,278"
            fill="#172f38"
            fillOpacity="0.30"
          />

          <polygon
            points="158,250 208,230 238,270 190,270"
            fill="#091a21"
            fillOpacity="0.43"
          />

          <polygon
            points="202,390 238,346 270,375 248,420"
            fill="#29434d"
            fillOpacity="0.18"
          />

          <polygon
            points="238,346 292,360 270,375"
            fill="#0c2028"
            fillOpacity="0.40"
          />

          <polygon
            points="280,220 318,242 300,275 260,258"
            fill="#203b45"
            fillOpacity="0.21"
          />

          <polygon
            points="318,242 350,198 374,240 350,280"
            fill="#0a1b22"
            fillOpacity="0.42"
          />

          <polygon
            points="360,355 374,320 414,338 398,370"
            fill="#29434d"
            fillOpacity="0.17"
          />

          <polygon
            points="414,338 452,382 398,370"
            fill="#0a1c23"
            fillOpacity="0.39"
          />

          <polygon
            points="430,238 452,264 438,300 404,276"
            fill="#172f38"
            fillOpacity="0.24"
          />

          <polygon
            points="452,264 490,250 518,285 488,310"
            fill="#0c2028"
            fillOpacity="0.38"
          />

          <polygon
            points="510,330 518,330 548,294 568,328 526,360"
            fill="#213b45"
            fillOpacity="0.16"
          />
        </g>

        {/* Small scattered fragments */}

        <g>
          <polygon
            points="52,310 74,286 91,304 76,330"
            fill="#29434d"
            fillOpacity="0.17"
          />

          <polygon
            points="92,268 115,244 130,272 110,286"
            fill="#172f38"
            fillOpacity="0.23"
          />

          <polygon
            points="148,220 170,205 190,225 174,244"
            fill="#29434d"
            fillOpacity="0.15"
          />

          <polygon
            points="214,185 246,166 254,196 232,210"
            fill="#0c2028"
            fillOpacity="0.27"
          />

          <polygon
            points="270,292 288,268 310,284 300,305"
            fill="#29434d"
            fillOpacity="0.15"
          />

          <polygon
            points="330,185 350,166 374,182 358,204"
            fill="#172f38"
            fillOpacity="0.22"
          />

          <polygon
            points="398,220 420,198 442,218 428,238"
            fill="#29434d"
            fillOpacity="0.14"
          />

          <polygon
            points="468,180 494,158 512,184 492,202"
            fill="#0c2028"
            fillOpacity="0.24"
          />

          <polygon
            points="530,245 552,224 574,246 550,262"
            fill="#29434d"
            fillOpacity="0.13"
          />

          <polygon
            points="585,205 610,186 628,210 604,226"
            fill="#172f38"
            fillOpacity="0.20"
          />
        </g>

        {/* Main fractures */}

        <g
          fill="none"
          stroke="var(--backfill-ice-primary)"
          strokeOpacity="0.38"
          strokeWidth="1.1"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M0 430 L82 378 L42 405 L118 340" />
          <path d="M82 378 L126 455 L178 394 L238 346" />
          <path d="M118 340 L172 278 L158 250" />

          <path d="M172 278 L238 346 L318 242" />
          <path d="M238 346 L318 414 L374 320" />
          <path d="M252 310 L300 275 L318 242" />

          <path d="M318 242 L350 198 L374 240 L390 286" />
          <path d="M374 320 L452 264 L452 382" />
          <path d="M452 264 L518 330 L536 222" />

          <path d="M452 382 L418 470 L526 414" />
          <path d="M518 330 L548 294 L568 328" />

          <path d="M76 330 L52 310 L74 286" />
          <path d="M208 230 L214 185 L246 166" />
          <path d="M350 166 L330 185 L350 198" />
          <path d="M420 198 L398 220 L430 238" />
          <path d="M494 158 L468 180 L492 202" />
        </g>

        {/* Fine fractures */}

        <g
          fill="none"
          stroke="var(--backfill-ice-secondary)"
          strokeOpacity="0.28"
          strokeWidth="0.75"
          strokeLinecap="round"
        >
          <path d="M28 348 L52 310 L76 330" />
          <path d="M74 286 L92 268 L115 286" />
          <path d="M126 455 L110 420 L132 390" />

          <path d="M158 250 L148 220 L170 205" />
          <path d="M190 270 L214 245 L208 230" />

          <path d="M202 390 L232 410 L248 420" />
          <path d="M270 375 L292 360 L318 414" />

          <path d="M280 220 L300 275 L288 292" />
          <path d="M350 198 L330 185 L350 166" />

          <path d="M360 355 L398 370 L414 338" />
          <path d="M404 276 L430 238 L438 300" />

          <path d="M488 310 L510 330 L500 360" />
          <path d="M530 245 L548 294 L552 224" />

          <path d="M526 414 L568 328 L585 300" />
        </g>
      </svg>
    </div>
  );
}

export function BackfillIceTextureTopRight() {
  return (
    <div className="backfill-ice-texture-top-right" aria-hidden="true">
      <svg
        className="backfill-ice-texture-top-right-svg"
        viewBox="0 0 900 520"
        preserveAspectRatio="none"
      >
        <defs>
          <linearGradient
            id="backfill-top-fragment-a"
            x1="100%"
            y1="0%"
            x2="20%"
            y2="100%"
          >
            <stop offset="0%" stopColor="#07161c" stopOpacity="0.62" />
            <stop offset="100%" stopColor="#1a3039" stopOpacity="0.12" />
          </linearGradient>

          <linearGradient
            id="backfill-top-fragment-b"
            x1="0%"
            y1="0%"
            x2="100%"
            y2="100%"
          >
            <stop offset="0%" stopColor="#0a1b22" stopOpacity="0.58" />
            <stop offset="100%" stopColor="#29434d" stopOpacity="0.10" />
          </linearGradient>
        </defs>

        {/* Top-right cluster */}

        <g>
          <polygon
            points="900,0 900,82 842,116 790,78 814,0"
            fill="url(#backfill-top-fragment-a)"
          />

          <polygon
            points="822,0 814,72 752,108 716,58 738,0"
            fill="#08181f"
            fillOpacity="0.52"
          />

          <polygon
            points="900,72 842,116 868,172 900,192"
            fill="#0b1d24"
            fillOpacity="0.48"
          />

          <polygon
            points="790,78 842,116 800,168 742,138 752,108"
            fill="#172f38"
            fillOpacity="0.42"
          />

          <polygon
            points="716,58 752,108 712,150 666,116 682,70"
            fill="url(#backfill-top-fragment-b)"
          />

          <polygon
            points="842,116 800,168 826,226 882,210 868,172"
            fill="#0a1b22"
            fillOpacity="0.50"
          />

          <polygon
            points="742,138 800,168 770,224 706,204 682,166"
            fill="#0c2028"
            fillOpacity="0.46"
          />

          <polygon
            points="666,116 712,150 682,210 620,184 624,138"
            fill="#203b45"
            fillOpacity="0.30"
          />

          <polygon
            points="900,192 882,210 858,278 900,302"
            fill="#08181f"
            fillOpacity="0.52"
          />

          <polygon
            points="826,226 770,224 734,278 782,318 842,294"
            fill="url(#backfill-top-fragment-a)"
          />

          <polygon
            points="706,204 770,224 734,278 672,254 658,218"
            fill="#0d222a"
            fillOpacity="0.48"
          />

          <polygon
            points="620,184 682,210 658,270 602,246 586,210"
            fill="#172f38"
            fillOpacity="0.40"
          />

          <polygon
            points="858,278 842,294 806,362 854,390 900,348 900,302"
            fill="#0b1d24"
            fillOpacity="0.50"
          />

          <polygon
            points="782,318 734,278 680,310 692,374 754,390 806,362"
            fill="#0a1c23"
            fillOpacity="0.48"
          />

          <polygon
            points="672,254 734,278 680,310 624,292 602,246"
            fill="url(#backfill-top-fragment-b)"
          />

          <polygon
            points="586,210 602,246 558,286 520,254 538,218"
            fill="#0c2028"
            fillOpacity="0.44"
          />

          <polygon
            points="624,292 680,310 692,374 628,392 590,348"
            fill="#203b45"
            fillOpacity="0.32"
          />

          <polygon
            points="754,390 806,362 854,390 824,448 764,444"
            fill="#0b1d24"
            fillOpacity="0.46"
          />

          <polygon
            points="692,374 754,390 764,444 710,470 674,424"
            fill="#0d222a"
            fillOpacity="0.43"
          />

          <polygon
            points="590,348 628,392 600,454 542,430 528,378"
            fill="#172f38"
            fillOpacity="0.37"
          />

          <polygon
            points="528,378 542,430 500,474 458,438 476,390"
            fill="#0a1b22"
            fillOpacity="0.42"
          />

          <polygon
            points="710,470 764,444 786,490 742,520 676,520 674,488"
            fill="url(#backfill-top-fragment-a)"
          />
        </g>

        {/* Detached fragments */}

        <g>
          <polygon
            points="680,42 704,18 728,34 712,64"
            fill="#29434d"
            fillOpacity="0.18"
          />

          <polygon
            points="770,150 792,126 816,142 800,168"
            fill="#29434d"
            fillOpacity="0.17"
          />

          <polygon
            points="620,82 648,58 666,82 648,106"
            fill="#172f38"
            fillOpacity="0.22"
          />

          <polygon
            points="858,238 878,218 894,244 882,266"
            fill="#29434d"
            fillOpacity="0.16"
          />

          <polygon
            points="548,150 574,130 592,154 570,174"
            fill="#203b45"
            fillOpacity="0.18"
          />

          <polygon
            points="520,310 546,288 568,310 548,332"
            fill="#29434d"
            fillOpacity="0.17"
          />

          <polygon
            points="458,344 484,322 502,348 480,370"
            fill="#172f38"
            fillOpacity="0.19"
          />

          <polygon
            points="610,438 634,416 654,440 632,460"
            fill="#29434d"
            fillOpacity="0.15"
          />

          <polygon
            points="820,454 846,430 870,454 848,478"
            fill="#203b45"
            fillOpacity="0.16"
          />
        </g>

        {/* Main fractures */}

        <g
          fill="none"
          stroke="var(--backfill-ice-primary)"
          strokeOpacity="0.40"
          strokeWidth="1.1"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M900 82 L842 116 L800 168 L826 226" />
          <path d="M814 72 L790 78 L752 108 L742 138" />
          <path d="M752 108 L712 150 L682 210" />

          <path d="M800 168 L770 224 L734 278" />
          <path d="M682 210 L658 270 L672 254" />
          <path d="M602 246 L658 270 L624 292" />

          <path d="M882 210 L858 278 L842 294" />
          <path d="M734 278 L680 310 L692 374" />
          <path d="M672 254 L624 292 L590 348" />

          <path d="M680 310 L628 392 L600 454" />
          <path d="M692 374 L754 390 L764 444" />
          <path d="M806 362 L754 390 L824 448" />

          <path d="M542 430 L500 474 L458 438" />
          <path d="M600 454 L542 430 L528 378" />
          <path d="M764 444 L742 520 L710 470" />
        </g>

        {/* Fine fractures */}

        <g
          fill="none"
          stroke="var(--backfill-ice-secondary)"
          strokeOpacity="0.30"
          strokeWidth="0.75"
          strokeLinecap="round"
        >
          <path d="M704 18 L680 42 L666 82" />
          <path d="M648 58 L620 82 L624 138" />
          <path d="M792 126 L770 150 L770 224" />

          <path d="M878 218 L858 238 L858 278" />
          <path d="M574 130 L548 150 L538 218" />

          <path d="M546 288 L520 310 L528 378" />
          <path d="M484 322 L458 344 L476 390" />

          <path d="M634 416 L610 438 L600 454" />
          <path d="M846 430 L820 454 L824 448" />

          <path d="M624 184 L602 246 L586 210" />
          <path d="M706 204 L672 254 L680 310" />

          <path d="M782 318 L754 390 L692 374" />
          <path d="M854 390 L824 448 L786 490" />
        </g>
      </svg>
    </div>
  );
}