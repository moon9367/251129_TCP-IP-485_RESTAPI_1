# REST API 완전 가이드 📚

> **RS485(Modbus) → TCP/IP → REST API 변환 프로젝트**  
> 영어 전용 API | 223개 제어 항목 | 자동 Swagger 문서

---

## 📋 목차

1. [빠른 시작](#-빠른-시작)
2. [API 엔드포인트](#-api-엔드포인트)
3. [테스트 방법](#-테스트-방법)
4. [제어 항목 분류](#-제어-항목-분류)
5. [사용 예시](#-사용-예시)
6. [주요 제어 항목](#-주요-제어-항목)
7. [주의사항](#-주의사항)

---

## 🚀 빠른 시작

### 1️⃣ 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

또는 직접 설치:
```bash
pip install fastapi uvicorn pymodbus pydantic requests
```

### 2️⃣ REST API 서버 실행

```bash
python rest_api_server.py
```

서버가 시작되면:
- **API 서버**: http://localhost:8000
- **Swagger 문서**: http://localhost:8000/docs ⭐ (추천!)
- **ReDoc 문서**: http://localhost:8000/redoc

### 3️⃣ 연결 정보

- **Modbus TCP 주소**: aiseednaju.iptime.org:9139 (DDNS) - IP: 168.131.153.52 (참고용)
- **Unit ID**: 1
- **총 제어 항목**: 223개

---

## 📡 API 엔드포인트

### 📌 기본 정보

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/` | GET | API 정보 및 버전 |
| `/health` | GET | Modbus 연결 상태 확인 |
| `/docs` | GET | Swagger UI (대화형 문서) |

### 📋 제어 항목 목록

| 엔드포인트 | 설명 | 예시 |
|-----------|------|------|
| `/api/controls/list` | 전체 항목 목록 (223개) | - |
| `/api/controls/list?category=sensors` | 센서 항목만 (10개) | 온도, 습도 등 |
| `/api/controls/list?category=settings` | 설정 항목만 (125개) | 모드, 온도 설정 등 |
| `/api/controls/list?category=status` | 상태 항목만 (88개) | 출력표시, 에러 등 |
| `/api/controls/list?writable_only=true` | 쓰기 가능 항목만 (125개) | 설정값 |

### 🔧 설정값 (읽기/쓰기 가능)

| 엔드포인트 | 메서드 | 설명 | 워드주소 |
|-----------|--------|------|----------|
| `/api/settings/{name}` | GET | 현재 설정값 읽기 | 0~59 |
| `/api/settings/{name}` | PUT | 설정값 변경 (⚠️ 주의) | 0~59 |

**예시 항목**: `dehumidifier_auto_mode`, `heating_on_temperature_setting`, `circulation_fan_auto_mode`

### 🌡️ 센서값 (읽기 전용)

| 엔드포인트 | 메서드 | 설명 | 워드주소 |
|-----------|--------|------|----------|
| `/api/sensors/{name}` | GET | 센서값 읽기 | 70~79 |
| `/api/sensors/all` | GET | 모든 센서값 한 번에 | 70~79 |

**예시 항목**: `indoor_current_temperature`, `outdoor_current_humidity`, `indoor_current_solar_radiation`

### 📊 상태값 (읽기 전용)

| 엔드포인트 | 메서드 | 설명 | 워드주소 |
|-----------|--------|------|----------|
| `/api/status/{name}` | GET | 상태/에러 읽기 | 60~69, 80~84 |

**예시 항목**: `circulation_fan_output_indicator`, `internal_temperature_sensor_error`

### 🔨 Raw 레지스터 (고급 사용자용)

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/api/raw/read/{address}` | GET | 워드주소 직접 읽기 |
| `/api/raw/write/{address}` | POST | 워드주소 직접 쓰기 (⚠️ 위험) |

---

## 🧪 테스트 방법

### 🌐 방법 1: Swagger UI (가장 쉬움! ⭐)

1. **브라우저에서 열기**:
   ```
   http://localhost:8000/docs
   ```

2. **센서값 읽기 테스트**:
   - `GET /api/sensors/{name}` 클릭
   - "Try it out" 버튼 클릭
   - `name`에 **indoor_current_temperature** 입력
   - "Execute" 버튼 클릭
   - 결과 확인! ✅

3. **전체 목록 보기**:
   - `GET /api/controls/list` 클릭
   - "Try it out" 클릭
   - "Execute" 클릭
   - 223개 항목 확인!

4. **설정값 변경 테스트** (주의!):
   - `PUT /api/settings/{name}` 클릭
   - "Try it out" 클릭
   - `name`에 **dehumidifier_auto_mode** 입력
   - Request body에 `{"value": 1}` 입력
   - "Execute" 클릭

### 💻 방법 2: Python 코드

```python
import requests

# 1. 센서값 읽기
response = requests.get("http://localhost:8000/api/sensors/indoor_current_temperature")
data = response.json()
print(f"온도: {data['value']}°C")

# 2. 설정값 읽기
response = requests.get("http://localhost:8000/api/settings/dehumidifier_auto_mode")
print(f"제습모드: {response.json()['value']}")

# 3. 설정값 쓰기 (주의!)
response = requests.put(
    "http://localhost:8000/api/settings/dehumidifier_auto_mode",
    json={"value": 1}
)
print(f"변경 성공: {response.json()['success']}")

# 4. 모든 센서값 조회
response = requests.get("http://localhost:8000/api/sensors/all")
sensors = response.json()['sensors']
for name, data in sensors.items():
    print(f"{name}: {data['value']} {data['unit']}")
```

### 🔧 방법 3: PowerShell (Windows)

```powershell
# 서버 상태 확인
Invoke-WebRequest -Uri "http://localhost:8000/health"

# 센서값 읽기
Invoke-WebRequest -Uri "http://localhost:8000/api/sensors/indoor_current_temperature"

# 설정값 읽기
Invoke-WebRequest -Uri "http://localhost:8000/api/settings/dehumidifier_auto_mode"

# 설정값 쓰기 (주의!)
Invoke-WebRequest -Uri "http://localhost:8000/api/settings/dehumidifier_auto_mode" `
  -Method PUT `
  -ContentType "application/json" `
  -Body '{"value": 1}'

# 전체 목록 조회
Invoke-WebRequest -Uri "http://localhost:8000/api/controls/list"
```

### 🐚 방법 4: cURL (Linux/Mac/Git Bash)

```bash
# 센서값 읽기
curl http://localhost:8000/api/sensors/indoor_current_temperature

# 설정값 쓰기
curl -X PUT http://localhost:8000/api/settings/dehumidifier_auto_mode \
  -H "Content-Type: application/json" \
  -d '{"value": 1}'
```

---

## 📊 제어 항목 분류

### 총 223개 제어 항목

| 카테고리 | 개수 | 워드주소 | 설명 |
|---------|------|----------|------|
| **설정값 (쓰기 가능)** | **125개** | **0~59** | **모드, 온도 설정 등** |
| └ REGISTER_WRITE | 40개 | - | 레지스터 전체 쓰기 (온도, 시간 등) |
| └ BIT_WRITE | 52개 | - | 비트 단위 쓰기 (모드 ON/OFF) |
| └ BIT_RANGE_WRITE | 33개 | - | 비트 범위 쓰기 (시간, 횟수 등) |
| **센서값 (읽기 전용)** | **10개** | **70~79** | **온도, 습도 등** |
| └ SENSOR_READ | 10개 | 70~79 | 센서 현재값 |
| **상태값 (읽기 전용)** | **88개** | **60~69, 80~84** | **출력표시, 에러 등** |
| └ BIT_READ | 80개 | 65~69 | 상태/에러 비트 |
| └ REGISTER_READ | 8개 | 60~64, 80~84 | 시스템 상태 |

### 🎯 REST API 엔드포인트 매핑

```
워드주소 0~59 (설정값)
└─> GET/PUT /api/settings/{name}
    ├─ dehumidifier_auto_mode (제습오토모드)
    ├─ heating_on_temperature_setting (난방ON온도설정)
    └─ circulation_fan_auto_mode (유동팬오토모드)

워드주소 70~79 (센서값)
└─> GET /api/sensors/{name}
    ├─ indoor_current_temperature (내부현재온도)
    ├─ indoor_current_humidity (내부현재습도)
    └─ outdoor_current_temperature (외부현재온도)

워드주소 60~69, 80~84 (상태)
└─> GET /api/status/{name}
    ├─ circulation_fan_output_indicator (유동팬출력표시)
    ├─ internal_temperature_sensor_error (내부온도센서에러)
    └─ heating_output_indicator (난방출력표시)
```

---

## 💡 사용 예시

### 예시 1: 센서값 읽기 (온도)

**요청**:
```http
GET /api/sensors/indoor_current_temperature
```

**응답**:
```json
{
  "success": true,
  "name": "indoor_current_temperature",
  "value": 23.5,
  "unit": "°C",
  "type": "SENSOR_READ",
  "address": 70,
  "description": "내부 현재온도 (내부현재온도)"
}
```

### 예시 2: 설정값 읽기 (제습모드)

**요청**:
```http
GET /api/settings/dehumidifier_auto_mode
```

**응답**:
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

### 예시 3: 설정값 쓰기 (제습모드 켜기)

**요청**:
```http
PUT /api/settings/dehumidifier_auto_mode
Content-Type: application/json

{
  "value": 1
}
```

**응답**:
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

### 예시 4: 상태 확인 (출력표시)

**요청**:
```http
GET /api/status/circulation_fan_output_indicator
```

**응답**:
```json
{
  "success": true,
  "name": "circulation_fan_output_indicator",
  "value": 0,
  "unit": "-",
  "type": "BIT_READ",
  "address": 65,
  "description": "유동팬출력 표시 (유동팬출력표시)"
}
```

### 예시 5: 모든 센서값 조회

**요청**:
```http
GET /api/sensors/all
```

**응답**:
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
    "indoor_current_humidity": {
      "value": 65.2,
      "unit": "%",
      "address": 71,
      "description": "내부 현재습도 (내부현재습도)",
      "success": true
    }
  }
}
```

---

## 🎯 주요 제어 항목

### ✏️ 쓰기 가능한 설정값 (워드주소 0~59)

#### 모드 제어 (BIT_WRITE) - 0/1 토글

| 영어 이름 | 한글 이름 | 워드주소 | 비트 | 설명 |
|----------|----------|---------|------|------|
| `dehumidifier_auto_mode` | 제습오토모드 | 18 | 0 | 제습 자동 제어 |
| `circulation_fan_auto_mode` | 유동팬오토모드 | 9 | 0 | 유동팬 자동 제어 |
| `heating_auto_mode` | 난방오토모드 | 14 | 0 | 난방 자동 제어 |
| `irrigation_auto_mode` | 관수오토모드 | 10 | 0 | 관수 자동 제어 |
| `lighting_auto_mode` | 조명오토모드 | 45 | 0 | 조명 자동 제어 |
| `dehumidifier_forced_operation` | 제습강제운전 | 19 | 0 | 제습 강제 운전 |
| `circulation_fan_forced_operation` | 유동팬강제운전 | 9 | 1 | 유동팬 강제 운전 |

#### 온도 설정 (REGISTER_WRITE) - 온도값

| 영어 이름 | 한글 이름 | 워드주소 | 범위 | 단위 |
|----------|----------|---------|------|------|
| `heating_on_temperature_setting` | 난방ON온도설정 | 16 | 0~65535 | °C |
| `heating_off_temperature_setting` | 난방OFF온도설정 | 17 | 0~65535 | °C |
| `circulation_fan_on_temperature` | 유동팬ON온도 | 5 | 0~999 | °C |
| `circulation_fan_off_temperature` | 유동팬OFF온도 | 6 | -55~999 | °C |
| `insulation_curtain_open_temperature_setting` | 보온커튼열림온도설정 | 31 | 0~65535 | °C |

### 📖 읽기 전용 센서값 (워드주소 70~79)

| 영어 이름 | 한글 이름 | 워드주소 | 단위 | 설명 |
|----------|----------|---------|------|------|
| `indoor_current_temperature` | 내부현재온도 | 70 | °C | 실내 온도 |
| `indoor_current_humidity` | 내부현재습도 | 71 | % | 실내 습도 |
| `indoor_current_solar_radiation` | 내부현재일사량 | 72 | W/m² | 실내 일사량 |
| `indoor_current_moisture` | 내부현재함수율 | 73 | % | 토양 함수율 |
| `indoor_current_soil_tension` | 내부현재수분장력 | 74 | kPa | 토양 수분장력 |
| `outdoor_current_temperature` | 외부현재온도 | 75 | °C | 실외 온도 |
| `outdoor_current_humidity` | 외부현재습도 | 76 | % | 실외 습도 |
| `outdoor_solar_radiation` | 외부일사량 | 77 | W/m² | 실외 일사량 |

### 📊 읽기 전용 상태값 (워드주소 65~69)

#### 출력 표시 (BIT_READ)

| 영어 이름 | 한글 이름 | 워드주소 | 비트 | 의미 |
|----------|----------|---------|------|------|
| `circulation_fan_output_indicator` | 유동팬출력표시 | 65 | 2 | 1=작동중 |
| `irrigation_output_indicator` | 관수출력표시 | 65 | 3 | 1=작동중 |
| `heating_output_indicator` | 난방출력표시 | 65 | 4 | 1=작동중 |
| `dehumidifier_output_indicator` | 제습출력표시 | 65 | 5 | 1=작동중 |
| `lighting_output_indicator` | 조명출력표시 | 67 | 8 | 1=작동중 |

#### 에러 상태 (BIT_READ)

| 영어 이름 | 한글 이름 | 워드주소 | 비트 | 의미 |
|----------|----------|---------|------|------|
| `internal_temperature_sensor_error` | 내부온도센서에러 | 68 | 7 | 1=에러 |
| `internal_humidity_sensor_error` | 내부습도센서에러 | 68 | 8 | 1=에러 |
| `external_temperature_sensor_error` | 외부온도센서에러 | 69 | 8 | 1=에러 |
| `external_humidity_sensor_error` | 외부습도센서에러 | 69 | 9 | 1=에러 |
| `pcb_temperature_sensor_error` | PCB온도센서에러 | 65 | 1 | 1=에러 |

---

## ⚠️ 주의사항

### 🔴 설정값 쓰기 작업 시

1. **실제 장비에 영향**: 
   - 모든 쓰기 작업은 즉시 실제 하드웨어에 반영됩니다
   - 테스트 환경이 아니면 신중하게 사용하세요

2. **값 범위 확인**:
   - 각 항목마다 허용 범위가 다릅니다
   - Swagger UI에서 범위를 확인하세요
   - 잘못된 값은 거부되거나 예상치 못한 동작을 일으킬 수 있습니다

3. **현재 상태 먼저 확인**:
   ```python
   # 나쁜 예
   requests.put("/api/settings/heating_auto_mode", json={"value": 1})
   
   # 좋은 예
   current = requests.get("/api/settings/heating_auto_mode").json()
   print(f"현재값: {current['value']}")
   # 확인 후 변경
   requests.put("/api/settings/heating_auto_mode", json={"value": 1})
   ```

4. **비트 값 (모드 제어)**:
   - 0 = OFF, 1 = ON
   - 다른 값은 허용되지 않습니다

5. **온도 값**:
   - 대부분 10배 스케일링 (예: 23.5°C → 235)
   - API가 자동으로 변환하지만, Raw API 사용 시 주의

### 🟡 네트워크 설정

- **Modbus TCP**: `aiseednaju.iptime.org:9139` (DDNS)
- **REST API**: `localhost:8000`
- **변경 필요 시**: `rest_api_server.py` 파일 수정
  ```python
  controller = ModbusController(
      host="aiseednaju.iptime.org",  # DDNS 주소 (또는 IP: 168.131.153.52)
      port=9139,
      unit_id=1
  )
  ```

### 🟢 에러 코드

| 코드 | 의미 | 해결 방법 |
|-----|------|-----------|
| 200 | 성공 | - |
| 400 | 잘못된 요청 | 항목 이름, 값 범위 확인 |
| 404 | 항목을 찾을 수 없음 | 영어 이름 철자 확인 |
| 503 | Modbus 연결 실패 | 장비 전원, 네트워크 확인 |
| 500 | 서버 내부 오류 | 로그 확인 |

### 📝 권장 테스트 순서

1. ✅ **헬스 체크**: `/health`
2. ✅ **목록 조회**: `/api/controls/list`
3. ✅ **센서 읽기**: `/api/sensors/indoor_current_temperature`
4. ✅ **상태 읽기**: `/api/status/circulation_fan_output_indicator`
5. ✅ **설정 읽기**: `/api/settings/dehumidifier_auto_mode`
6. ⚠️ **설정 쓰기**: `/api/settings/dehumidifier_auto_mode` (주의!)

---

## 🎯 실전 활용 예시

### 1️⃣ 모니터링 대시보드

```python
import requests
import time

def monitor_sensors():
    """주요 센서값 실시간 모니터링"""
    while True:
        # 온도, 습도 읽기
        temp = requests.get("http://localhost:8000/api/sensors/indoor_current_temperature").json()
        humid = requests.get("http://localhost:8000/api/sensors/indoor_current_humidity").json()
        
        # 출력
        print(f"🌡️  온도: {temp['value']}°C | 💧 습도: {humid['value']}%")
        
        # 에러 체크
        temp_error = requests.get("http://localhost:8000/api/status/internal_temperature_sensor_error").json()
        if temp_error['value'] == 1:
            print("⚠️  온도 센서 에러 발생!")
        
        time.sleep(60)  # 1분마다

monitor_sensors()
```

### 2️⃣ 자동 제어 시스템

```python
import requests

def auto_control():
    """온도/습도에 따른 자동 제어"""
    # 현재 온도 확인
    temp_response = requests.get("http://localhost:8000/api/sensors/indoor_current_temperature")
    temp = temp_response.json()['value']
    
    # 현재 습도 확인
    humid_response = requests.get("http://localhost:8000/api/sensors/indoor_current_humidity")
    humid = humid_response.json()['value']
    
    # 조건별 제어
    if temp > 30:
        # 온도가 높으면 제습 켜기
        requests.put(
            "http://localhost:8000/api/settings/dehumidifier_auto_mode",
            json={"value": 1}
        )
        print("🔄 제습 시작 (온도 높음)")
    
    if humid > 80:
        # 습도가 높으면 유동팬 켜기
        requests.put(
            "http://localhost:8000/api/settings/circulation_fan_auto_mode",
            json={"value": 1}
        )
        print("🔄 유동팬 시작 (습도 높음)")

auto_control()
```

### 3️⃣ 에러 알림 시스템

```python
import requests

def check_errors():
    """모든 센서 에러 확인"""
    error_sensors = [
        "internal_temperature_sensor_error",
        "internal_humidity_sensor_error",
        "external_temperature_sensor_error",
        "external_humidity_sensor_error",
        "pcb_temperature_sensor_error"
    ]
    
    errors = []
    for sensor in error_sensors:
        response = requests.get(f"http://localhost:8000/api/status/{sensor}")
        data = response.json()
        
        if data['value'] == 1:
            errors.append(data['description'])
    
    if errors:
        print("⚠️  에러 발생:")
        for error in errors:
            print(f"   - {error}")
        # 여기에 이메일/SMS 알림 코드 추가
    else:
        print("✅ 모든 센서 정상")

check_errors()
```

### 4️⃣ 데이터 로깅

```python
import requests
import csv
from datetime import datetime

def log_sensor_data():
    """센서 데이터를 CSV 파일로 저장"""
    # 모든 센서 데이터 조회
    response = requests.get("http://localhost:8000/api/sensors/all")
    sensors = response.json()['sensors']
    
    # CSV 파일에 저장
    with open('sensor_log.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # 시간 기록
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [timestamp]
        
        # 각 센서값 추가
        for name, data in sensors.items():
            row.append(data['value'])
        
        writer.writerow(row)
    
    print(f"✅ {timestamp} 데이터 저장 완료")

# 1분마다 실행
import time
while True:
    log_sensor_data()
    time.sleep(60)
```

---


### 문제 해결

1. **Swagger UI 확인**: http://localhost:8000/docs
2. **서버 로그 확인**: REST API 서버 실행 터미널
3. **연결 상태 확인**: `/health` 엔드포인트

### 관련 문서

- `control_specs.py` - 모든 제어 항목 정의
- `제어명세서.txt` - 제어 항목 상세 설명 (한글/영어)
- `제어항목_요약.txt` - 제어 항목 요약 정보

---

## 📝 버전 정보

- **버전**: 3.0.0 (English Only)
- **마지막 업데이트**: 2024-12-09
- **호환성**: Python 3.7+
- **주요 변경사항**:
  - 영어 전용 API로 전환
  - 한글 이름은 description에 포함
  - 더 빠르고 간단한 구조

---

## 🎉 마무리

이제 **REST API**로 모든 Modbus 장비를 편리하게 제어할 수 있습니다!

**가장 쉬운 시작**: http://localhost:8000/docs 에서 바로 테스트하세요! 🚀


