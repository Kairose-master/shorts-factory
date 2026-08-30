# 소스 & 라이선스

- **아카이브 아이템**: [Film No. 6889](https://archive.org/details/gov.archives.li.255.s.6889) — U.S. National Archives, *Records of the National Aeronautics and Space Administration, 1903–2006*, FedFlix 디지털화
- **라이선스**: CC0 (Public Domain, `creativecommons.org/publicdomain/zero/1.0`)
- **사용 구간**: 원본 릴(17.6분, uncatalogued footage) 중 974–999초 — 우주왕복선을 태운 보잉 747 셔틀 캐리어 항공기(SCA)가 산악 지형 위를 낮게 비행하다 활주로에 착륙하는 연속 장면
- **정확한 임무/일자**: uncatalogued 릴이라 특정 임무명·촬영일은 메타데이터에 없음 — 제목에 날짜·임무명을 넣지 않았습니다 (인용 없는 주장은 쓰지 않는다는 원칙)

## ⚠️ 오디오 없음

이 릴은 전체 17.6분 구간을 100초 간격으로 볼륨 측정한 결과 **처음부터 끝까지 -77.5dB 수준(사실상 무음)**이었습니다. 지난번 아폴로 11호 발사 클립과 달리 이 National Archives 릴 자체가 무성 필름(원본 마그네틱 오디오 트랙 소실 또는 무성 프린트)이라, 원본 오디오를 살릴 방법이 없습니다.

그래서 이번 렌더는 **무음 상태로 그대로** 냈습니다 — 늡덕후 포맷의 "원본 그대로, 가공 없음" 원칙을 지키려면 이게 맞다고 판단했지만, 짧은 영상에 소리가 전혀 없으면 시청 경험이 약해질 수 있습니다. 원하시면:
1. 이대로 무음 유지
2. 엔진/바람 앰비언스를 합성음(SFX 라이브러리 아님, ffmpeg로 생성하는 순수 합성 노이즈)으로 얕게 깔기
3. `audio-acquisition` 스킬로 무료 SFX 라이브러리에서 실제 제트엔진 음원을 찾아 합성

중 어느 쪽을 원하시는지 알려주시면 반영하겠습니다.
