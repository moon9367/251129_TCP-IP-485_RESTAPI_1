# 🌐 Cloudflare Tunnel + Netlify 배포 가이드

## 📋 목차
1. [Cloudflare Tunnel이 필요한 이유](#why)
2. [Cloudflare Tunnel 설치](#install)
3. [REST API 서버 + Tunnel 실행](#run)
4. [Netlify 배포](#netlify)
5. [문제 해결](#troubleshooting)

---

## 🤔 Cloudflare Tunnel이 필요한 이유 {#why}

### HTTPS Mixed Content 문제

```
❌ Netlify (HTTPS) → REST API (HTTP) = 차단됨!
✅ Netlify (HTTPS) → Cloudflare Tunnel (HTTPS) = 작동!
```

**문제:**
- Netlify는 **HTTPS**로 프론트엔드를 배포합니다
- 로컬 REST API는 **HTTP**입니다
- HTTPS 페이지에서 HTTP API를 호출하면 브라우저가 **Mixed Content**로 차단합니다

**해결:**
- **Cloudflare Tunnel**을 사용하면 로컬 HTTP를 **HTTPS**로 노출할 수 있습니다
- 무료이며 설치도 간단합니다

---

## 📥 Cloudflare Tunnel 설치 {#install}

### 방법 1: cloudflared 다운로드 (권장)

1. **다운로드 페이지 방문:**
   ```
   https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
   ```

2. **Windows 버전 다운로드:**
   - `cloudflared-windows-amd64.exe` 다운로드
   - 파일명을 `cloudflared.exe`로 변경
   - 프로젝트 폴더에 복사

3. **설치 확인:**
   ```cmd
   cloudflared --version
   ```

### 방법 2: NPX 사용 (Node.js 필요)

```bash
npx cloudflared tunnel --url http://localhost:8000
```

---

## 🚀 REST API 서버 + Tunnel 실행 {#run}

### Step 1: REST API 서버 실행

**터미널 1번:**
```cmd
start_api_server.bat
```

**확인:**
```
✅ http://localhost:8000/docs 접속 가능
```

### Step 2: Cloudflare Tunnel 실행

**터미널 2번:**
```cmd
start_cloudflare_tunnel.bat
```

**출력 예시:**
```
+--------------------------------------------------------------------------------------------+
|  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable): |
|  https://abc-123-xyz.trycloudflare.com                                                    |
+--------------------------------------------------------------------------------------------+
```

**⚠️ 중요:**
- 위의 URL(`https://abc-123-xyz.trycloudflare.com`)을 복사하세요!
- 이 URL은 **터널이 실행될 때마다 변경됩니다**

### Step 3: API Config 업데이트

**`web_ui/api-config.js` 파일 수정:**
```javascript
const API_CONFIG = {
  // Cloudflare Tunnel URL로 변경
  BASE_URL: 'https://abc-123-xyz.trycloudflare.com',  // 👈 여기!
  
  ENDPOINTS: {
    // ... (나머지 동일)
  }
};
```

### Step 4: 테스트

**브라우저에서 확인:**
```
https://abc-123-xyz.trycloudflare.com/docs
```

**API 호출 테스트:**
```bash
curl https://abc-123-xyz.trycloudflare.com/health
```

**예상 결과:**
```json
{
  "status": "healthy",
  "modbus": "connected",
  "timestamp": "2024-12-09"
}
```

---

## 🌍 Netlify 배포 {#netlify}

### Step 1: GitHub 저장소 준비

**프로젝트 구조:**
```
project/
├── web_ui/              # 👈 프론트엔드 파일들
│   ├── index.html
│   ├── api-config.js    # 👈 Cloudflare Tunnel URL 설정 필수
│   ├── api-client.js
│   ├── data-manager.js
│   ├── script.js
│   └── styles.css
├── rest_api_server.py   # 로컬에서만 실행
└── start_api_server.bat # 로컬에서만 실행
```

**GitHub에 업로드:**
```bash
git init
git add web_ui/
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

### Step 2: Netlify 배포

1. **Netlify 가입:**
   ```
   https://app.netlify.com/signup
   ```

2. **New site from Git 클릭**

3. **GitHub 저장소 선택**

4. **Build settings 설정:**
   ```
   Base directory: web_ui
   Build command: (비워두기)
   Publish directory: .
   ```

5. **Deploy site 클릭**

6. **배포 완료!**
   ```
   https://your-app-name.netlify.app
   ```

### Step 3: Cloudflare Tunnel URL 업데이트

**⚠️ 중요: Netlify 배포 전에 반드시 수정!**

**`web_ui/api-config.js`:**
```javascript
const API_CONFIG = {
  // Cloudflare Tunnel URL로 설정
  BASE_URL: 'https://abc-123-xyz.trycloudflare.com',  // 👈 실제 Tunnel URL
  
  ENDPOINTS: {
    // ... (나머지 동일)
  }
};
```

**변경 후 GitHub에 푸시:**
```bash
cd web_ui
git add api-config.js
git commit -m "Update API URL to Cloudflare Tunnel"
git push
```

**Netlify가 자동으로 재배포합니다! 🎉**

---

## 🎯 전체 작업 흐름

```
1️⃣ 로컬 개발 (테스트)
   ├─ start_api_server.bat 실행
   ├─ api-config.js: BASE_URL = 'http://localhost:8000'
   └─ index.html을 브라우저에서 열기

2️⃣ Cloudflare Tunnel 설정
   ├─ start_api_server.bat 실행 (터미널 1)
   ├─ start_cloudflare_tunnel.bat 실행 (터미널 2)
   ├─ Tunnel URL 복사: https://abc-123-xyz.trycloudflare.com
   └─ api-config.js: BASE_URL을 Tunnel URL로 변경

3️⃣ Netlify 배포
   ├─ web_ui/ 폴더를 GitHub에 푸시
   ├─ Netlify에서 GitHub 저장소 연결
   ├─ Base directory: web_ui
   └─ 배포 완료: https://your-app.netlify.app

4️⃣ 최종 확인
   ├─ 로컬에서 REST API + Tunnel 실행 유지
   ├─ Netlify 사이트 방문: https://your-app.netlify.app
   └─ 센서 데이터가 정상적으로 표시되는지 확인
```

---

## 🛠️ 문제 해결 {#troubleshooting}

### ❌ Mixed Content 에러

**증상:**
```
Mixed Content: The page at 'https://your-app.netlify.app' was loaded over HTTPS,
but requested an insecure XMLHttpRequest endpoint 'http://localhost:8000/api/...'
```

**원인:**
- `api-config.js`에서 `BASE_URL`이 여전히 `http://localhost:8000`

**해결:**
```javascript
// ❌ 잘못된 설정
BASE_URL: 'http://localhost:8000',

// ✅ 올바른 설정
BASE_URL: 'https://abc-123-xyz.trycloudflare.com',
```

---

### ❌ Cloudflare Tunnel이 작동하지 않음

**증상:**
```
cloudflared: command not found
```

**해결:**
1. `cloudflared.exe`가 프로젝트 폴더에 있는지 확인
2. 또는 NPX 사용: `npx cloudflared tunnel --url http://localhost:8000`

---

### ❌ Netlify에서 API 호출 실패

**증상:**
- 브라우저 콘솔: `Failed to fetch`, `ERR_CONNECTION_REFUSED`

**원인:**
1. Cloudflare Tunnel이 실행되지 않았음
2. Tunnel URL이 잘못되었음
3. Modbus 서버가 실행되지 않았음

**해결:**
1. **로컬에서 확인:**
   ```bash
   # REST API 서버 실행 확인
   curl http://localhost:8000/health
   
   # Cloudflare Tunnel 확인
   curl https://abc-123-xyz.trycloudflare.com/health
   ```

2. **둘 다 정상이면:**
   - `api-config.js`의 `BASE_URL` 확인
   - 브라우저 개발자 도구 → Network 탭에서 실제 호출 URL 확인

---

### ❌ Tunnel URL이 자주 변경됨

**원인:**
- 무료 Tunnel은 매번 새로운 URL을 생성합니다

**해결 방법:**

#### 방법 1: Named Tunnel (권장)
```bash
# 1. Cloudflare 계정 생성 (무료)
cloudflared tunnel login

# 2. Named Tunnel 생성
cloudflared tunnel create smartfarm-api

# 3. Named Tunnel 실행
cloudflared tunnel run smartfarm-api
```

**장점:**
- URL이 고정됨: `https://smartfarm-api.your-account.workers.dev`
- `api-config.js`를 한 번만 수정하면 됨

#### 방법 2: 환경 변수 사용
```javascript
// api-config.js
const API_CONFIG = {
  // 환경에 따라 자동 선택
  BASE_URL: window.location.hostname === 'localhost' 
    ? 'http://localhost:8000'
    : 'https://abc-123-xyz.trycloudflare.com',  // 👈 Tunnel URL 업데이트
  
  // ... (나머지 동일)
};
```

---

## 📊 비용 정보

| 항목 | 비용 |
|------|------|
| Cloudflare Tunnel (Quick Tunnel) | ✅ 무료 |
| Cloudflare Tunnel (Named Tunnel) | ✅ 무료 |
| Netlify (Static Hosting) | ✅ 무료 (100GB/월) |
| GitHub (Public Repo) | ✅ 무료 |
| **총 비용** | **✅ 0원** |

---

## 🎯 다음 단계

### 로컬 개발 완료 후:
1. ✅ `start_api_server.bat` 실행
2. ✅ `start_cloudflare_tunnel.bat` 실행
3. ✅ Tunnel URL 복사
4. ✅ `web_ui/api-config.js` 업데이트
5. ✅ GitHub에 푸시
6. ✅ Netlify 자동 재배포

### 프로덕션 환경:
1. Named Tunnel 설정 (URL 고정)
2. 방화벽 설정
3. SSL 인증서 (Cloudflare가 자동 제공)
4. 모니터링 설정

---

## 💡 추가 팁

### 1. 로컬 테스트 시
```javascript
// api-config.js
BASE_URL: 'http://localhost:8000',  // 로컬 테스트
```

### 2. Netlify 배포 시
```javascript
// api-config.js
BASE_URL: 'https://abc-123-xyz.trycloudflare.com',  // 프로덕션
```

### 3. 자동 전환 (고급)
```javascript
// api-config.js
const API_CONFIG = {
  BASE_URL: (() => {
    // 환경에 따라 자동 선택
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return 'http://localhost:8000';  // 로컬
    } else {
      return 'https://abc-123-xyz.trycloudflare.com';  // 프로덕션
    }
  })(),
  
  // ... (나머지 동일)
};
```

---

**완료! 🎉**

이제 Netlify에서 프론트엔드를 배포하고, 로컬 REST API를 Cloudflare Tunnel로 HTTPS로 노출할 수 있습니다!






