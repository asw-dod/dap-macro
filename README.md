# Dap Macro 어떻게 동작하나요?

Github에 코드를 작성 한 뒤, Tag 정보를 달게 된다면 Github Action에서 이벤트가 발생하여 도커 빌드를 한 뒤, 도커 허브에 이미지를 푸시 하게 됩니다.

# 어떻게 사용하나요?

```sh
$ docker run -e DEU_ID_CHACHA=[동의대학교 아이디] \
             -e DEU_PW_CHACHA=[동의대학교 비밀번호] \
             -e GITHUB_TOKEN=[깃허브 토큰, 이슈 출력] \
             -e REPO_NAME=[깃허브 레포, 이슈 출력] \
             -e ORG_NAME=[깃허브 관리, 이슈 출력] \
             aoikazto/load-dap:latest
```

# 언제 이슈가 갱신이 되나요?

UTC 시간 기준 매일 1시, 9시에 갱신이 됩니다. 한국 시간 기준으로 10시, 18시에 갱신이 됩니다.

# 어떻게 정보를 가져오나요?

아래의 API를 통해 접근 하시면 됩니다.
> https://api.github.com/repos/asw-dod/dap-macro/issues


# Github Action 처리 근황

[![Docker Image CI](https://github.com/asw-dod/dap-macro/actions/workflows/docker-image.yml/badge.svg)](https://github.com/asw-dod/dap-macro/actions/workflows/docker-image.yml) [![Docker Run](https://github.com/asw-dod/dap-macro/actions/workflows/docker.yml/badge.svg)](https://github.com/asw-dod/dap-macro/actions/workflows/docker.yml)
