# longform2shorts

롱폼 → 숏폼 자동 편집 도구. 핵심 설계 = **말 밀도 최대화**: 발화 블록 사이의
모든 무음(> `--max-gap`)을 점프컷해 "말이 끊기지 않는" 숏폼을 만든다.

## 파이프라인

전사(faster-whisper, 로컬·무API·단어 타임스탬프) → 무음 점프컷 → 하이라이트
스코어링(발화 밀도 최우선 + 숫자·질문·훅 어휘) → 비중복 창 선택 → 렌더
(세로 1080×1920 블러 확장 배경, 구간별 verbatim 자막 PNG 오버레이, loudnorm -14).

```bash
pip install faster-whisper imageio-ffmpeg pillow numpy
python3 tools/longform2shorts/l2s.py --input long.mp4 --outdir out/ \
    --clips 2 --target 30 --max-gap 0.4 --model small
```

`out/report.json`에 클립별 원본 구간·점수·전체 전사가 남는다 — 자막은 전사
원문 그대로이며 지어내는 문장이 없다.

## 실적용 검증 (projects/l2s-demo/)

Handsel 델리게이트 데모(2:05, 영어 내레이션, 사용자 본인 저작물):
- 전사 200단어 → 발화 블록 18개, 원본 발화 밀도 **58%**
- 산출: short_1 (28.0s, 원본 24–68s에서 6블록 점프컷) · short_2 (19.2s, 80–119s)
- 산출물 발화 밀도 **100%** — 무음 0

## 디자인 결정의 근거

- 블러 확장 세로 배경: 9채널 썸네일 실측 관행 (kr 리서치 reference-board)
- 자막 스타일(흰 고딕+먹 스트로크, ≤2줄): 당몰이/제로비 실측
- 하이라이트 점수에서 발화 밀도가 최우선 가중: "말이 많아야 한다"는 운영 원칙의 도구화

## 한계

- 화자 얼굴 추적 크롭 없음(중앙 고정) — 화면 녹화·단일 구도 소스에 최적
- 단일 패스 loudnorm이라 짧은 클립에서 -14±1.5dB 오차
- 한국어 전사 품질은 whisper small 기준 — 고유명사 오인식 가능, `--model medium` 권장
