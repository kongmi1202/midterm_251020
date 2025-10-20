# Streamlit 기반 음역대별 가수 추천 웹 애플리케이션 (Python 재구현)

import streamlit as st
import re
import pandas as pd
import altair as alt
from streamlit.components.v1 import html as st_html # HTML/CSS 컴포넌트 출력을 위해 사용

# 1. 핵심 데이터 정의
# 모든 성종 분류 기준, 난이도별 추천곡, 특징 등을 포함합니다.
VOICE_DATA = {
    'Bass (베이스)': {
        'min_midi': 40, 'max_midi': 64,  # E2 - E4
        'description': "웅장하고 깊은 저음을 가진 목소리입니다. 무대 전체를 감싸는 듯한 무게감과 카리스마가 느껴지며, 보통 느리고 진중한 노래에 잘 어울립니다. (남성의 가장 낮은 음역)",
        'singers': [
            {'name': "스트레이 키즈 펠릭스", 'songs': [
                {'title': "God's Menu", 'level': "하", 'detail': "톡 쏘는 낮은 톤 위주로, 특유의 낮은 목소리만 잘 살리면 난이도가 낮아요.", 'link': "https://www.youtube.com/results?search_query=스트레이키즈+God's+Menu"},
                {'title': "MIROH", 'level': "중", 'detail': "다이내믹한 랩과 보컬 연결이 요구되어 리듬감이 중요합니다.", 'link': "https://www.youtube.com/results?search_query=스트레이키즈+MIROH"},
                {'title': "Seoul (Prod. HONNE)", 'level': "상", 'detail': "섬세한 감정 표현과 넓은 다이내믹 레인지를 요구하며, 느린 템포에서 집중력이 필요합니다.", 'link': "https://www.youtube.com/results?search_query=방탄소년단+RM+Seoul"}
            ]},
            {'name': "방탄소년단 RM", 'songs': [
                {'title': "Change (with Wale)", 'level': "하", 'detail': "안정적인 랩 플로우가 중심이며, 보컬 음역대가 평이합니다.", 'link': "https://www.youtube.com/results?search_query=방탄소년단+RM+Change+Wale"},
                {'title': "wild flower", 'level': "중", 'detail': "깊은 감성과 넓은 음역대 랩을 요구하여 표현력이 필요합니다.", 'link': "https://www.youtube.com/results?search_query=방탄소년단+RM+wild+flower"}
            ]}
        ]
    },
    'Baritone (바리톤)': {
        'min_midi': 43, 'max_midi': 67,  # G2 - G4
        'description': "중후하고 부드러운 중저음을 가진 목소리입니다. 가장 흔한 남성 음역대로, 감정을 표현하는 데 뛰어나 발라드나 미디엄 템포의 곡을 안정적으로 소화합니다.",
        'singers': [
            {'name': "존 박", 'songs': [
                {'title': "철부지", 'level': "하", 'detail': "중저음 중심의 서정적인 곡으로, 부드러운 음색 표현에 집중하기 좋아요.", 'link': "https://www.youtube.com/results?search_query=존박+철부지"},
                {'title': "네 생각", 'level': "중", 'detail': "후반부 고음이 강조되는 미디엄 템포 곡으로, 부드러운 고음 연결이 중요합니다.", 'link': "https://www.youtube.com/results?search_query=존박+네+생각"},
                {'title': "Falling", 'level': "상", 'detail': "후렴구에서 가성 및 믹스 보이스로의 전환이 잦아 고음 컨트롤 테크닉이 매우 어렵습니다.", 'link': "https://www.youtube.com/results?search_query=존박+Falling"}
            ]},
            {'name': "폴 킴", 'songs': [
                {'title': "모든 날, 모든 순간", 'level': "하", 'detail': "감미로운 중음역이 중심이며, 편안한 음역대의 대표적인 곡입니다.", 'link': "https://www.youtube.com/results?search_query=폴킴+모든날+모든순간"},
                {'title': "너를 만나", 'level': "중", 'detail': "섬세한 감정 표현과 안정적인 호흡이 요구되는 발라드입니다.", 'link': "https://www.youtube.com/results?search_query=폴킴+너를만나"}
            ]}
        ]
    },
    'Tenor (테너)': {
        'min_midi': 47, 'max_midi': 72,  # B2 - C5
        'description': "힘차고 시원한 고음을 가진 목소리입니다. 맑고 높은 음역대로, 듣는 사람에게 짜릿한 쾌감을 주며 가창력이 강조되는 노래나 팝페라에 많이 활용됩니다. (남성의 가장 높은 음역)",
        'singers': [
            {'name': "방탄소년단 정국", 'songs': [
                {'title': "Seven (feat. Latto)", 'level': "하", 'detail': "쉬운 템포와 편안한 중음역 보컬로 리듬감을 연습하기 좋아요.", 'link': "https://www.youtube.com/results?search_query=방탄소년단+정국+Seven"},
                {'title': "Standing Next to You", 'level': "중", 'detail': "다이내믹한 고음과 리듬감이 요구되어 안정적인 발성이 필요합니다.", 'link': "https://www.youtube.com/results?search_query=방탄소년단+정국+Standing+Next+to+You"}
            ]}
        ]
    },
    'Alto (알토)': {
        'min_midi': 52, 'max_midi': 76,  # E3 - E5
        'description': "안정적이고 따뜻한 중저음을 가진 목소리입니다. 중저음 영역에서 가장 편안하고 풍부한 소리를 내며, 곡의 중심을 잡아주거나 무게감 있는 감정을 표현하는 데 좋습니다. (여성의 가장 낮은 음역)",
        'singers': [
            {'name': "이영지", 'songs': [
                {'title': "NOT SORRY", 'level': "하", 'detail': "리듬감이 중심이며, 보컬 음역대는 평이하여 랩 연습과 함께 좋습니다.", 'link': "https://www.youtube.com/results?search_query=이영지+NOT+SORRY"},
                {'title': "낮 밤", 'level': "중", 'detail': "랩과 보컬을 오가며 중저음의 깊이를 표현해야 하여 소울풀한 음색이 중요합니다.", 'link': "https://www.youtube.com/results?search_query=이영지+낮밤"}
            ]}
        ]
    },
    'Mezzo-Soprano (메조소프라노)': {
        'min_midi': 55, 'max_midi': 79,  # G3 - G5
        'description': "부드럽고 유연한 중음역을 가진 목소리입니다. 다양한 음색을 소화할 수 있어 넓은 스펙트럼의 노래에 잘 어울리며, 감정과 기교를 잘 조화시킵니다.",
        'singers': [
            {'name': "이하이", 'songs': [
                {'title': "한숨", 'level': "하", 'detail': "느린 템포, 중음역 중심의 감성 발라드로, 감정 표현에 집중하기 좋아요.", 'link': "https://www.youtube.com/results?search_query=이하이+한숨"},
                {'title': "ONLY", 'level': "중", 'detail': "부드러운 고음 처리와 소울풀한 음색을 요구하는 R&B 곡입니다.", 'link': "https://www.youtube.com/results?search_query=이하이+ONLY"}
            ]},
            {'name': "화사", 'songs': [
                {'title': "Twit", 'level': "하", 'detail': "리듬감과 그루브에 집중하며, 비교적 편안한 음역대에서 매력을 발산할 수 있습니다.", 'link': "https://www.youtube.com/results?search_query=화사+Twit"},
                {'title': "Maria", 'level': "중", 'detail': "파워풀한 중음과 가성이 조화되어 세련된 R&B 느낌을 잘 살려야 합니다.", 'link': "https://www.youtube.com/results?search_query=화사+Maria"},
                {'title': "I'm a B", 'level': "상", 'detail': "강한 비트 속에서 중음역대의 파워와 고음을 동시에 요구하는 고난이도 퍼포먼스 곡입니다.", 'link': "https://www.youtube.com/results?search_query=화사+I'm+a+B"}
            ]}
        ]
    },
    'Soprano (소프라노)': {
        'min_midi': 59, 'max_midi': 84,  # B3 - C6
        'description': "화려하고 맑은 고음을 가진 목소리입니다. 여성의 가장 높은 음역대로, 밝고 청아한 느낌을 주며 가벼운 팝이나 뮤지컬 넘버, 클래식 아리아에 주로 활용됩니다.",
        'singers': [
            {'name': "아이유", 'songs': [
                {'title': "밤편지", 'level': "하", 'detail': "비교적 느린 템포로, 잔잔하게 감정을 표현하기 좋아 음역대가 평이해요.", 'link': "https://www.youtube.com/results?search_query=아이유+밤편지"},
                {'title': "좋은 날", 'level': "상", 'detail': "템포가 빠르고 숨을 잘 쉬어야 해요. 3단 고음 테크닉이 필요합니다.", 'link': "https://www.youtube.com/results?search_query=아이유+좋은날"}
            ]},
            {'name': "태연", 'songs': [
                {'title': "I", 'level': "중", 'detail': "중간 템포지만 중저음과 고음을 부드럽게 연결하는 기술이 필요해요.", 'link': "https://www.youtube.com/results?search_query=태연+I"},
                {'title': "Fine", 'level': "상", 'detail': "매우 높은 고음이 길게 이어지고 호흡량이 많아야 하는 고난이도 곡입니다.", 'link': "https://www.youtube.com/results?search_query=태연+Fine"}
            ]}
        ]
    }
}

# 2. MIDI 변환 및 분류 로직 함수
def note_to_midi(note_string):
    """음계 문자열(C3, G4 등)을 MIDI 번호로 변환합니다. C4는 MIDI 60입니다."""
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    match = re.match(r'^([A-G]#?)(\d)$', note_string.upper())
    
    if not match:
        return None

    note = match.group(1)
    octave = int(match.group(2))
    
    if note not in notes:
        return None

    note_index = notes.index(note)
    # MIDI 공식: (옥타브 + 1) * 12 + 노트 인덱스.
    return (octave + 1) * 12 + note_index

def midi_to_note(midi):
    """MIDI 번호를 음계 문자열(예: C4)로 변환합니다."""
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = (midi // 12) - 1
    note_index = midi % 12
    return notes[note_index] + str(octave)

def find_voice_type(low_note_str, high_note_str):
    """사용자의 음역대를 가장 잘 포괄하는 성종을 찾아 반환합니다."""
    low_midi = note_to_midi(low_note_str)
    high_midi = note_to_midi(high_note_str)

    if low_midi is None or high_midi is None:
        return {"error": "올바른 음계 형식(예: C3, G4)으로 입력해 주세요."}
    
    if low_midi >= high_midi:
        return {"error": "최고음이 최저음보다 높아야 합니다."}

    best_match = None
    best_score = -1 

    for voice_type, data in VOICE_DATA.items():
        v_min = data['min_midi']
        v_max = data['max_midi']

        # 1. 포괄된 길이 계산 (사용자의 음역대가 성종 범위와 겹치는 정도)
        covered_low = max(low_midi, v_min)
        covered_high = min(high_midi, v_max)
        covered_range = max(0, covered_high - covered_low)
        
        # 2. 페널티 계산 (성종 범위를 벗어난 정도)
        penalty_low = max(0, v_min - low_midi) * 2 
        penalty_high = max(0, high_midi - v_max) * 2 

        # 3. 점수 계산 (포괄된 범위가 넓고, 벗어난 정도가 작을수록 높은 점수)
        current_score = covered_range - penalty_low - penalty_high

        # 4. 최적 매칭 업데이트
        if current_score > best_score:
            best_score = current_score
            best_match = {'voice_type': voice_type, 'data': data}
        
        # 완벽 포함 시 보너스 점수 (정확한 매칭을 선호)
        if covered_low <= low_midi and covered_high >= high_midi:
            current_score += 100 
            if current_score > best_score:
                 best_score = current_score
                 best_match = {'voice_type': voice_type, 'data': data}

    if best_match and best_score > -10: 
        best_match['low_midi'] = low_midi # 시각화를 위해 MIDI 값 추가
        best_match['high_midi'] = high_midi
        return best_match
    else:
        return {"error": "입력하신 음역대가 표준 성종 범위에서 너무 많이 벗어나 분류가 어렵습니다. 다시 입력해 주세요."}


# [NEW] 피아노 건반 UI 생성 및 사용자 음역대 표시 함수 (HTML/CSS 기반)
def generate_keyboard_html(low_midi, high_midi):
    """
    CSS와 HTML을 사용하여 피아노 건반 UI를 생성하고 사용자 음역대를 강조합니다.
    (검은 건반 배열 오류 수정 및 C음 레이블 표시)
    """
    
    start_midi = 36 # C2
    end_midi = 84   # C6
    
    # 1. CSS 스타일 정의
    css_styles = """
    <style>
        .keyboard-wrapper {
            position: relative;
            width: 100%;
            max-width: 800px;
            height: 120px; /* 건반 전체 높이 */
            margin: 40px auto 10px auto;
            box-sizing: border-box;
            background: #fff;
            border: 1px solid #000;
            border-radius: 8px;
        }
        .white-key-container {
            display: flex;
            width: 100%;
            height: 100%;
            position: relative;
            z-index: 1; 
        }
        .white-key {
            flex-grow: 1;
            height: 100%;
            border-right: 1px solid #000;
            background-color: #fff;
            box-sizing: border-box;
            position: relative;
        }
        .white-key:last-child {
            border-right: none;
        }
        
        /* 검은 건반 스타일: 너비를 줄이고 위치를 조정 */
        .black-key-container {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 60%; 
            pointer-events: none; 
            z-index: 2;
        }
        .black-key {
            position: absolute;
            /* width: 3%; 정도의 비율로 직접 계산하여 inline style로 적용할 것 */
            height: 100%;
            background-color: #000;
            top: 0;
            border-radius: 0 0 3px 3px;
        }
        
        /* 음역대 강조 스타일 */
        .highlighted-white {
            background-color: #fce7f3 !important; /* 연한 분홍색 강조 */
        }
        .highlighted-black {
            background-color: #db2777 !important; /* 진한 분홍색 강조 */
        }
        
        /* C음 레이블 스타일 */
        .label-text {
            font-weight: bold;
            color: #1e40af; /* 레이블 색상 */
            position: absolute;
            top: 5px; /* 건반 위쪽에 위치 */
            font-size: 11px;
            width: 100%;
            text-align: center;
        }
    </style>
    """
    
    # 2. 피아노 건반 구조 생성
    white_keys_html = ""
    black_keys_html = ""
    
    all_midi_notes = list(range(start_midi, end_midi + 1))
    
    white_note_indices = [0, 2, 4, 5, 7, 9, 11] # C, D, E, F, G, A, B
    total_white_keys = len([m for m in all_midi_notes if m % 12 in white_note_indices])
    key_width_pc = 100 / total_white_keys
    
    # MIDI 번호와 흰 건반 인덱스 매핑
    white_key_midi_map = [midi for midi in all_midi_notes if midi % 12 in white_note_indices]
    
    white_key_count = 0
    black_key_width_pc = key_width_pc * 0.55 # 검은 건반 너비 (흰 건반 너비의 55% 정도로 설정)
    
    for midi in all_midi_notes:
        note_index = midi % 12
        is_white = note_index in white_note_indices
        is_black = not is_white
        
        is_highlighted = low_midi <= midi <= high_midi
        
        if is_white:
            
            # 1. 흰 건반 HTML 생성
            white_key_count += 1
            
            label_text = ''
            # C음(note_index 0)에만 레이블 표시
            if note_index == 0: 
                 label_text = f'<span class="label-text">{midi_to_note(midi)}</span>'
                 
            white_keys_html += f"""
            <div class="white-key {'highlighted-white' if is_highlighted else ''}" style="width: {key_width_pc}%;">
                {label_text}
            </div>
            """
            
        elif is_black:
            # 2. 검은 건반 HTML 생성
            
            # 검은 건반이 위치해야 할 흰 건반의 인덱스를 찾습니다. (C#은 C, D#은 D 등)
            # note_index 1(C#) -> 0(C), 3(D#) -> 2(D), 6(F#) -> 5(F), 8(G#) -> 7(G), 10(A#) -> 9(A)
            base_midi_for_black = midi - 1
            if base_midi_for_black % 12 == 4: base_midi_for_black -= 1 # E와 F 사이를 건너뛰기 위함
            if base_midi_for_black % 12 == 11: base_midi_for_black -= 1 # B와 C 사이를 건너뛰기 위함

            try:
                base_white_index = white_key_midi_map.index(base_midi_for_black)
                
                # 검은 건반의 왼쪽 시작 위치 (퍼센트)
                # 검은 건반은 해당 흰 건반 오른쪽 경계 근처에 위치해야 합니다.
                # base_start_pc: 검은 건반이 속한 흰 건반의 왼쪽 시작 위치
                base_start_pc = base_white_index * key_width_pc
                
                # 검은 건반 위치: 흰 건반 시작점 + (흰 건반 너비 * 0.75) - (검은 건반 너비 / 2)
                # 0.75는 검은 건반을 흰 건반의 3/4 지점에 가깝게 배치하여 시각적 중앙으로 보이게 함
                left_offset_pc = base_start_pc + (key_width_pc * 0.75) - (black_key_width_pc / 2)
                
                black_keys_html += f"""
                <div class="key black-key {'highlighted-black' if is_highlighted else ''}" style="left: {left_offset_pc}%; width: {black_key_width_pc}%;">
                </div>
                """
            except ValueError:
                # 데이터 범위 밖의 건반은 건너뜁니다.
                pass 
                
    # 3. 최종 HTML 구성 (검은 건반이 흰 건반 위에 겹쳐지도록)
    keyboard_output = f"""
    {css_styles}
    <div class="keyboard-wrapper">
        <div class="white-key-container">
            {white_keys_html}
        </div>
        <!-- 검은 건반 컨테이너는 흰 건반 컨테이너 위에 위치하며, position: absolute로 처리됩니다. -->
        <div class="black-key-container"> 
            {black_keys_html}
        </div>
    </div>
    """
    
    # 4. 사용자 음역대 레이블
    low_note_name = midi_to_note(low_midi)
    high_note_name = midi_to_note(high_midi)
    
    info_html = f"""
    <div style="text-align: center; margin-top: 10px;">
        <span style="font-size: 1.5em; color: #dc2626; font-weight: bold;">{low_note_name}</span> 
        &nbsp;—&nbsp; 
        <span style="font-size: 1.5em; color: #dc2626; font-weight: bold;">{high_note_name}</span> 
        <p style="margin-top: 5px; color: #4b5563;">(입력하신 음역대입니다)</p>
    </div>
    """

    # 최종 결과: 건반 HTML + 정보 HTML
    return keyboard_output + info_html

# 4. Streamlit UI 및 출력

st.set_page_config(page_title="Voice Match", layout="centered")

st.markdown("<h1 style='text-align: center; color: #1e40af;'>🎤 Voice Match</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>최저음과 최고음을 입력하여 나의 성종과 추천 가수를 찾아보세요!</p>", unsafe_allow_html=True)

# 사용자 입력 섹션
with st.container(border=True):
    st.subheader("음역대 입력")
    # 빈칸으로 뜨도록 value="" 설정
    low_note = st.text_input("최저음 입력 (예: C3, G2)", value="", max_chars=3).strip() 
    high_note = st.text_input("최고음 입력 (예: G4, C5)", value="", max_chars=3).strip()
    
    find_button = st.button("내 성종 확인하기 🔍", type="primary", use_container_width=True)

# 결과 출력
if find_button:
    result = find_voice_type(low_note, high_note)
    
    if "error" in result:
        st.error(result['error'])
    else:
        st.success(f"🎉 당신의 성종은: {result['voice_type']}")
        
        data = result['data']
        
        # 성종 특징 표시
        st.markdown(f"**성종 특징:** *{data['description']}*")
        st.markdown("---")
        
        # 시각화 출력 블록
        try:
            # HTML/CSS 기반의 피아노 건반 UI 출력
            st.subheader("나의 음역대 위치 시각화 (피아노 건반)")
            
            keyboard_html = generate_keyboard_html(
                low_midi=result['low_midi'], 
                high_midi=result['high_midi']
            )
            # st_html 컴포넌트를 사용하여 건반 UI를 안정적으로 출력합니다.
            # height를 300으로 늘려 충분한 공간을 확보합니다.
            st_html(keyboard_html, height=300) 
            
        except Exception as e:
            # 시각화 오류 발생 시 사용자에게 알림
            st.warning(f"시각화 UI 생성 중 오류가 발생했습니다. (디버깅 정보: {e})")

        st.markdown("<h3 style='color: #4b5563;'>내 성종을 가진 가수와 난이도별 추천 노래:</h3>", unsafe_allow_html=True)
        
        # 가수별 목록 표시 (필터링 로직 제거)
        for singer in data['singers']:
            
            # 노래 목록을 필터링 없이 그대로 사용
            filtered_songs = singer['songs']
            
            if filtered_songs: # 노래가 있을 경우에만 가수 이름을 표시
                st.markdown(f"**<span style='color: #047857;'>{singer['name']}</span>**", unsafe_allow_html=True)
            
                # 노래 목록 표시 (난이도 및 링크 스타일링)
                for song in filtered_songs:
                    level_style = "color: #2563eb;" # 하 (파란색)
                    if song['level'] == '상':
                        level_style = "color: #dc2626;" # 상 (빨간색)
                    elif song['level'] == '중':
                        level_style = "color: #059669;" # 중 (초록색)
                    
                    # 재생 버튼 아이콘
                    youtube_icon = "▶️"
                    
                    # HTML과 CSS를 사용하여 노래 정보와 재생 버튼을 같은 줄에 표시
                    song_markdown = f"""
                    <div style='background-color: #f3ffef; padding: 8px; border-radius: 6px; margin-bottom: 5px; border-left: 3px solid #6ee7b4; display: flex; align-items: center; justify-content: space-between;'>
                        <span style='flex-grow: 1;'>
                            <span style='{level_style}; font-weight: bold; margin-right: 5px;'>({song['level']})</span>
                            <span class='font-bold'>{song['title']}</span>: 
                            <span style='color: #4b5563;'>{song['detail']}</span>
                        </span>
                        <a href="{song.get('link', '#')}" target="_blank" title="유튜브에서 노래 듣기">
                            <span style='font-size: 1.5em; color: #ff0000; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);'>{youtube_icon}</span>
                        </a>
                    </div>
                    """
                    st.markdown(song_markdown, unsafe_allow_html=True)
