# AI Journalist

AI-Powered Article Generator: Collects and analyzes the latest news to craft high-quality articles autonomously.

AI 기반 자동 기사 생성 시스템: 최신 뉴스를 수집하고 분석하여 고품질의 기사를 작성합니다.

## What we want to know

- 기존 기사 데이터를 바탕으로 새로운 기사를 생성할 수 있는가
- Cost effective 하면서도 높은 품질의 기사를 생성할 수 있는가

## Pipeline

1. 필요한 라이브러리 설치 및 API 키 설정
2. 주제 설정 ("아이폰 16 출시 및 스펙")
3. AI(Claude)를 사용해 주제와 관련된 5개의 검색어 생성 (Claude 3 Haiku)
4. 생성된 검색어로 Google 뉴스 검색 수행 (SerpAPI)
5. 각 검색 결과에서 AI가 가장 관련성 높은 기사 선택 (Claude 3 Haiku)
6. 선택된 기사들의 본문 내용 추출
7. 추출된 내용을 바탕으로 AI가 한국어로 NYT 스타일의 기사 작성 (Claude 3.5 Sonnet)

## API Usage while development

Total cost: $0.3464 (461.29 South Korean won)

Claude 3 Haiku
- Input: $0.0049 (0.019 Million Input Tokens)
- Output: $0.0015 (0.001 Million Output Tokens)

Claude 3.5 Sonnet
- Input: $0.21 (0.071 Million Input Tokens) 
- Output: $0.13 (0.008 Million Output Tokens)

### Reference

- https://github.com/mshumer/ai-journalist
- YouTube [빵형의 개발도상국](https://www.youtube.com/@bbanghyong)
- 폰트 [빛의계승자체](https://noonnu.cc/font_page/442)


