#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
REST API 테스트 클라이언트
================================================================================
rest_api_server.py를 테스트하는 간단한 클라이언트

사용법:
    python test_api_client.py
    
필요 패키지:
    pip install requests
================================================================================
"""

import requests
import json
from typing import Dict, Any

# API 기본 URL
BASE_URL = "http://localhost:8000"


def print_response(title: str, response: requests.Response):
    """응답 예쁘게 출력"""
    print("\n" + "=" * 70)
    print(f"📡 {title}")
    print("=" * 70)
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print("=" * 70)


def test_health_check():
    """헬스 체크"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200


def test_list_controls():
    """제어 항목 목록 조회"""
    print("\n\n🔍 전체 제어 항목 목록 조회")
    response = requests.get(f"{BASE_URL}/api/controls/list")
    print_response("전체 목록", response)
    
    # 쓰기 가능 항목만
    print("\n\n✏️ 쓰기 가능 항목만 조회")
    response = requests.get(f"{BASE_URL}/api/controls/list?writable_only=true")
    print_response("쓰기 가능 항목", response)
    
    # 센서 카테고리만
    print("\n\n🌡️ 센서 항목만 조회")
    response = requests.get(f"{BASE_URL}/api/controls/list?category=sensors")
    print_response("센서 항목", response)


def test_read_sensor():
    """센서값 읽기"""
    print("\n\n🌡️ 센서값 읽기 테스트")
    
    sensors = [
        "내부현재온도",
        "내부현재습도",
        "외부현재온도",
        "외부일사량"
    ]
    
    for sensor in sensors:
        response = requests.get(f"{BASE_URL}/api/sensors/{sensor}")
        print_response(f"센서: {sensor}", response)


def test_read_all_sensors():
    """모든 센서값 조회"""
    print("\n\n📊 모든 센서값 조회")
    response = requests.get(f"{BASE_URL}/api/sensors/all")
    print_response("전체 센서", response)


def test_read_setting():
    """설정값 읽기"""
    print("\n\n⚙️ 설정값 읽기 테스트")
    
    settings = [
        "제습오토모드",
        "유동팬오토모드",
        "난방ON온도설정",
        "유동팬ON온도"
    ]
    
    for setting in settings:
        response = requests.get(f"{BASE_URL}/api/settings/{setting}")
        print_response(f"설정: {setting}", response)


def test_write_setting():
    """설정값 쓰기"""
    print("\n\n✏️ 설정값 쓰기 테스트")
    
    # 주의: 실제 장비에 쓰기를 수행합니다!
    # 테스트 전에 안전한지 확인하세요
    
    confirm = input("\n⚠️  실제 장비에 쓰기를 수행합니다. 계속하시겠습니까? (yes/no): ")
    if confirm.lower() != 'yes':
        print("쓰기 테스트를 건너뜁니다.")
        return
    
    # 제습오토모드 토글 테스트
    print("\n\n1️⃣ 제습오토모드 현재 상태 읽기")
    response = requests.get(f"{BASE_URL}/api/settings/제습오토모드")
    print_response("현재 상태", response)
    
    if response.status_code == 200:
        current_value = response.json().get('value', 0)
        new_value = 1 if current_value == 0 else 0
        
        print(f"\n\n2️⃣ 제습오토모드 값 변경: {current_value} → {new_value}")
        response = requests.put(
            f"{BASE_URL}/api/settings/제습오토모드",
            json={"value": new_value}
        )
        print_response("쓰기 결과", response)
        
        print(f"\n\n3️⃣ 제습오토모드 변경 확인")
        response = requests.get(f"{BASE_URL}/api/settings/제습오토모드")
        print_response("변경 후 상태", response)


def test_read_status():
    """상태값 읽기"""
    print("\n\n📈 상태값 읽기 테스트")
    
    statuses = [
        "유동팬출력표시",
        "난방출력표시",
        "PCB온도센서에러",
        "내부온도센서에러"
    ]
    
    for status in statuses:
        response = requests.get(f"{BASE_URL}/api/status/{status}")
        print_response(f"상태: {status}", response)


def test_raw_access():
    """Raw 레지스터 접근"""
    print("\n\n🔧 Raw 레지스터 접근 테스트")
    
    # 워드주소 70 읽기 (내부현재온도)
    response = requests.get(f"{BASE_URL}/api/raw/read/70")
    print_response("Raw Read - 워드70", response)


def main():
    """메인 테스트 실행"""
    print("=" * 70)
    print("🚀 REST API 테스트 클라이언트")
    print("=" * 70)
    print(f"서버 URL: {BASE_URL}")
    print("=" * 70)
    
    # 서버 연결 확인
    if not test_health_check():
        print("\n❌ 서버 연결 실패!")
        print("1. REST API 서버가 실행 중인지 확인하세요: python rest_api_server.py")
        print(f"2. URL이 올바른지 확인하세요: {BASE_URL}")
        return
    
    print("\n✅ 서버 연결 성공!")
    
    # 메뉴
    while True:
        print("\n\n" + "=" * 70)
        print("📋 테스트 메뉴")
        print("=" * 70)
        print("1. 제어 항목 목록 조회")
        print("2. 센서값 읽기")
        print("3. 모든 센서값 조회")
        print("4. 설정값 읽기")
        print("5. 설정값 쓰기 (⚠️  주의)")
        print("6. 상태값 읽기")
        print("7. Raw 레지스터 접근")
        print("0. 종료")
        print("=" * 70)
        
        choice = input("\n선택: ").strip()
        
        if choice == '1':
            test_list_controls()
        elif choice == '2':
            test_read_sensor()
        elif choice == '3':
            test_read_all_sensors()
        elif choice == '4':
            test_read_setting()
        elif choice == '5':
            test_write_setting()
        elif choice == '6':
            test_read_status()
        elif choice == '7':
            test_raw_access()
        elif choice == '0':
            print("\n👋 테스트 클라이언트를 종료합니다.")
            break
        else:
            print("❌ 잘못된 선택입니다.")
        
        input("\n\n⏸️  Enter를 눌러 계속...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 사용자가 중단했습니다.")
    except Exception as e:
        print(f"\n\n❌ 오류 발생: {e}")






