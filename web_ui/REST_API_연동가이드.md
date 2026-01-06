# 프론트엔드 REST API 연동 가이드 🌐

> **스마트팜 대시보드 ↔ REST API 서버 연동**  
> 영어 전용 API | 실시간 센서 모니터링 | 제어 기능

---

## 📋 목차

1. [빠른 시작](#-빠른-시작)
2. [서버 주소 설정](#-서버-주소-설정)
3. [파일 구조](#-파일-구조)
4. [API 연동 방법](#-api-연동-방법)
5. [테스트 방법](#-테스트-방법)
6. [주요 변경사항](#-주요-변경사항)
7. [트러블슈팅](#-트러블슈팅)

---

## 🚀 빠른 시작

### 1️⃣ REST API 서버 실행

```bash
# 프로젝트 루트 디렉토리에서
python rest_api_server.py
```

서버 시작 확인:
- **API 서버**: http://localhost:8000
- **Swagger 문서**: http://localhost:8000/docs

### 2️⃣ 프론트엔드 실행

```bash
# web_ui 디렉토리로 이동
cd web_ui

# 간단한 HTTP 서버 실행 (Python)
python -m http.server 3000

# 또는 Node.js
npx http-server -p 3000
```

브라우저에서 접속:
- **대시보드**: http://localhost:3000/index.html

### 3️⃣ 연결 확인

브라우저 개발자 도구(F12) 콘솔에서 확인:
```
✅ Health check: {status: "ok", modbus_connected: true}
✅ Sensor data updated: {...}
```

---

## 🌐 서버 주소 설정

### 로컬 테스트 (기본값)

`api-config.js` 파일에서 기본 설정 확인:

```javascript
const API_CONFIG = {
  BASE_URL: 'http://localhost:8000',  // 로컬 서버
  ...
};
```

### 실제 서버로 변경

#### 방법 1: 파일 수정 (권장)

`api-config.js` 파일 열기:

```javascript
const API_CONFIG = {
  // 개발: 'http://localhost:8000'
  // 운영: 'http://실제서버IP:8000'
  BASE_URL: 'http://192.168.1.100:8000',  // 실제 서버 IP로 변경
  ...
};
```

#### 방법 2: 브라우저 콘솔에서 동적 변경

브라우저 개발자 도구(F12) 콘솔에서:

```javascript
// 서버 주소 변경
ConfigManager.setBaseURL('http://192.168.1.100:8000');

// 연결 테스트
await ConfigManager.testConnection();
```

#### 방법 3: 환경별 설정 파일 (고급)

`api-config.js` 상단에 추가:

```javascript
// 환경 감지
const isProduction = window.location.hostname !== 'localhost';
const API_CONFIG = {
  BASE_URL: isProduction 
    ? 'http://192.168.1.100:8000'  // 운영 서버
    : 'http://localhost:8000',      // 개발 서버
  ...
};
```

---

## 📁 파일 구조

### 핵심 파일

```
web_ui/
├── 🔧 api-config.js          # API 서버 주소 및 엔드포인트 설정
├── 🌐 api-client.js          # REST API 호출 로직
├── 📊 data-manager.js        # 센서 데이터 관리 및 UI 업데이트
├── 📜 script.js              # 메인 UI 로직
├── 📈 chart-manager.js       # 차트 관리
│
├── 🏠 index.html             # 메인 대시보드
├── 🛰️ sensor-monitor.html   # 센서 모니터
├── 🧭 control-schedule.html # 제어 스케줄
├── 🔔 notifications.html    # 알림 센터
├── 📹 monitoring.html       # 모니터링
├── 🗂️ reports.html          # 리포트
│
└── 🎨 styles.css, pages.css  # 스타일
```

### 수정된 파일

✅ **api-config.js**
- 서버 주소 설정 기능 추가
- 영어 API 엔드포인트로 변경
- 센서 키 매핑 업데이트

✅ **api-client.js**
- 오늘 만든 REST API에 맞게 메서드 수정
- `getSetting()`, `setSetting()` 추가
- `getStatus()` 추가
- 센서 데이터 포맷팅 로직 수정

✅ **data-manager.js**
- 센서 키 매핑 업데이트
- UI 업데이트 로직 개선

---

## 🔌 API 연동 방법

### 센서 데이터 읽기

#### 모든 센서 한 번에

```javascript
// API 호출
const sensors = await apiClient.getAllSensors();

// 결과
{
  indoor_temp: 23.5,          // 내부온도
  indoor_humidity: 65,        // 내부습도
  indoor_solar: 350,          // 내부일사량
  outdoor_temp: 18.2,         // 외부온도
  outdoor_humidity: 72,       // 외부습도
  outdoor_solar: 580,         // 외부일사량
  ...
}
```

#### 개별 센서

```javascript
// UI 키 사용
const data = await apiClient.getSensor('indoor_temp');

// 또는 직접 API 이름 사용
const data = await apiClient.getSensor('indoor_current_temperature');

// 결과
{
  success: true,
  name: "indoor_current_temperature",
  value: 23.5,
  unit: "°C",
  type: "SENSOR_READ",
  address: 70,
  description: "내부 현재온도 (내부현재온도)"
}
```

### 설정값 읽기/쓰기

#### 설정값 읽기

```javascript
// 제습 오토모드 상태 확인
const data = await apiClient.getSetting('dehumidifier_auto');

// 결과
{
  success: true,
  name: "dehumidifier_auto_mode",
  value: 0,  // 0=OFF, 1=ON
  unit: "-",
  type: "BIT_WRITE",
  address: 18,
  description: "제습오토모드 (제습오토모드)"
}
```

#### 설정값 쓰기

```javascript
// 제습 오토모드 켜기
const result = await apiClient.setSetting('dehumidifier_auto', 1);

// 결과
{
  success: true,
  name: "dehumidifier_auto_mode",
  written_value: 1,
  verified_value: 1,
  type: "BIT_WRITE",
  address: 18
}
```

### 상태값 읽기

```javascript
// 유동팬 출력 표시 확인
const status = await apiClient.getStatus('circulation_fan_output_indicator');

// 결과
{
  success: true,
  name: "circulation_fan_output_indicator",
  value: 1,  // 0=OFF, 1=ON
  unit: "-",
  type: "BIT_READ",
  address: 65,
  description: "유동팬출력 표시 (유동팬출력표시)"
}
```

### 헬스 체크

```javascript
// Modbus 연결 상태 확인
const health = await apiClient.checkHealth();

// 결과
{
  status: "ok",
  modbus_connected: true,
  timestamp: "2024-12-09T12:34:56.789Z"
}
```

---

## 🧪 테스트 방법

### 방법 1: 브라우저 콘솔 (권장)

브라우저에서 대시보드 열고 F12 → Console:

```javascript
// 1. 헬스 체크
await apiClient.checkHealth();

// 2. 모든 센서 조회
const sensors = await apiClient.getAllSensors();
console.table(sensors);

// 3. 개별 센서 조회
await apiClient.getSensor('indoor_temp');

// 4. 설정값 읽기
await apiClient.getSetting('dehumidifier_auto');

// 5. 설정값 쓰기 (주의!)
await apiClient.setSetting('dehumidifier_auto', 1);

// 6. 상태 확인
await apiClient.getStatus('circulation_fan_output_indicator');

// 7. 서버 주소 변경
ConfigManager.setBaseURL('http://192.168.1.100:8000');
await ConfigManager.testConnection();
```

### 방법 2: 네트워크 탭 확인

브라우저 F12 → Network 탭:
1. 대시보드 열기
2. 자동으로 API 호출 시작
3. `localhost:8000` 요청 확인
4. 응답 확인

### 방법 3: 자동 새로고침 확인

대시보드가 10초마다 자동으로 센서 데이터를 업데이트합니다:

```javascript
// 현재 센서 데이터 확인
dataManager.getSensorData();

// 수동 새로고침
await dataManager.refresh();

// 자동 새로고침 중지
dataManager.stop();

// 자동 새로고침 재시작
dataManager.start();
```

---

## 🔄 주요 변경사항

### ✅ API 엔드포인트 변경

| 구분 | 기존 | 신규 (영어 API) |
|------|------|-----------------|
| 센서 전체 | `/api/sensors` | `/api/sensors/all` |
| 센서 개별 | `/api/sensors/{key}` | `/api/sensors/{name}` |
| 설정 읽기 | (없음) | `/api/settings/{name}` |
| 설정 쓰기 | `/api/bits/{addr}/{bit}` | `/api/settings/{name}` |
| 상태 읽기 | (없음) | `/api/status/{name}` |
| 헬스 체크 | `/healthz` | `/health` |

### ✅ 센서 키 매핑

| UI 표시 | 기존 키 | 신규 키 (영어) |
|---------|---------|----------------|
| 내부온도 | `indoor_temp_1` | `indoor_current_temperature` |
| 내부습도 | `indoor_humidity` | `indoor_current_humidity` |
| 내부일사량 | `indoor_solar` | `indoor_current_solar_radiation` |
| 토양함수율 | (없음) | `indoor_current_moisture` |
| 토양장력 | `indoor_soil_tension` | `indoor_current_soil_tension` |
| 외부온도 | `outdoor_temp` | `outdoor_current_temperature` |
| 외부습도 | `outdoor_humidity` | `outdoor_current_humidity` |
| 외부일사량 | `outdoor_solar` | `outdoor_solar_radiation` |
| 풍향 | `outdoor_wind_dir` | `indoor_wind_direction` |
| 풍속 | `outdoor_wind_speed` | `outdoor_wind_speed` |

### ✅ 응답 형식 변경

**센서 전체 조회 (`/api/sensors/all`)**

```json
{
  "success": true,
  "count": 10,
  "sensors": {
    "indoor_current_temperature": {
      "value": 23.5,
      "unit": "°C",
      "address": 70,
      "description": "내부 현재온도 (내부현재온도)",
      "success": true
    },
    ...
  }
}
```

**설정값 읽기 (`/api/settings/{name}`)**

```json
{
  "success": true,
  "name": "dehumidifier_auto_mode",
  "value": 0,
  "unit": "-",
  "type": "BIT_WRITE",
  "address": 18,
  "description": "제습오토모드 (제습오토모드)"
}
```

**설정값 쓰기 (`/api/settings/{name}`)**

```json
{
  "success": true,
  "name": "dehumidifier_auto_mode",
  "written_value": 1,
  "verified_value": 1,
  "type": "BIT_WRITE",
  "address": 18
}
```

---

## 🔧 트러블슈팅

### ❌ 연결 실패: CORS 에러

**증상**:
```
Access to fetch at 'http://localhost:8000/...' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**해결**:
1. `rest_api_server.py`에서 CORS 설정 확인:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # 개발 중에는 "*", 운영에서는 특정 도메인
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. 또는 브라우저 확장 프로그램 사용 (개발 전용):
   - Chrome: "CORS Unblock"
   - Firefox: "CORS Everywhere"

### ❌ 센서 데이터가 표시되지 않음

**확인 사항**:

1. **REST API 서버 실행 중인가?**
   ```bash
   # 터미널에서 확인
   netstat -an | findstr :8000  # Windows
   lsof -i :8000                 # Mac/Linux
   ```

2. **Modbus 연결 상태 확인**
   ```javascript
   await apiClient.checkHealth();
   // modbus_connected: true 확인
   ```

3. **HTML의 data-sensor 속성 확인**
   ```html
   <!-- 올바른 예 -->
   <div data-sensor="indoor_temp">...</div>
   
   <!-- 잘못된 예 -->
   <div data-sensor="indoor_temp_1">...</div>  <!-- 구식 키 -->
   ```

### ❌ 설정값 쓰기 실패

**확인 사항**:

1. **올바른 항목인가?**
   ```javascript
   // 설정값 항목 목록 확인
   console.log(API_CONFIG.SETTING_KEYS);
   ```

2. **값 범위가 올바른가?**
   - 비트 값: 0 또는 1만 허용
   - 레지스터 값: 각 항목마다 범위 다름

3. **실제 하드웨어가 연결되어 있는가?**
   - `/health` 엔드포인트로 Modbus 연결 확인

### ❌ 자동 새로고침이 작동하지 않음

**확인**:

```javascript
// DataManager 상태 확인
console.log(dataManager.isRunning);  // true여야 함

// 수동으로 재시작
dataManager.stop();
dataManager.start();
```

### ❌ 서버 주소 변경 후 연결 안 됨

**확인 사항**:

1. **방화벽 설정**
   - 서버 PC의 8000 포트 허용

2. **네트워크 연결**
   ```bash
   # 핑 테스트
   ping 192.168.1.100
   
   # 포트 테스트
   telnet 192.168.1.100 8000
   ```

3. **REST API 서버 주소 바인딩**
   ```python
   # rest_api_server.py 마지막 부분
   if __name__ == "__main__":
       uvicorn.run(
           app,
           host="0.0.0.0",  # 외부 접속 허용
           port=8000
       )
   ```

---

## 📝 주의사항

### 🔴 설정값 쓰기 작업 시

1. **실제 장비에 즉시 반영됩니다**
   - 테스트 환경이 아니면 신중하게 사용

2. **현재 상태 먼저 확인**
   ```javascript
   // 나쁜 예
   await apiClient.setSetting('heating_auto', 1);
   
   // 좋은 예
   const current = await apiClient.getSetting('heating_auto');
   console.log('현재값:', current.value);
   // 확인 후 변경
   await apiClient.setSetting('heating_auto', 1);
   ```

3. **쓰기 후 검증**
   ```javascript
   const result = await apiClient.setSetting('heating_auto', 1);
   console.log('쓴 값:', result.written_value);
   console.log('검증 값:', result.verified_value);
   // 두 값이 같아야 정상
   ```

### 🟡 성능 최적화

1. **불필요한 API 호출 줄이기**
   - 자동 새로고침 주기 조절 (기본 10초)
   - 필요한 센서만 조회

2. **네트워크 요청 배치**
   ```javascript
   // 나쁜 예: 개별 호출
   const temp = await apiClient.getSensor('indoor_temp');
   const humid = await apiClient.getSensor('indoor_humidity');
   
   // 좋은 예: 한 번에
   const allSensors = await apiClient.getAllSensors();
   ```

---

## 🎉 완료!

이제 프론트엔드와 REST API가 완벽하게 연동되었습니다!

### ✅ 확인 체크리스트

- [ ] REST API 서버 실행 중
- [ ] 프론트엔드 실행 중
- [ ] 브라우저 콘솔에서 헬스 체크 성공
- [ ] 센서 데이터 표시됨
- [ ] 자동 새로고침 작동 중
- [ ] 서버 주소 설정 확인

### 📚 관련 문서

- **REST API 완전 가이드**: `../REST_API_완전가이드.md`
- **제어 명세서**: `../제어명세서.txt`
- **제어 항목 요약**: `../제어항목_요약.txt`

---

**문서 생성일**: 2024-12-09  
**프로젝트**: 스마트팜 RS485(Modbus) → TCP/IP → REST API 변환






