# SOP — 수집과 자막 확보

수집가의 공정. 채널에서 새 설교를 감지해 `sermons/<id>/`를 만든다.
비용이 드는 유일한 상시 공정이므로 규칙이 엄격하다.

## 비용

| 동작 | 호출 | credits |
|---|---|---|
| 신규 감지 (`channel-videos`, 30편) | 1 | 1 |
| 설교 1편 자막 | 1 | 1 |
| 댓글 1편 | 1 | 1 |

**설교 30편을 한 번에 수집하면 31 credits.** 헌장 자율경계 3번에 따라
예상 호출 수를 먼저 말한다. `sermon_ingest.py`는 기본이 dry-run이며,
`--fetch` 없이는 과금 호출을 하지 않는다.

## 실행

```bash
# 무과금: 무엇을 가져올지만 보여준다
python3 scripts/sermon_ingest.py --list

# 신규 감지 후 자막까지 (1 + N credits)
python3 scripts/sermon_ingest.py --fetch --limit 3

# 특정 영상 하나
python3 scripts/sermon_ingest.py --fetch --video Y1ABPz8B7kw
```

## 엔드포인트 주의

`scrapecreators-api` 스킬의 라우팅 표는 채널 영상 목록을
`/v1/youtube/channel/videos`로 적고 있으나 **실제 경로는
`/v1/youtube/channel-videos`** 이다(2026-08-29 실측, 전자는 404).
스킬 파일은 upstream 바이트 동일성 유지 대상이라 고치지 않는다.
`sermon_ingest.py`가 올바른 경로를 쓴다.

## 산출물

```
sermons/<sermon-id>/
├── meta.json        파싱된 제목 필드 + 조회수 + 길이 + 설교 시작 추정
├── transcript.json  타임스탬프 자막 원본 (gitignore 대상)
├── summary.md       요약가 산출
└── logic-map.md     논증분석가 산출
```

sermon-id 규약: `S-YYYYMMDD-<slug>` — 예 `S-20260828-EZK47`.
날짜는 **설교 날짜**(제목에 적힌 것)이지 업로드 날짜가 아니다.

## 제목 파싱

`sermon_ingest.py`의 파서가 날짜·본문·예배종류·설교자·제목을 뽑는다.
실측 60개 제목에 대한 회귀 테스트가 스크립트 안에 있다
(`python3 scripts/sermon_ingest.py --selftest`).

**미지의 형태는 `service_type: 기타`로 떨어진다.** 조용히 틀리는 것보다
분류를 포기하는 편이 낫다. `기타`가 늘어나면 제목 규약이 바뀐 것이니
파서를 고친다.

## 설교 시작 지점 추정

새벽기도 영상은 앞 약 5분이 찬송과 기도다(`../research/channel-model.md` §6).
추정 규칙:

1. 분당 `[노래]`/`[음악]`/`[박수]` 마커 밀도를 센다
2. 마커 밀도가 0으로 떨어진 뒤 처음 나오는 봉독 신호
   (`말씀입니다`, `절까지`, `아멘`) 지점을 후보로 잡는다
3. 후보가 없으면 마커가 끝난 지점 + 60초

**결과는 언제나 `sermon_start_ms_estimated`로 기록한다.** 확정값이 아니다.
요약가는 이 값 이전 구간을 읽지 않는다.

## 수집가가 하지 않는 것

- **자막을 고치지 않는다.** ASR 오류를 발견해도 `transcript.json`은 원본 그대로
  둔다. 교정은 QUOTE 승격 시점에 사람이 음성을 듣고 한다.
- **요약하지 않는다.** 요약가의 일이다.
- **댓글을 자동 수집하지 않는다.** 별도 승인이 있을 때만.
