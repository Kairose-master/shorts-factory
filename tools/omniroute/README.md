# OmniRoute 로컬 게이트웨이

설치·검증 완료 (v3.8.49, `npm i -g omniroute`). 이 컨테이너에서 기동 확인:

```
omniroute            # 대시보드 http://localhost:20128 · API http://localhost:20128/v1
curl --noproxy localhost http://localhost:20128/v1/models   # auto/best-coding 등 콤보 모델 확인
```

## 용도와 한계 (정직 노트)

- **이 원격 세션의 토큰은 못 줄인다.** 세션의 모델 호출은 하네스가 관리하며 로컬
  게이트웨이를 거치지 않는다. 컨테이너도 세션 종료 시 사라지므로 여기 설치는
  검증·문서화 목적이다.
- **로컬 Claude Code CLI에서 쓰는 법**: `npm i -g omniroute` 후 settings.json에
  `ANTHROPIC_BASE_URL=http://localhost:20128` — 요청이 무료/저가 프로바이더로
  라우팅되고 RTK+Caveman 압축이 걸린다.
- **권장 전략**: 대본·검수 등 창작 판정은 본 모델 유지, 기계적 반복작업만 우회.
  대화·코드가 제3자 프로바이더로 나간다는 점(프라이버시)을 감안할 것.
- Handsel 오피스 에이전트는 Handsel 클라우드에서 실행되므로 이 로컬 게이트웨이와
  무관하다 (오피스의 MCP 와이어링은 Exa 등 공개 Streamable HTTP 서버 사용).
