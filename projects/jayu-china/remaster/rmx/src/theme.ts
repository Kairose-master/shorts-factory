import { Easing } from "remotion";

/** 자유중국 리마스터 테마 — 채널 아이덴티티(노이르 네이비 + 앰버 + 옐로) 유지. */
export const theme = {
  colors: {
    bg: "#10131d",
    bg2: "#232838",
    paper: "#f2e9dc",
    ink: "#14110f",
    outline: "#1a1613",
    amber: "#e8a33d",
    yellow: "#ffe400",
    red: "#c8452e",
    steel: "#5b7c99",
    green: "#6ea85c",
    greenText: "#8cc87e",
    dim: "#969aa6",
    skin: "#f6f3ec",
    hair: "#26211c",
    suitD: "#343846",
    suitB: "#4a5c78",
    suitR: "#763c34",
    uniG: "#606654",
    workB: "#5e4e38",
    coatG: "#786a4a",
    shirt: "#ded8ca",
    glow: "rgba(232,163,61,0.45)",
  },
  font: {
    serif: "NotoSerifKR",
    sans: "NotoSansKR",
  },
  ease: {
    out: Easing.bezier(0.16, 1, 0.3, 1),
    inOut: Easing.bezier(0.65, 0, 0.35, 1),
    in: Easing.bezier(0.55, 0, 1, 0.45),
  },
  spring: {
    smooth: { damping: 26, stiffness: 120 },
    snappy: { damping: 20, stiffness: 220 },
    bouncy: { damping: 12, stiffness: 190 },
    heavy: { damping: 30, stiffness: 80 },
  },
} as const;
