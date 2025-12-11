#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Control Specifications Database (English Keys)
================================================================================
All Modbus control items defined with English keys

Usage:
    from control_specs import CONTROL_SPECS
    
    spec = CONTROL_SPECS["indoor_current_temperature"]
    print(spec['address'])      # 70
    print(spec['korean_name'])  # 내부현재온도
================================================================================
"""

# ============================================================================
# Control Specifications (CONTROL_SPECS) - English Keys
# ============================================================================

CONTROL_SPECS = {
    # ========================================================================
    # Word Address 0~4: Basic Settings
    # ========================================================================

    "io_board_station_number": {
        "korean_name": "IO보드국번",
        "type": "REGISTER_WRITE",
        "address": 0,
        "scale": 1,
        "unit": "-",
        "description": "IO보드 국번 (IO보드국번)"
    },

    "pcb_ambient_temperature_setting": {
        "korean_name": "PCB주위온도설정",
        "type": "REGISTER_WRITE",
        "address": 1,
        "scale": 10,
        "unit": "°C",
        "description": "PCB 주위온도 설정 (PCB주위온도설정)"
    },

    "program_password": {
        "korean_name": "프로그램비밀번호",
        "type": "REGISTER_WRITE",
        "address": 2,
        "scale": 1,
        "unit": "-",
        "description": "프로그램 정교조정 비밀번호 (프로그램비밀번호)"
    },

    "sensor_save_interval": {
        "korean_name": "센서값저장주기",
        "type": "REGISTER_WRITE",
        "address": 3,
        "scale": 1,
        "unit": "분",
        "description": "센서값 저장주기 (센서값저장주기)"
    },

    "sensor_record_unit_include": {
        "korean_name": "센서기록유닛포함",
        "type": "BIT_WRITE",
        "address": 4,
        "bit": 2,
        "unit": "-",
        "description": "센서기록 시 유닛포함 여부 (센서기록유닛포함)"
    },

    "sensor_file_type": {
        "korean_name": "센서파일타입",
        "type": "BIT_WRITE",
        "address": 4,
        "bit": 1,
        "unit": "-",
        "description": "센서기록파일타입 (0:txt, 1:csv) (센서파일타입)"
    },

    "password_enable": {
        "korean_name": "비밀번호사용",
        "type": "BIT_WRITE",
        "address": 4,
        "bit": 0,
        "unit": "-",
        "description": "비밀번호사용유무 (비밀번호사용)"
    },

    # ========================================================================
    # Word Address 5~13: Fan & Irrigation
    # ========================================================================

    "circulation_fan_on_temperature": {
        "korean_name": "유동팬ON온도",
        "type": "REGISTER_WRITE",
        "address": 5,
        "scale": 10,
        "unit": "°C",
        "description": "유동팬 ON설정온도 (유동팬ON온도)"
    },

    "circulation_fan_off_temperature": {
        "korean_name": "유동팬OFF온도",
        "type": "REGISTER_WRITE",
        "address": 6,
        "scale": 10,
        "unit": "°C",
        "description": "유동팬 OFF설정온도 (유동팬OFF온도)"
    },

    "circulation_fan_on_humidity": {
        "korean_name": "유동팬ON습도",
        "type": "REGISTER_WRITE",
        "address": 7,
        "scale": 10,
        "unit": "%",
        "description": "유동팬 ON설정습도 (유동팬ON습도)"
    },

    "circulation_fan_off_humidity": {
        "korean_name": "유동팬OFF습도",
        "type": "REGISTER_WRITE",
        "address": 8,
        "scale": 10,
        "unit": "%",
        "description": "유동팬 OFF설정습도 (유동팬OFF습도)"
    },

    "circulation_fan_off_time": {
        "korean_name": "유동팬OFF시간",
        "type": "BIT_RANGE_WRITE",
        "address": 9,
        "bit_start": 11,
        "bit_end": 15,
        "unit": "-",
        "description": "유동팬 OFF시간 (유동팬OFF시간)"
    },

    "circulation_fan_time_control_enable": {
        "korean_name": "유동팬시간조절",
        "type": "BIT_WRITE",
        "address": 9,
        "bit": 10,
        "unit": "-",
        "description": "유동팬시간조절 사용 (유동팬시간조절)"
    },

    "circulation_fan_humidity_control_enable": {
        "korean_name": "유동팬습도조절",
        "type": "BIT_WRITE",
        "address": 9,
        "bit": 9,
        "unit": "-",
        "description": "유동팬습도조절 사용 (유동팬습도조절)"
    },

    "circulation_fan_temperature_control_enable": {
        "korean_name": "유동팬온도조절",
        "type": "BIT_WRITE",
        "address": 9,
        "bit": 8,
        "unit": "-",
        "description": "유동팬 온도조절 사용 (유동팬온도조절)"
    },

    "circulation_fan_on_time": {
        "korean_name": "유동팬온시간",
        "type": "BIT_RANGE_WRITE",
        "address": 9,
        "bit_start": 2,
        "bit_end": 7,
        "unit": "-",
        "description": "유동팬 온시간 (유동팬온시간)"
    },

    "circulation_fan_forced_operation": {
        "korean_name": "유동팬강제운전",
        "type": "BIT_WRITE",
        "address": 9,
        "bit": 1,
        "unit": "-",
        "description": "유동팬강제운전 (유동팬강제운전)"
    },

    "circulation_fan_auto_mode": {
        "korean_name": "유동팬오토모드",
        "type": "BIT_WRITE",
        "address": 9,
        "bit": 0,
        "unit": "-",
        "description": "유동팬오토모드 (유동팬오토모드)"
    },

    "irrigation_moisture_setting": {
        "korean_name": "함수율관수설정",
        "type": "BIT_RANGE_WRITE",
        "address": 10,
        "bit_start": 8,
        "bit_end": 15,
        "unit": "-",
        "description": "함수율에 의한 관수 설정값 (함수율관수설정)"
    },

    "irrigation_start_hour": {
        "korean_name": "관수시작시",
        "type": "BIT_RANGE_WRITE",
        "address": 10,
        "bit_start": 2,
        "bit_end": 7,
        "unit": "시",
        "description": "관수 시작시각(시) (관수시작시)"
    },

    "irrigation_forced_operation": {
        "korean_name": "관수강제운전",
        "type": "BIT_WRITE",
        "address": 10,
        "bit": 1,
        "unit": "-",
        "description": "관수강제운전 (관수강제운전)"
    },

    "irrigation_auto_mode": {
        "korean_name": "관수오토모드",
        "type": "BIT_WRITE",
        "address": 10,
        "bit": 0,
        "unit": "-",
        "description": "관수오토모드 (관수오토모드)"
    },

    "irrigation_off_time_minutes": {
        "korean_name": "관수OFF시간",
        "type": "BIT_RANGE_WRITE",
        "address": 11,
        "bit_start": 9,
        "bit_end": 15,
        "unit": "분",
        "description": "관수 OFF시간(분) (관수OFF시간)"
    },

    "irrigation_time_unit": {
        "korean_name": "관수타임유닛",
        "type": "BIT_WRITE",
        "address": 11,
        "bit": 8,
        "unit": "-",
        "description": "관수ON/OFF 타임유닛 (관수타임유닛)"
    },

    "irrigation_on_time_minutes": {
        "korean_name": "관수ON시간",
        "type": "BIT_RANGE_WRITE",
        "address": 11,
        "bit_start": 1,
        "bit_end": 7,
        "unit": "분",
        "description": "관수 ON시간(분) (관수ON시간)"
    },

    "irrigation_sensor_condition_enable": {
        "korean_name": "관수센서조건",
        "type": "BIT_WRITE",
        "address": 11,
        "bit": 0,
        "unit": "-",
        "description": "관수 센서조건 사용 (관수센서조건)"
    },

    "irrigation_end_hour": {
        "korean_name": "관수종료시",
        "type": "BIT_RANGE_WRITE",
        "address": 12,
        "bit_start": 10,
        "bit_end": 15,
        "unit": "시",
        "description": "관수 종료시각(시) (관수종료시)"
    },

    "irrigation_repeat_count": {
        "korean_name": "관수반복회수",
        "type": "BIT_RANGE_WRITE",
        "address": 12,
        "bit_start": 6,
        "bit_end": 9,
        "unit": "회",
        "description": "관수 반복회수 (관수반복회수)"
    },

    "next_irrigation_day": {
        "korean_name": "다음관수일",
        "type": "BIT_RANGE_WRITE",
        "address": 12,
        "bit_start": 0,
        "bit_end": 5,
        "unit": "일",
        "description": "다음관수 일 설정 (다음관수일)"
    },

    "soil_tension_setting": {
        "korean_name": "수분장력설정",
        "type": "BIT_RANGE_WRITE",
        "address": 13,
        "bit_start": 8,
        "bit_end": 15,
        "unit": "-",
        "description": "수분장력설정 (수분장력설정)"
    },

    "soil_tension_enable": {
        "korean_name": "수분장력사용",
        "type": "BIT_WRITE",
        "address": 13,
        "bit": 6,
        "unit": "-",
        "description": "수분장력사용 (수분장력사용)"
    },

    "irrigation_start_minute": {
        "korean_name": "관수시작분",
        "type": "BIT_RANGE_WRITE",
        "address": 13,
        "bit_start": 0,
        "bit_end": 5,
        "unit": "분",
        "description": "관수 시작시각(분) (관수시작분)"
    },

    # ========================================================================
    # Word Address 14~17: Heating
    # ========================================================================

    "heating_on_humidity_setting": {
        "korean_name": "난방ON습도설정",
        "type": "BIT_RANGE_WRITE",
        "address": 14,
        "bit_start": 2,
        "bit_end": 15,
        "unit": "-",
        "description": "난방 ON 습도설정값 (난방ON습도설정)"
    },

    "heating_forced_operation": {
        "korean_name": "난방강제운전",
        "type": "BIT_WRITE",
        "address": 14,
        "bit": 1,
        "unit": "-",
        "description": "난방강제운전 (난방강제운전)"
    },

    "heating_auto_mode": {
        "korean_name": "난방오토모드",
        "type": "BIT_WRITE",
        "address": 14,
        "bit": 0,
        "unit": "-",
        "description": "난방오토모드 (난방오토모드)"
    },

    "heating_off_humidity_setting": {
        "korean_name": "난방OFF습도설정",
        "type": "BIT_RANGE_WRITE",
        "address": 15,
        "bit_start": 2,
        "bit_end": 15,
        "unit": "-",
        "description": "난방 OFF 습도설정값 (난방OFF습도설정)"
    },

    "heating_humidity_condition_enable": {
        "korean_name": "난방습도조건사용",
        "type": "BIT_WRITE",
        "address": 15,
        "bit": 1,
        "unit": "-",
        "description": "난방습도조건사용 (난방습도조건사용)"
    },

    "heating_temperature_condition_enable": {
        "korean_name": "난방온도조건사용",
        "type": "BIT_WRITE",
        "address": 15,
        "bit": 0,
        "unit": "-",
        "description": "난방온도조건사용 (난방온도조건사용)"
    },

    "heating_on_temperature_setting": {
        "korean_name": "난방ON온도설정",
        "type": "REGISTER_WRITE",
        "address": 16,
        "scale": 10,
        "unit": "°C",
        "description": "난방 ON 온도설정값 (난방ON온도설정)"
    },

    "heating_off_temperature_setting": {
        "korean_name": "난방OFF온도설정",
        "type": "REGISTER_WRITE",
        "address": 17,
        "scale": 10,
        "unit": "°C",
        "description": "난방 OFF 온도설정값 (난방OFF온도설정)"
    },

    # ========================================================================
    # Word Address 18~19: Dehumidification
    # ========================================================================

    "dehumidifier_on_setting": {
        "korean_name": "제습ON설정",
        "type": "BIT_RANGE_WRITE",
        "address": 18,
        "bit_start": 1,
        "bit_end": 15,
        "unit": "-",
        "description": "제습 ON설정값 (제습ON설정)"
    },

    "dehumidifier_auto_mode": {
        "korean_name": "제습오토모드",
        "type": "BIT_WRITE",
        "address": 18,
        "bit": 0,
        "unit": "-",
        "description": "제습오토모드 (제습오토모드)"
    },

    "dehumidifier_off_setting": {
        "korean_name": "제습OFF설정",
        "type": "BIT_RANGE_WRITE",
        "address": 19,
        "bit_start": 1,
        "bit_end": 15,
        "unit": "-",
        "description": "제습 OFF설정값 (제습OFF설정)"
    },

    "dehumidifier_forced_operation": {
        "korean_name": "제습강제운전",
        "type": "BIT_WRITE",
        "address": 19,
        "bit": 0,
        "unit": "-",
        "description": "제습강제운전 (제습강제운전)"
    },

    # ========================================================================
    # Word Address 20~28: Roof Control
    # ========================================================================

    "right_close_mode": {
        "korean_name": "우측닫기모드",
        "type": "BIT_WRITE",
        "address": 20,
        "bit": 15,
        "unit": "-",
        "description": "우측닫기모드 (우측닫기모드)"
    },

    "right_open_mode": {
        "korean_name": "우측열기모드",
        "type": "BIT_WRITE",
        "address": 20,
        "bit": 14,
        "unit": "-",
        "description": "우측열기모드 (우측열기모드)"
    },

    "right_auto_mode": {
        "korean_name": "우측오토모드",
        "type": "BIT_WRITE",
        "address": 20,
        "bit": 13,
        "unit": "-",
        "description": "우측오토모드 (우측오토모드)"
    },

    "left_close_mode": {
        "korean_name": "좌측닫기모드",
        "type": "BIT_WRITE",
        "address": 20,
        "bit": 12,
        "unit": "-",
        "description": "좌측닫기모드 (좌측닫기모드)"
    },

    "left_open_mode": {
        "korean_name": "좌측열기모드",
        "type": "BIT_WRITE",
        "address": 20,
        "bit": 11,
        "unit": "-",
        "description": "좌측열기모드 (좌측열기모드)"
    },

    "left_auto_mode": {
        "korean_name": "좌측오토모드",
        "type": "BIT_WRITE",
        "address": 20,
        "bit": 10,
        "unit": "-",
        "description": "좌측오토모드 (좌측오토모드)"
    },

    "roof_high_humidity_open_setting": {
        "korean_name": "천장고습열림설정",
        "type": "BIT_RANGE_WRITE",
        "address": 20,
        "bit_start": 0,
        "bit_end": 9,
        "unit": "-",
        "description": "천장 고습열림 설정값 (천장고습열림설정)"
    },

    "close_on_rain_when_disabled": {
        "korean_name": "사용안함일때비오면닫기",
        "type": "BIT_WRITE",
        "address": 21,
        "bit": 15,
        "unit": "-",
        "description": "사용안함일때 비오면 닫기기능 (사용안함일때비오면닫기)"
    },

    "close_on_rain_when_forced_open": {
        "korean_name": "강제열기일때비오면닫기",
        "type": "BIT_WRITE",
        "address": 21,
        "bit": 14,
        "unit": "-",
        "description": "강제열기일때 비오면 닫기기능 (강제열기일때비오면닫기)"
    },

    "roof_temperature_diff_condition_enable": {
        "korean_name": "천장개폐온도차조건사용",
        "type": "BIT_WRITE",
        "address": 21,
        "bit": 13,
        "unit": "-",
        "description": "천장개폐 온도차조건사용 (천장개폐온도차조건사용)"
    },

    "roof_humidity_condition_enable": {
        "korean_name": "천장개폐습도조건사용",
        "type": "BIT_WRITE",
        "address": 21,
        "bit": 12,
        "unit": "-",
        "description": "천장개폐 습도조건사용 (천장개폐습도조건사용)"
    },

    "roof_temperature_condition_enable": {
        "korean_name": "천장개폐온도조건사용",
        "type": "BIT_WRITE",
        "address": 21,
        "bit": 11,
        "unit": "-",
        "description": "천장개폐 온도조건사용 (천장개폐온도조건사용)"
    },

    "roof_wind_speed_condition_enable": {
        "korean_name": "천장개폐풍속조건사용",
        "type": "BIT_WRITE",
        "address": 21,
        "bit": 10,
        "unit": "-",
        "description": "천장개폐 풍속조건 사용 (천장개폐풍속조건사용)"
    },

    "roof_time_condition_enable": {
        "korean_name": "천장개폐시간조건사용",
        "type": "BIT_WRITE",
        "address": 21,
        "bit": 9,
        "unit": "-",
        "description": "천장개폐 시간조건 사용 (천장개폐시간조건사용)"
    },

    "open_close_temperature_deviation": {
        "korean_name": "열기닫기편차온도",
        "type": "BIT_RANGE_WRITE",
        "address": 21,
        "bit_start": 0,
        "bit_end": 8,
        "unit": "-",
        "description": "열기닫기 편차온도 (열기닫기편차온도)"
    },

    "high_humidity_open_setting_value": {
        "korean_name": "고습열림설정값",
        "type": "REGISTER_WRITE",
        "address": 22,
        "scale": 10,
        "unit": "%",
        "description": "고습열림 설정값 (고습열림설정값)"
    },

    "temperature_diff_open_close_deviation": {
        "korean_name": "온도차조건열기닫기편차온도",
        "type": "REGISTER_WRITE",
        "address": 23,
        "scale": 10,
        "unit": "°C",
        "description": "온도차 조건 사용시 열기 닫기 편차온도 (온도차조건열기닫기편차온도)"
    },

    "temperature_diff_open_setting_value": {
        "korean_name": "온도차열기설정값",
        "type": "REGISTER_WRITE",
        "address": 24,
        "scale": 10,
        "unit": "°C",
        "description": "온도차 열기 설정값 (온도차열기설정값)"
    },

    "open_temperature_setting": {
        "korean_name": "열림설정온도",
        "type": "REGISTER_WRITE",
        "address": 25,
        "scale": 10,
        "unit": "°C",
        "description": "열림 설정온도 (열림설정온도)"
    },

    "close_temperature_setting": {
        "korean_name": "닫힘설정온도",
        "type": "REGISTER_WRITE",
        "address": 26,
        "scale": 10,
        "unit": "°C",
        "description": "닫힘 설정온도 (닫힘설정온도)"
    },

    "roof_close_time": {
        "korean_name": "천장개폐닫힘시간",
        "type": "BIT_RANGE_WRITE",
        "address": 27,
        "bit_start": 8,
        "bit_end": 15,
        "unit": "-",
        "description": "천장개폐 닫힘시간 (천장개폐닫힘시간)"
    },

    "roof_open_time": {
        "korean_name": "천장개폐열림시간",
        "type": "BIT_RANGE_WRITE",
        "address": 27,
        "bit_start": 0,
        "bit_end": 7,
        "unit": "-",
        "description": "천장개폐 열림시간 (천장개폐열림시간)"
    },

    "close_on_strong_wind_when_disabled": {
        "korean_name": "사용안함일때강풍이면닫기사용",
        "type": "BIT_WRITE",
        "address": 28,
        "bit": 15,
        "unit": "-",
        "description": "사용안함일 때 강풍이면 닫기사용 (사용안함일때강풍이면닫기사용)"
    },

    "strong_wind_close_deviation": {
        "korean_name": "강풍닫기편차",
        "type": "BIT_RANGE_WRITE",
        "address": 28,
        "bit_start": 8,
        "bit_end": 14,
        "unit": "-",
        "description": "강풍닫기 편차 (강풍닫기편차)"
    },

    "close_on_strong_wind_when_forced_open": {
        "korean_name": "강제열기일때강풍이면닫기사용",
        "type": "BIT_WRITE",
        "address": 28,
        "bit": 7,
        "unit": "-",
        "description": "강제열기일 때 강풍이면 닫기사용 (강제열기일때강풍이면닫기사용)"
    },

    "strong_wind_close_wind_speed_setting": {
        "korean_name": "강풍닫기설정풍속",
        "type": "BIT_RANGE_WRITE",
        "address": 28,
        "bit_start": 0,
        "bit_end": 6,
        "unit": "-",
        "description": "강풍닫기 설정풍속 (강풍닫기설정풍속)"
    },

    # ========================================================================
    # Word Address 29~37: Insulation Curtain
    # ========================================================================

    "insulation_curtain_time_condition_enable": {
        "korean_name": "보온커튼시간조건사용",
        "type": "BIT_WRITE",
        "address": 29,
        "bit": 15,
        "unit": "-",
        "description": "보온커튼시간조건사용 (보온커튼시간조건사용)"
    },

    "insulation_curtain_temperature_condition_enable": {
        "korean_name": "보온커튼온도조건사용",
        "type": "BIT_WRITE",
        "address": 29,
        "bit": 14,
        "unit": "-",
        "description": "보온커튼온도조건사용 (보온커튼온도조건사용)"
    },

    "unused_29": {
        "korean_name": "사용안함_29",
        "type": "BIT_WRITE",
        "address": 29,
        "bit": 13,
        "unit": "-",
        "description": "사용안함 (사용안함_29)"
    },

    "insulation_curtain_close_time": {
        "korean_name": "보온커튼닫힘시각",
        "type": "BIT_RANGE_WRITE",
        "address": 29,
        "bit_start": 8,
        "bit_end": 12,
        "unit": "시",
        "description": "보온커튼 닫힘 시각 (보온커튼닫힘시각)"
    },

    "upper_insulation_curtain_close_mode": {
        "korean_name": "상부보온커튼닫기모드",
        "type": "BIT_WRITE",
        "address": 29,
        "bit": 7,
        "unit": "-",
        "description": "상부보온커튼 닫기모드 (상부보온커튼닫기모드)"
    },

    "upper_insulation_curtain_open_mode": {
        "korean_name": "상부보온커튼열기모드",
        "type": "BIT_WRITE",
        "address": 29,
        "bit": 6,
        "unit": "-",
        "description": "상부보온커튼 열기모드 (상부보온커튼열기모드)"
    },

    "upper_insulation_curtain_auto_mode": {
        "korean_name": "상부보온커튼오토모드",
        "type": "BIT_WRITE",
        "address": 29,
        "bit": 5,
        "unit": "-",
        "description": "상부보온커튼 오토모드 (상부보온커튼오토모드)"
    },

    "insulation_curtain_open_time": {
        "korean_name": "보온커튼열림시각",
        "type": "BIT_RANGE_WRITE",
        "address": 29,
        "bit_start": 0,
        "bit_end": 4,
        "unit": "시",
        "description": "보온커튼 열림시각 (보온커튼열림시각)"
    },

    "unused_30": {
        "korean_name": "사용안함_30",
        "type": "BIT_RANGE_WRITE",
        "address": 30,
        "bit_start": 3,
        "bit_end": 15,
        "unit": "-",
        "description": "사용안함 (사용안함_30)"
    },

    "side_insulation_curtain_close_mode": {
        "korean_name": "측면보온커튼닫기모드",
        "type": "BIT_WRITE",
        "address": 30,
        "bit": 2,
        "unit": "-",
        "description": "측면보온커튼 닫기모드 (측면보온커튼닫기모드)"
    },

    "side_insulation_curtain_open_mode": {
        "korean_name": "측면보온커튼열기모드",
        "type": "BIT_WRITE",
        "address": 30,
        "bit": 1,
        "unit": "-",
        "description": "측면보온커튼 열기모드 (측면보온커튼열기모드)"
    },

    "side_insulation_curtain_auto_mode": {
        "korean_name": "측면보온커튼오토모드",
        "type": "BIT_WRITE",
        "address": 30,
        "bit": 0,
        "unit": "-",
        "description": "측면보온커튼 오토모드 (측면보온커튼오토모드)"
    },

    "insulation_curtain_open_temperature_setting": {
        "korean_name": "보온커튼열림온도설정",
        "type": "REGISTER_WRITE",
        "address": 31,
        "scale": 10,
        "unit": "°C",
        "description": "보온커튼 열림온도설정 (보온커튼열림온도설정)"
    },

    "insulation_curtain_close_temperature_setting": {
        "korean_name": "보온커튼닫힘온도설정",
        "type": "REGISTER_WRITE",
        "address": 32,
        "scale": 10,
        "unit": "°C",
        "description": "보온커튼 닫힘온도설정 (보온커튼닫힘온도설정)"
    },

    "insulation_curtain_open_close_temperature_deviation": {
        "korean_name": "보온커튼열기닫기편차온도",
        "type": "REGISTER_WRITE",
        "address": 33,
        "scale": 10,
        "unit": "°C",
        "description": "보온커튼 열기닫기 편차온도 (보온커튼열기닫기편차온도)"
    },

    "upper_insulation_curtain_total_travel_time_setting": {
        "korean_name": "상부보온커튼전체이동시간설정",
        "type": "REGISTER_WRITE",
        "address": 34,
        "scale": 1,
        "unit": "초",
        "description": "상부보온커튼 전체이동시간 설정 (상부보온커튼전체이동시간설정)"
    },

    "upper_insulation_curtain_open_limit_ratio": {
        "korean_name": "상부보온커튼열림제한비율",
        "type": "REGISTER_WRITE",
        "address": 35,
        "scale": 1,
        "unit": "%",
        "description": "상부보온커튼 열림제한비율 (상부보온커튼열림제한비율)"
    },

    "side_insulation_curtain_total_travel_time_setting": {
        "korean_name": "측면보온커튼전체이동시간설정",
        "type": "REGISTER_WRITE",
        "address": 36,
        "scale": 1,
        "unit": "초",
        "description": "측면보온커튼 전체이동시간 설정 (측면보온커튼전체이동시간설정)"
    },

    "side_insulation_curtain_open_limit_ratio": {
        "korean_name": "측면보온커튼열림제한비율",
        "type": "REGISTER_WRITE",
        "address": 37,
        "scale": 1,
        "unit": "%",
        "description": "측면보온커튼 열림제한비율 (측면보온커튼열림제한비율)"
    },

    # ========================================================================
    # Word Address 38~44: Shading Curtain
    # ========================================================================

    "shading_curtain_time_condition_enable": {
        "korean_name": "차광커튼시간조건사용",
        "type": "BIT_WRITE",
        "address": 38,
        "bit": 15,
        "unit": "-",
        "description": "차광커튼시간조건사용 (차광커튼시간조건사용)"
    },

    "shading_curtain_temperature_condition_enable": {
        "korean_name": "차광커튼온도조건사용",
        "type": "BIT_WRITE",
        "address": 38,
        "bit": 14,
        "unit": "-",
        "description": "차광커튼온도조건사용 (차광커튼온도조건사용)"
    },

    "unused_38": {
        "korean_name": "사용안함_38",
        "type": "BIT_WRITE",
        "address": 38,
        "bit": 13,
        "unit": "-",
        "description": "사용안함 (사용안함_38)"
    },

    "shading_curtain_close_time": {
        "korean_name": "차광커튼닫힘시각",
        "type": "BIT_RANGE_WRITE",
        "address": 38,
        "bit_start": 8,
        "bit_end": 12,
        "unit": "시",
        "description": "차광커튼 닫힘시각 (차광커튼닫힘시각)"
    },

    "shading_curtain_close_mode": {
        "korean_name": "차광커튼닫기모드",
        "type": "BIT_WRITE",
        "address": 38,
        "bit": 7,
        "unit": "-",
        "description": "차광커튼 닫기모드 (차광커튼닫기모드)"
    },

    "shading_curtain_open_mode": {
        "korean_name": "차광커튼열기모드",
        "type": "BIT_WRITE",
        "address": 38,
        "bit": 6,
        "unit": "-",
        "description": "차광커튼 열기모드 (차광커튼열기모드)"
    },

    "shading_curtain_auto_mode": {
        "korean_name": "차광커튼오토모드",
        "type": "BIT_WRITE",
        "address": 38,
        "bit": 5,
        "unit": "-",
        "description": "차광커튼 오토모드 (차광커튼오토모드)"
    },

    "shading_curtain_open_time": {
        "korean_name": "차광커튼열림시각",
        "type": "BIT_RANGE_WRITE",
        "address": 38,
        "bit_start": 0,
        "bit_end": 4,
        "unit": "시",
        "description": "차광커튼 열림시각 (차광커튼열림시각)"
    },

    "solar_radiation_sensor_condition_enable": {
        "korean_name": "일사센서조건사용",
        "type": "BIT_WRITE",
        "address": 39,
        "bit": 15,
        "unit": "-",
        "description": "일사센서조건사용 (일사센서조건사용)"
    },

    "shading_curtain_total_travel_time": {
        "korean_name": "차광커튼전체이동시간",
        "type": "BIT_RANGE_WRITE",
        "address": 39,
        "bit_start": 0,
        "bit_end": 14,
        "unit": "초",
        "description": "차광커튼 전체이동시간 (차광커튼전체이동시간)"
    },

    "shading_curtain_high_temperature_open_setting": {
        "korean_name": "차광커튼고온열림설정온도",
        "type": "REGISTER_WRITE",
        "address": 40,
        "scale": 10,
        "unit": "°C",
        "description": "차광커튼 고온열림 설정온도 (차광커튼고온열림설정온도)"
    },

    "shading_curtain_close_solar_radiation_setting": {
        "korean_name": "차광커튼닫힘일사량설정",
        "type": "REGISTER_WRITE",
        "address": 41,
        "scale": 1,
        "unit": "W/m²",
        "description": "차광커튼 닫힘일사량 설정 (차광커튼닫힘일사량설정)"
    },

    "shading_curtain_solar_sensor_open_close_deviation": {
        "korean_name": "차광커튼일사센서열기닫기편차값",
        "type": "REGISTER_WRITE",
        "address": 42,
        "scale": 1,
        "unit": "W/m²",
        "description": "차광커튼 일사센서에 의한 열기 닫기 편차값 (차광커튼일사센서열기닫기편차값)"
    },

    "shading_curtain_high_temp_open_close_deviation": {
        "korean_name": "차광커튼고온열기닫기편차값",
        "type": "REGISTER_WRITE",
        "address": 43,
        "scale": 10,
        "unit": "°C",
        "description": "차광커튼 고온에 의한 열기 닫기 편차값 (차광커튼고온열기닫기편차값)"
    },

    "shading_curtain_open_limit_ratio": {
        "korean_name": "차광커튼열림제한비율",
        "type": "REGISTER_WRITE",
        "address": 44,
        "scale": 1,
        "unit": "%",
        "description": "차광커튼 열림제한비율 (차광커튼열림제한비율)"
    },

    # ========================================================================
    # Word Address 45~46: Lighting
    # ========================================================================

    "lighting_on_time_minute": {
        "korean_name": "조명온시각분",
        "type": "BIT_RANGE_WRITE",
        "address": 45,
        "bit_start": 8,
        "bit_end": 15,
        "unit": "분",
        "description": "조명 온시각 분 (조명온시각분)"
    },

    "lighting_on_time_hour": {
        "korean_name": "조명온시각시",
        "type": "BIT_RANGE_WRITE",
        "address": 45,
        "bit_start": 1,
        "bit_end": 7,
        "unit": "시",
        "description": "조명 온시각 시 (조명온시각시)"
    },

    "lighting_auto_mode": {
        "korean_name": "조명오토모드",
        "type": "BIT_WRITE",
        "address": 45,
        "bit": 0,
        "unit": "-",
        "description": "조명오토모드 (조명오토모드)"
    },

    "lighting_off_time_minute": {
        "korean_name": "조명오프시각분",
        "type": "BIT_RANGE_WRITE",
        "address": 46,
        "bit_start": 8,
        "bit_end": 15,
        "unit": "분",
        "description": "조명 오프시각 분 (조명오프시각분)"
    },

    "lighting_off_time_hour": {
        "korean_name": "조명오프시각시",
        "type": "BIT_RANGE_WRITE",
        "address": 46,
        "bit_start": 1,
        "bit_end": 7,
        "unit": "시",
        "description": "조명 오프시각 시 (조명오프시각시)"
    },

    "lighting_forced_operation": {
        "korean_name": "조명강제운전",
        "type": "BIT_WRITE",
        "address": 46,
        "bit": 0,
        "unit": "-",
        "description": "조명강제운전 (조명강제운전)"
    },

    # ========================================================================
    # Word Address 47~57: Sensor Calibration
    # ========================================================================

    "internal_temperature_sensor_calibration": {
        "korean_name": "내부온도센서보정값",
        "type": "REGISTER_WRITE",
        "address": 47,
        "scale": 10,
        "unit": "°C",
        "description": "내부온도 센서 보정값 (내부온도센서보정값)"
    },

    "internal_humidity_sensor_calibration": {
        "korean_name": "내부습도센서보정값",
        "type": "REGISTER_WRITE",
        "address": 48,
        "scale": 10,
        "unit": "%",
        "description": "내부습도 센서 보정값 (내부습도센서보정값)"
    },

    "internal_solar_radiation_sensor_calibration": {
        "korean_name": "내부일사센서보정값",
        "type": "REGISTER_WRITE",
        "address": 49,
        "scale": 1,
        "unit": "W/m²",
        "description": "내부 일사센서 보정값 (내부일사센서보정값)"
    },

    "internal_moisture_sensor_calibration": {
        "korean_name": "내부함수율센서보정값",
        "type": "REGISTER_WRITE",
        "address": 50,
        "scale": 1,
        "unit": "%",
        "description": "내부 함수율 센서 보정값 (내부함수율센서보정값)"
    },

    "internal_soil_tension_sensor_calibration": {
        "korean_name": "내부수분장력센서보정값",
        "type": "REGISTER_WRITE",
        "address": 51,
        "scale": 1,
        "unit": "kPa",
        "description": "내부 수분장력센서 보정값 (내부수분장력센서보정값)"
    },

    "external_temperature_sensor_calibration": {
        "korean_name": "외부온도센서보정값",
        "type": "REGISTER_WRITE",
        "address": 52,
        "scale": 10,
        "unit": "°C",
        "description": "외부온도센서 보정값 (외부온도센서보정값)"
    },

    "external_humidity_sensor_calibration": {
        "korean_name": "외부습도센서보정값",
        "type": "REGISTER_WRITE",
        "address": 53,
        "scale": 10,
        "unit": "%",
        "description": "외부습도센서 보정값 (외부습도센서보정값)"
    },

    "external_solar_radiation_sensor_calibration": {
        "korean_name": "외부일사센서보정값",
        "type": "REGISTER_WRITE",
        "address": 54,
        "scale": 1,
        "unit": "W/m²",
        "description": "외부 일사센서 보정값 (외부일사센서보정값)"
    },

    "external_wind_direction_sensor_calibration": {
        "korean_name": "외부풍향센서보정값",
        "type": "REGISTER_WRITE",
        "address": 55,
        "scale": 1,
        "unit": "°",
        "description": "외부 풍향센서 보정값 (외부풍향센서보정값)"
    },

    "external_wind_speed_sensor_calibration": {
        "korean_name": "외부풍속센서보정값",
        "type": "REGISTER_WRITE",
        "address": 56,
        "scale": 10,
        "unit": "m/s",
        "description": "외부 풍속센서 보정값 (외부풍속센서보정값)"
    },

    "external_sensor_communication_address": {
        "korean_name": "외부센서통신주소",
        "type": "BIT_RANGE_WRITE",
        "address": 57,
        "bit_start": 8,
        "bit_end": 15,
        "unit": "-",
        "description": "외부센서 통신주소 (외부센서통신주소)"
    },

    "internal_sensor_communication_address": {
        "korean_name": "내부센서통신주소",
        "type": "BIT_RANGE_WRITE",
        "address": 57,
        "bit_start": 0,
        "bit_end": 7,
        "unit": "-",
        "description": "내부센서 통신주소 (내부센서통신주소)"
    },

    # ========================================================================
    # Word Address 58~64: System Information
    # ========================================================================

    "reserved_58": {
        "korean_name": "reserved_58",
        "type": "REGISTER_WRITE",
        "address": 58,
        "scale": 1,
        "unit": "-",
        "description": "reserved (reserved_58)"
    },

    "reserved_59": {
        "korean_name": "reserved_59",
        "type": "REGISTER_WRITE",
        "address": 59,
        "scale": 1,
        "unit": "-",
        "description": "reserved (reserved_59)"
    },

    "io_board_communication_check": {
        "korean_name": "IO보드통신체크",
        "type": "REGISTER_READ",
        "address": 60,
        "scale": 1,
        "unit": "-",
        "description": "IO보드 통신 체크 (100=연결끊김) (IO보드통신체크)"
    },

    "pcb_current_temperature": {
        "korean_name": "PCB주위현재온도",
        "type": "REGISTER_READ",
        "address": 61,
        "scale": 10,
        "unit": "°C",
        "description": "PCB 주위 현재온도 (PCB주위현재온도)"
    },

    "current_time_hour": {
        "korean_name": "현재시각_시",
        "type": "REGISTER_READ",
        "address": 62,
        "scale": 1,
        "unit": "시",
        "description": "현재시각(시) (현재시각_시)"
    },

    "current_time_minute": {
        "korean_name": "현재시각_분",
        "type": "REGISTER_READ",
        "address": 63,
        "scale": 1,
        "unit": "분",
        "description": "현재 분 (현재시각_분)"
    },

    "current_time_second": {
        "korean_name": "현재시각_초",
        "type": "REGISTER_READ",
        "address": 64,
        "scale": 1,
        "unit": "초",
        "description": "현재 초 (현재시각_초)"
    },

    # ========================================================================
    # Word Address 65~67: Output Status
    # ========================================================================

    "circulation_fan_humidity_condition_output_active": {
        "korean_name": "유동팬습도조건출력중",
        "type": "BIT_READ",
        "address": 65,
        "bit": 15,
        "unit": "-",
        "description": "유동팬습도조건에 의한 출력중 (유동팬습도조건출력중)"
    },

    "circulation_fan_temperature_condition_output_active": {
        "korean_name": "유동팬온도조건출력중",
        "type": "BIT_READ",
        "address": 65,
        "bit": 14,
        "unit": "-",
        "description": "유동팬온도조건에 의한 출력중 (유동팬온도조건출력중)"
    },

    "shading_open_output_indicator": {
        "korean_name": "차광열림출력표시",
        "type": "BIT_READ",
        "address": 65,
        "bit": 13,
        "unit": "-",
        "description": "차광 열림출력 표시 (차광열림출력표시)"
    },

    "shading_close_output_indicator": {
        "korean_name": "차광닫힘출력표시",
        "type": "BIT_READ",
        "address": 65,
        "bit": 12,
        "unit": "-",
        "description": "차광 닫힘출력 표시 (차광닫힘출력표시)"
    },

    "upper_insulation_open_output_indicator": {
        "korean_name": "상부보온열림출력표시",
        "type": "BIT_READ",
        "address": 65,
        "bit": 11,
        "unit": "-",
        "description": "상부보온 열림출력 표시 (상부보온열림출력표시)"
    },

    "upper_insulation_close_output_indicator": {
        "korean_name": "상부보온닫힘출력표시",
        "type": "BIT_READ",
        "address": 65,
        "bit": 10,
        "unit": "-",
        "description": "상부보온 닫힘출력 표시 (상부보온닫힘출력표시)"
    },

    "roof_right_end_open_output_indicator": {
        "korean_name": "천장우단열림출력표시",
        "type": "BIT_READ",
        "address": 65,
        "bit": 9,
        "unit": "-",
        "description": "천장우단 열림출력 표시 (천장우단열림출력표시)"
    },

    "roof_right_open_output_indicator": {
        "korean_name": "천장우열림출력표시",
        "type": "BIT_READ",
        "address": 65,
        "bit": 8,
        "unit": "-",
        "description": "천장우 열림출력 표시 (천장우열림출력표시)"
    },

    "roof_left_end_open_output_indicator": {
        "korean_name": "천장좌단열림출력표시",
        "type": "BIT_READ",
        "address": 65,
        "bit": 7,
        "unit": "-",
        "description": "천장좌단 열림출력 표시 (천장좌단열림출력표시)"
    },

    "roof_left_open_output_indicator": {
        "korean_name": "천장좌열림출력표시",
        "type": "BIT_READ",
        "address": 65,
        "bit": 6,
        "unit": "-",
        "description": "천장좌 열림출력 표시 (천장좌열림출력표시)"
    },

    "dehumidifier_output_indicator": {
        "korean_name": "제습출력표시",
        "type": "BIT_READ",
        "address": 65,
        "bit": 5,
        "unit": "-",
        "description": "제습출력 표시 (제습출력표시)"
    },

    "heating_output_indicator": {
        "korean_name": "난방출력표시",
        "type": "BIT_READ",
        "address": 65,
        "bit": 4,
        "unit": "-",
        "description": "난방출력 표시 (난방출력표시)"
    },

    "irrigation_output_indicator": {
        "korean_name": "관수출력표시",
        "type": "BIT_READ",
        "address": 65,
        "bit": 3,
        "unit": "-",
        "description": "관수출력 표시 (관수출력표시)"
    },

    "circulation_fan_output_indicator": {
        "korean_name": "유동팬출력표시",
        "type": "BIT_READ",
        "address": 65,
        "bit": 2,
        "unit": "-",
        "description": "유동팬출력 표시 (유동팬출력표시)"
    },

    "pcb_temperature_sensor_error": {
        "korean_name": "PCB온도센서에러",
        "type": "BIT_READ",
        "address": 65,
        "bit": 1,
        "unit": "-",
        "description": "PCB온도센서 에러 (PCB온도센서에러)"
    },

    "factory_reset_check": {
        "korean_name": "생정초기화체크",
        "type": "BIT_READ",
        "address": 65,
        "bit": 0,
        "unit": "-",
        "description": "생정초기화 체크 (생정초기화체크)"
    },

    "irrigation_in_progress": {
        "korean_name": "관수중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 15,
        "unit": "-",
        "description": "관수 중 (관수중)"
    },

    "rain_sensor_detecting": {
        "korean_name": "감우센서감지중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 14,
        "unit": "-",
        "description": "감우센서 감지중 (감우센서감지중)"
    },

    "shading_solar_sensor_output_active": {
        "korean_name": "차광일사센서출력중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 13,
        "unit": "-",
        "description": "차광:일사센서에 의한 출력중 (차광일사센서출력중)"
    },

    "shading_time_condition_output_active": {
        "korean_name": "차광시간조건출력중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 12,
        "unit": "-",
        "description": "차광:시간조건에 의한 출력중 (차광시간조건출력중)"
    },

    "shading_temperature_condition_output_active": {
        "korean_name": "차광온도조건출력중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 11,
        "unit": "-",
        "description": "차광:온도조건에 의한 출력중 (차광온도조건출력중)"
    },

    "insulation_time_condition_output_active": {
        "korean_name": "보온시간조건출력중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 10,
        "unit": "-",
        "description": "보온:시간조건에 의한 출력중 (보온시간조건출력중)"
    },

    "insulation_temperature_condition_output_active": {
        "korean_name": "보온온도조건출력중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 9,
        "unit": "-",
        "description": "보온:온도조건에 의한 출력중 (보온온도조건출력중)"
    },

    "roof_left_rain_condition_output_active": {
        "korean_name": "천장좌감우조건출력중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 8,
        "unit": "-",
        "description": "천장좌:감우조건에 의한 출력중 (천장좌감우조건출력중)"
    },

    "roof_left_temperature_diff_condition_output_active": {
        "korean_name": "천장좌온도차조건출력중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 7,
        "unit": "-",
        "description": "천장좌:온도차조건에 의한 출력중 (천장좌온도차조건출력중)"
    },

    "roof_left_humidity_condition_output_active": {
        "korean_name": "천장좌습도조건출력중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 6,
        "unit": "-",
        "description": "천장좌:습도조건에 의한 출력중 (천장좌습도조건출력중)"
    },

    "roof_left_temperature_condition_output_active": {
        "korean_name": "천장좌온도조건출력중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 5,
        "unit": "-",
        "description": "천장좌:온도조건에 의한 출력중 (천장좌온도조건출력중)"
    },

    "heating_humidity_condition_output_active": {
        "korean_name": "난방습도조건출력중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 4,
        "unit": "-",
        "description": "난방:습도조건에 의한 출력중 (난방습도조건출력중)"
    },

    "heating_temperature_condition_output_active": {
        "korean_name": "난방온도조건출력중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 3,
        "unit": "-",
        "description": "난방:온도조건에 의한 출력중 (난방온도조건출력중)"
    },

    "irrigation_time_condition_output_active": {
        "korean_name": "관수시간조건출력중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 2,
        "unit": "-",
        "description": "관수:시간조건에 의한 출력중 (관수시간조건출력중)"
    },

    "irrigation_moisture_output_active": {
        "korean_name": "관수함수율출력중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 1,
        "unit": "-",
        "description": "관수:함수율에 의한 출력중 (관수함수율출력중)"
    },

    "circulation_fan_time_condition_output_active": {
        "korean_name": "유동팬시간조건출력중",
        "type": "BIT_READ",
        "address": 66,
        "bit": 0,
        "unit": "-",
        "description": "유동팬:시간조건에 의한 출력중 (유동팬시간조건출력중)"
    },

    "reserved_67_15": {
        "korean_name": "reserved_67_15",
        "type": "BIT_READ",
        "address": 67,
        "bit": 15,
        "unit": "-",
        "description": "reserved (reserved_67_15)"
    },

    "side_insulation_curtain_close_output_indicator": {
        "korean_name": "측면보온커튼닫힘출력표시",
        "type": "BIT_READ",
        "address": 67,
        "bit": 14,
        "unit": "-",
        "description": "측면보온커튼 닫힘출력 표시 (측면보온커튼닫힘출력표시)"
    },

    "side_insulation_curtain_open_output_indicator": {
        "korean_name": "측면보온커튼열림출력표시",
        "type": "BIT_READ",
        "address": 67,
        "bit": 13,
        "unit": "-",
        "description": "측면보온커튼 열림출력 표시 (측면보온커튼열림출력표시)"
    },

    "roof_right_wind_speed_output_active": {
        "korean_name": "천장우풍속출력중",
        "type": "BIT_READ",
        "address": 67,
        "bit": 12,
        "unit": "-",
        "description": "천장우 풍속에 의한 출력중 (천장우풍속출력중)"
    },

    "roof_right_time_output_active": {
        "korean_name": "천장우시간출력중",
        "type": "BIT_READ",
        "address": 67,
        "bit": 11,
        "unit": "-",
        "description": "천장우 시간에 의한 출력중 (천장우시간출력중)"
    },

    "roof_left_wind_speed_output_active": {
        "korean_name": "천장좌풍속출력중",
        "type": "BIT_READ",
        "address": 67,
        "bit": 10,
        "unit": "-",
        "description": "천장좌 풍속에 의한 출력중 (천장좌풍속출력중)"
    },

    "roof_left_time_output_active": {
        "korean_name": "천장좌시간출력중",
        "type": "BIT_READ",
        "address": 67,
        "bit": 9,
        "unit": "-",
        "description": "천장좌 시간에 의한 출력중 (천장좌시간출력중)"
    },

    "lighting_output_indicator": {
        "korean_name": "조명출력표시",
        "type": "BIT_READ",
        "address": 67,
        "bit": 8,
        "unit": "-",
        "description": "조명출력 표시 (조명출력표시)"
    },

    "roof_right_rain_condition_output_active": {
        "korean_name": "천장우감우조건출력중",
        "type": "BIT_READ",
        "address": 67,
        "bit": 7,
        "unit": "-",
        "description": "천장우:감우조건에 의한 출력중 (천장우감우조건출력중)"
    },

    "roof_right_temperature_diff_condition_output_active": {
        "korean_name": "천장우온도차조건출력중",
        "type": "BIT_READ",
        "address": 67,
        "bit": 6,
        "unit": "-",
        "description": "천장우:온도차조건에 의한 출력중 (천장우온도차조건출력중)"
    },

    "roof_right_humidity_condition_output_active": {
        "korean_name": "천장우습도조건출력중",
        "type": "BIT_READ",
        "address": 67,
        "bit": 5,
        "unit": "-",
        "description": "천장우:습도조건에 의한 출력중 (천장우습도조건출력중)"
    },

    "roof_right_temperature_condition_output_active": {
        "korean_name": "천장우온도조건출력중",
        "type": "BIT_READ",
        "address": 67,
        "bit": 4,
        "unit": "-",
        "description": "천장우:온도조건에 의한 출력중 (천장우온도조건출력중)"
    },

    "irrigation_repeat_count_indicator": {
        "korean_name": "관수반복횟수표시",
        "type": "BIT_READ",
        "address": 67,
        "bit": 3,
        "unit": "-",
        "description": "관수 반복 몇회 중인지 표시 (관수반복횟수표시)"
    },

    "reserved_67_2": {
        "korean_name": "reserved_67_2",
        "type": "BIT_READ",
        "address": 67,
        "bit": 2,
        "unit": "-",
        "description": "reserved (reserved_67_2)"
    },

    "reserved_67_1": {
        "korean_name": "reserved_67_1",
        "type": "BIT_READ",
        "address": 67,
        "bit": 1,
        "unit": "-",
        "description": "reserved (reserved_67_1)"
    },

    "reserved_67_0": {
        "korean_name": "reserved_67_0",
        "type": "BIT_READ",
        "address": 67,
        "bit": 0,
        "unit": "-",
        "description": "reserved (reserved_67_0)"
    },

    # ========================================================================
    # Word Address 68~69: Sensor Errors
    # ========================================================================

    "internal_sensor_info_15": {
        "korean_name": "내부센서정보_15",
        "type": "BIT_READ",
        "address": 68,
        "bit": 15,
        "unit": "-",
        "description": "내부센서 정보 (내부센서정보_15)"
    },

    "internal_sensor_info_14": {
        "korean_name": "내부센서정보_14",
        "type": "BIT_READ",
        "address": 68,
        "bit": 14,
        "unit": "-",
        "description": "내부센서 정보 (내부센서정보_14)"
    },

    "internal_sensor_time_output_active": {
        "korean_name": "내부센서시간출력중",
        "type": "BIT_READ",
        "address": 68,
        "bit": 13,
        "unit": "-",
        "description": "내부센서 시간에의한출력중 (내부센서시간출력중)"
    },

    "internal_sensor_temperature_output_active": {
        "korean_name": "내부센서온도출력중",
        "type": "BIT_READ",
        "address": 68,
        "bit": 12,
        "unit": "-",
        "description": "내부센서 온도에의한출력중 (내부센서온도출력중)"
    },

    "internal_soil_tension_sensor_error": {
        "korean_name": "내부수분장력센서에러",
        "type": "BIT_READ",
        "address": 68,
        "bit": 11,
        "unit": "-",
        "description": "내부수분장력센서 에러 (내부수분장력센서에러)"
    },

    "internal_moisture_sensor_error": {
        "korean_name": "내부함수율센서에러",
        "type": "BIT_READ",
        "address": 68,
        "bit": 10,
        "unit": "-",
        "description": "내부함수율센서에러 (내부함수율센서에러)"
    },

    "internal_solar_radiation_sensor_error": {
        "korean_name": "내부일사센서에러",
        "type": "BIT_READ",
        "address": 68,
        "bit": 9,
        "unit": "-",
        "description": "내부일사센서에러 (내부일사센서에러)"
    },

    "internal_humidity_sensor_error": {
        "korean_name": "내부습도센서에러",
        "type": "BIT_READ",
        "address": 68,
        "bit": 8,
        "unit": "-",
        "description": "내부습도센서에러 (내부습도센서에러)"
    },

    "internal_temperature_sensor_error": {
        "korean_name": "내부온도센서에러",
        "type": "BIT_READ",
        "address": 68,
        "bit": 7,
        "unit": "-",
        "description": "내부온도센서에러 (내부온도센서에러)"
    },

    "internal_soil_tension_sensor_device_error": {
        "korean_name": "내부수분장력센서디바이스에러",
        "type": "BIT_READ",
        "address": 68,
        "bit": 6,
        "unit": "-",
        "description": "내부수분장력센서 디바이스정보에러 (내부수분장력센서디바이스에러)"
    },

    "internal_moisture_sensor_device_error": {
        "korean_name": "내부함수율센서디바이스에러",
        "type": "BIT_READ",
        "address": 68,
        "bit": 5,
        "unit": "-",
        "description": "내부함수율센서 디바이스정보에러 (내부함수율센서디바이스에러)"
    },

    "internal_solar_radiation_sensor_device_error": {
        "korean_name": "내부일사센서디바이스에러",
        "type": "BIT_READ",
        "address": 68,
        "bit": 4,
        "unit": "-",
        "description": "내부일사센서 디바이스정보에러 (내부일사센서디바이스에러)"
    },

    "internal_humidity_sensor_device_error": {
        "korean_name": "내부습도센서디바이스에러",
        "type": "BIT_READ",
        "address": 68,
        "bit": 3,
        "unit": "-",
        "description": "내부습도센서 디바이스정보에러 (내부습도센서디바이스에러)"
    },

    "internal_temperature_sensor_device_error": {
        "korean_name": "내부온도센서디바이스에러",
        "type": "BIT_READ",
        "address": 68,
        "bit": 2,
        "unit": "-",
        "description": "내부온도센서 디바이스정보에러 (내부온도센서디바이스에러)"
    },

    "internal_sensor_node_error": {
        "korean_name": "내부센서노드에러",
        "type": "BIT_READ",
        "address": 68,
        "bit": 1,
        "unit": "-",
        "description": "내부센서 노드정보에러 (내부센서노드에러)"
    },

    "internal_sensor_communication_error": {
        "korean_name": "내부센서통신에러",
        "type": "BIT_READ",
        "address": 68,
        "bit": 0,
        "unit": "-",
        "description": "내부센서 통신에러 (내부센서통신에러)"
    },

    "external_sensor_info_15": {
        "korean_name": "외부센서정보_15",
        "type": "BIT_READ",
        "address": 69,
        "bit": 15,
        "unit": "-",
        "description": "외부센서 정보 (외부센서정보_15)"
    },

    "external_sensor_info_14": {
        "korean_name": "외부센서정보_14",
        "type": "BIT_READ",
        "address": 69,
        "bit": 14,
        "unit": "-",
        "description": "외부센서 정보 (외부센서정보_14)"
    },

    "external_sensor_error": {
        "korean_name": "외부센서에러",
        "type": "BIT_READ",
        "address": 69,
        "bit": 13,
        "unit": "-",
        "description": "외부센서에러 (외부센서에러)"
    },

    "external_wind_speed_sensor_error": {
        "korean_name": "외부풍속센서에러",
        "type": "BIT_READ",
        "address": 69,
        "bit": 12,
        "unit": "-",
        "description": "외부풍속센서에러 (외부풍속센서에러)"
    },

    "external_wind_direction_sensor_error": {
        "korean_name": "외부풍향센서에러",
        "type": "BIT_READ",
        "address": 69,
        "bit": 11,
        "unit": "-",
        "description": "외부풍향센서에러 (외부풍향센서에러)"
    },

    "external_solar_radiation_sensor_error": {
        "korean_name": "외부일사센서에러",
        "type": "BIT_READ",
        "address": 69,
        "bit": 10,
        "unit": "-",
        "description": "외부일사센서에러 (외부일사센서에러)"
    },

    "external_humidity_sensor_error": {
        "korean_name": "외부습도센서에러",
        "type": "BIT_READ",
        "address": 69,
        "bit": 9,
        "unit": "-",
        "description": "외부습도센서에러 (외부습도센서에러)"
    },

    "external_temperature_sensor_error": {
        "korean_name": "외부온도센서에러",
        "type": "BIT_READ",
        "address": 69,
        "bit": 8,
        "unit": "-",
        "description": "외부온도센서에러 (외부온도센서에러)"
    },

    "external_rain_sensor_error": {
        "korean_name": "외부감우센서에러",
        "type": "BIT_READ",
        "address": 69,
        "bit": 7,
        "unit": "-",
        "description": "외부감우센서에러 (외부감우센서에러)"
    },

    "external_wind_speed_sensor_device_error": {
        "korean_name": "외부풍속센서디바이스에러",
        "type": "BIT_READ",
        "address": 69,
        "bit": 6,
        "unit": "-",
        "description": "외부풍속센서 디바이스정보에러 (외부풍속센서디바이스에러)"
    },

    "external_wind_direction_sensor_device_error": {
        "korean_name": "외부풍향센서디바이스에러",
        "type": "BIT_READ",
        "address": 69,
        "bit": 5,
        "unit": "-",
        "description": "외부풍향센서 디바이스정보에러 (외부풍향센서디바이스에러)"
    },

    "external_solar_radiation_sensor_device_error": {
        "korean_name": "외부일사센서디바이스에러",
        "type": "BIT_READ",
        "address": 69,
        "bit": 4,
        "unit": "-",
        "description": "외부일사센서 디바이스정보에러 (외부일사센서디바이스에러)"
    },

    "external_humidity_sensor_device_error": {
        "korean_name": "외부습도센서디바이스에러",
        "type": "BIT_READ",
        "address": 69,
        "bit": 3,
        "unit": "-",
        "description": "외부습도센서 디바이스정보에러 (외부습도센서디바이스에러)"
    },

    "external_temperature_sensor_device_error": {
        "korean_name": "외부온도센서디바이스에러",
        "type": "BIT_READ",
        "address": 69,
        "bit": 2,
        "unit": "-",
        "description": "외부온도센서 디바이스정보에러 (외부온도센서디바이스에러)"
    },

    "external_sensor_node_error": {
        "korean_name": "외부센서노드에러",
        "type": "BIT_READ",
        "address": 69,
        "bit": 1,
        "unit": "-",
        "description": "외부센서 노드정보에러 (외부센서노드에러)"
    },

    "external_sensor_communication_error": {
        "korean_name": "외부센서통신에러",
        "type": "BIT_READ",
        "address": 69,
        "bit": 0,
        "unit": "-",
        "description": "외부센서 통신에러 (외부센서통신에러)"
    },

    # ========================================================================
    # Word Address 70~79: Current Sensor Values
    # ========================================================================

    "indoor_current_temperature": {
        "korean_name": "내부현재온도",
        "type": "SENSOR_READ",
        "address": 70,
        "scale": 10,
        "unit": "°C",
        "description": "내부 현재온도 (내부현재온도)"
    },

    "indoor_current_humidity": {
        "korean_name": "내부현재습도",
        "type": "SENSOR_READ",
        "address": 71,
        "scale": 10,
        "unit": "%",
        "description": "내부 현재습도 (내부현재습도)"
    },

    "indoor_current_solar_radiation": {
        "korean_name": "내부현재일사량",
        "type": "SENSOR_READ",
        "address": 72,
        "scale": 1,
        "unit": "W/m²",
        "description": "내부 현재일사량 (내부현재일사량)"
    },

    "indoor_current_moisture": {
        "korean_name": "내부현재함수율",
        "type": "SENSOR_READ",
        "address": 73,
        "scale": 1,
        "unit": "%",
        "description": "내부 현재 함수율 (내부현재함수율)"
    },

    "indoor_current_soil_tension": {
        "korean_name": "내부현재수분장력",
        "type": "SENSOR_READ",
        "address": 74,
        "scale": 1,
        "unit": "kPa",
        "description": "내부 현재 수분장력 (내부현재수분장력)"
    },

    "outdoor_current_temperature": {
        "korean_name": "외부현재온도",
        "type": "SENSOR_READ",
        "address": 75,
        "scale": 10,
        "unit": "°C",
        "description": "외부 현재온도 (외부현재온도)"
    },

    "outdoor_current_humidity": {
        "korean_name": "외부현재습도",
        "type": "SENSOR_READ",
        "address": 76,
        "scale": 10,
        "unit": "%",
        "description": "외부 현재습도 (외부현재습도)"
    },

    "outdoor_solar_radiation": {
        "korean_name": "외부일사량",
        "type": "SENSOR_READ",
        "address": 77,
        "scale": 1,
        "unit": "W/m²",
        "description": "외부 일사량 (외부일사량)"
    },

    "outdoor_current_evaporation": {
        "korean_name": "외부현재증발강",
        "type": "SENSOR_READ",
        "address": 78,
        "scale": 1,
        "unit": "-",
        "description": "외부 현재 증발강 (외부현재증발강)"
    },

    "outdoor_current_evaporation_rate": {
        "korean_name": "외부현재증속감",
        "type": "SENSOR_READ",
        "address": 79,
        "scale": 1,
        "unit": "-",
        "description": "외부 현재 증속감 (외부현재증속감)"
    },

    # ========================================================================
    # Word Address 80~84: Curtain Position
    # ========================================================================

    "time_remaining_until_next_irrigation": {
        "korean_name": "다습관수남은시간",
        "type": "REGISTER_READ",
        "address": 80,
        "scale": 1,
        "unit": "초",
        "description": "다습관수 까지 남은시간 (2워드) (다습관수남은시간)"
    },

    "upper_insulation_curtain_current_position": {
        "korean_name": "상부보온커튼이동량",
        "type": "REGISTER_READ",
        "address": 82,
        "scale": 1,
        "unit": "초",
        "description": "상부보온커튼 현재 이동량 (상부보온커튼이동량)"
    },

    "side_insulation_curtain_current_position": {
        "korean_name": "측면보온커튼이동량",
        "type": "REGISTER_READ",
        "address": 83,
        "scale": 1,
        "unit": "초",
        "description": "측면보온커튼 현재 이동량 (측면보온커튼이동량)"
    },

    "shading_curtain_current_position": {
        "korean_name": "차광커튼이동량",
        "type": "REGISTER_READ",
        "address": 84,
        "scale": 1,
        "unit": "초",
        "description": "차광커튼 현재 이동량 (차광커튼이동량)"
    }

}

# ============================================================================
# Utility Functions
# ============================================================================

def get_spec(name):
    """
    Get control item specification by name
    
    Args:
        name (str): Control item name (English)
        
    Returns:
        dict: Control item specification (None if not found)
    """
    return CONTROL_SPECS.get(name)


def list_all():
    """
    Get all control item names
    
    Returns:
        list: List of all control item names (English)
    """
    return list(CONTROL_SPECS.keys())


def get_by_address(address):
    """
    Get all control items at specific word address
    
    Args:
        address (int): Word address
        
    Returns:
        dict: All control items at that address {name: spec}
    """
    result = {}
    for name, spec in CONTROL_SPECS.items():
        if spec.get('address') == address:
            result[name] = spec
    return result


def get_by_type(spec_type):
    """
    Get all control item names of specific type
    
    Args:
        spec_type (str): Control type (e.g., 'SENSOR_READ', 'BIT_WRITE')
        
    Returns:
        list: List of control item names of that type
    """
    result = []
    for name, spec in CONTROL_SPECS.items():
        if spec.get('type') == spec_type:
            result.append(name)
    return result


if __name__ == "__main__":
    print(f"Total {len(CONTROL_SPECS)} control items defined.")
    print(f"\nWord address range: 0 ~ 84")
    print(f"\nControl types:")
    
    types_count = {}
    for spec in CONTROL_SPECS.values():
        spec_type = spec['type']
        types_count[spec_type] = types_count.get(spec_type, 0) + 1
    
    for spec_type, count in sorted(types_count.items()):
        print(f"  - {spec_type}: {count} items")
