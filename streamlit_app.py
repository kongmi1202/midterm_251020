import streamlit as st
import re

# 1. 핵심 데이터 정의
VOICE_DATA = {
    'Bass (베이스)': {
        'min_midi': 40, 'max_midi': 64,
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
        'min_midi': 43, 'max_midi': 67,
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
        'min_midi': 47, 'max_midi': 72,
        'description': "힘차고 시원한 고음을 가진 목소리입니다. 맑고 높은 음역대로, 듣는 사람에게 짜릿한 쾌감을 주며 가창력이 강조되는 노래나 팝페라에 많이 활용됩니다. (남성의 가장 높은 음역)",
        'singers': [
            {'name': "방탄소년단 정국", 'songs': [
                {'title': "Seven (feat. Latto)", 'level': "하", 'detail': "쉬운 템포와 편안한 중음역 보컬로 리듬감을 연습하기 좋아요.", 'link': "https://www.youtube.com/results?search_query=방탄소년단+정국+Seven"},
                {'title': "Standing Next to You", 'level': "중", 'detail': "다이내믹한 고음과 리듬감이 요구되어 안정적인 발성이 필요합니다.", 'link': "https://www.youtube.com/results?search_query=방탄소년단+정국+Standing+Next+to+You"}
            ]}
        ]
    },
    'Alto (알토)': {
        'min_midi': 52, 'max_midi': 76,
        'description': "안정적이고 따뜻한 중저음을 가진 목소리입니다. 중저음 영역에서 가장 편안하고 풍부한 소리를 내며, 곡의 중심을 잡아주거나 무게감 있는 감정을 표현하는 데 좋습니다. (여성의 가장 낮은 음역)",
        'singers': [
            {'name': "이영지", 'songs': [
                {'title': "NOT SORRY", 'level': "하", 'detail': "리듬감이 중심이며, 보컬 음역대는 평이하여 랩 연습과 함께 좋습니다.", 'link': "https://www.youtube.com/results?search_query=이영지+NOT+SORRY"},
                {'title': "낮 밤", 'level': "중", 'detail': "랩과 보컬을 오가며 중저음의 깊이를 표현해야 하여 소울풀한 음색이 중요합니다.", 'link': "https://www.youtube.com/results?search_query=이영지+낮밤"}
            ]}
        ]
    },
    'Mezzo-Soprano (메조소프라노)': {
        'min_midi': 55, 'max_midi': 79,
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
        'min_midi': 59, 'max_midi': 84,
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

def note_to_midi(note_string):
    """음계 문자열을 MIDI 번호로 변환"""
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    match = re.match(r'^([A-G]#?)(\d)$', note_string.upper())
   
    if not match:
        return None

    note = match.group(1)
    octave = int(match.group(2))
   
    if note not in notes:
        return None

    note_index = notes.index(note)
    return (octave + 1) * 12 + note_index

def midi_to_note(midi):
    """MIDI 번호를 음계 문자열로 변환"""
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = (midi // 12) - 1
    note_index = midi % 12
    return notes[note_index] + str(octave)

def find_voice_type(low_note_str, high_note_str):
    """성종 분류"""
    low_midi = note_to_midi(low_note_str)
    high_midi = note_to_midi(high_note_str)

    if low_midi is None or high_midi is None:
        return {"error": "올바른 음계 형식(예: C3, G4)으로 입력해 주세요."}
   
    if low_midi >= high_midi:
        return {"error": "최고음이 최저음보다 높아야 합니다."}

    # 음역대 범위 계산
    range_width = high_midi - low_midi
    
    # 1단계: 최저음이 속한 성종 그룹 찾기
    candidate_voices = []
    
    for voice_type, data in VOICE_DATA.items():
        v_min = data['min_midi']
        v_max = data['max_midi']
        
        # 최저음이 해당 성종의 음역대 안에 있으면 후보에 추가
        if v_min <= low_midi <= v_max:
            candidate_voices.append({'voice_type': voice_type, 'data': data})
    
    # 후보가 없으면 최저음에 가장 가까운 성종 선택
    if not candidate_voices:
        min_distance = float('inf')
        for voice_type, data in VOICE_DATA.items():
            v_min = data['min_midi']
            distance = abs(low_midi - v_min)
            
            if distance < min_distance:
                min_distance = distance
                candidate_voices = [{'voice_type': voice_type, 'data': data}]
    
    # 2단계: 음역대가 넓으면(24 이상, 2옥타브) 최고음 기준으로 재평가
    if range_width >= 24:
        # 모든 성종 중에서 최고음에 가장 가까운 것 선택
        best_match = None
        min_high_distance = float('inf')
        
        for voice_type, data in VOICE_DATA.items():
            v_max = data['max_midi']
            distance = abs(high_midi - v_max)
            
            if distance < min_high_distance:
                min_high_distance = distance
                best_match = {'voice_type': voice_type, 'data': data}
    else:
        # 음역대가 좁으면 후보 그룹 내에서 최고음에 가장 가까운 성종 선택
        best_match = None
        min_high_distance = float('inf')
        
        for candidate in candidate_voices:
            data = candidate['data']
            v_max = data['max_midi']
            distance = abs(high_midi - v_max)
            
            if distance < min_high_distance:
                min_high_distance = distance
                best_match = candidate
           
    if best_match:
        best_match['low_midi'] = low_midi
        best_match['high_midi'] = high_midi
        return best_match
    else:
        return {"error": "입력하신 음역대가 표준 성종 범위에서 너무 많이 벗어나 분류가 어렵습니다. 다시 입력해 주세요."}

def generate_piano_svg(low_midi, high_midi):
    """SVG 기반 피아노 건반 시각화"""
   
    start_midi = 36  # C2
    end_midi = 84    # C6
   
    white_width = 40
    white_height = 150
    black_width = 24
    black_height = 95
   
    # 흰 건반만 먼저 세기
    white_keys = []
    for midi in range(start_midi, end_midi + 1):
        if midi % 12 in [0, 2, 4, 5, 7, 9, 11]:  # C, D, E, F, G, A, B
            white_keys.append(midi)
   
    svg_width = len(white_keys) * white_width
    svg_height = white_height + 60
   
    svg = f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">'
   
    # 배경
    svg += f'<rect width="{svg_width}" height="{svg_height}" fill="#f0f0f0"/>'
   
    # 흰 건반 그리기
    white_idx = 0
    for midi in white_keys:
        x = white_idx * white_width
        is_highlighted = low_midi <= midi <= high_midi
       
        fill = '#ff69b4' if is_highlighted else '#ffffff'
        stroke = '#be185d' if is_highlighted else '#333333'
       
        svg += f'<rect x="{x}" y="20" width="{white_width}" height="{white_height}" '
        svg += f'fill="{fill}" stroke="{stroke}" stroke-width="2" rx="4"/>'
       
        # C 음에 라벨
        if midi % 12 == 0:
            note_name = midi_to_note(midi)
            svg += f'<text x="{x + white_width/2}" y="{white_height + 45}" '
            svg += f'text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">{note_name}</text>'
       
        white_idx += 1
   
    # 검은 건반 그리기
    # 각 검은 건반의 위치를 흰 건반 인덱스 기준으로 계산
    white_idx = 0
    for midi in range(start_midi, end_midi + 1):
        note = midi % 12
       
        # 흰 건반이면 인덱스 증가
        if note in [0, 2, 4, 5, 7, 9, 11]:
            white_idx += 1
        # 검은 건반 그리기
        elif note in [1, 3, 6, 8, 10]:  # C#, D#, F#, G#, A#
            is_highlighted = low_midi <= midi <= high_midi
            fill = '#c71585' if is_highlighted else '#000000'
           
            # 검은 건반의 x 위치 계산
            # 이전 흰 건반의 오른쪽 끝에서 시작
            x = (white_idx * white_width) - (black_width / 2)
           
            svg += f'<rect x="{x}" y="20" width="{black_width}" height="{black_height}" '
            svg += f'fill="{fill}" stroke="#000000" stroke-width="1.5" rx="3"/>'
   
    svg += '</svg>'
   
    low_note = midi_to_note(low_midi)
    high_note = midi_to_note(high_midi)
   
    info = f"""
    <div style="text-align: center; margin-top: 20px;">
        <span style="font-size: 1.8em; color: #dc2626; font-weight: bold;">{low_note}</span>
        <span style="font-size: 1.5em; color: #6b7280;">—</span>
        <span style="font-size: 1.8em; color: #dc2626; font-weight: bold;">{high_note}</span>
        <p style="margin-top: 8px; color: #4b5563;">(입력하신 음역대가 분홍색으로 표시됩니다)</p>
    </div>
    """
   
    return f'<div style="overflow-x: auto; padding: 20px; background: #ffffff; border-radius: 8px;">{svg}{info}</div>'

# Streamlit UI
st.set_page_config(page_title="Voice Match", layout="centered")

st.markdown("<h1 style='text-align: center; color: #1e40af;'>🎤 Voice Match</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>최저음과 최고음을 입력하여 나의 성종과 추천 가수를 찾아보세요!</p>", unsafe_allow_html=True)

with st.container(border=True):
    st.subheader("음역대 입력")
    low_note = st.text_input("최저음 입력 (예: C3, G2)", value="", max_chars=3).strip()
    high_note = st.text_input("최고음 입력 (예: G4, C5)", value="", max_chars=3).strip()
   
    find_button = st.button("내 성종 확인하기 🔍", type="primary", use_container_width=True)

if find_button:
    result = find_voice_type(low_note, high_note)
   
    if "error" in result:
        st.error(result['error'])
    else:
        st.success(f"🎉 당신의 성종은: {result['voice_type']}")
       
        data = result['data']
        st.markdown(f"**성종 특징:** *{data['description']}*")
        st.markdown("---")
       
        try:
            st.subheader("나의 음역대 위치 시각화")
            piano_html = generate_piano_svg(result['low_midi'], result['high_midi'])
            st.markdown(piano_html, unsafe_allow_html=True)
           
        except Exception as e:
            st.warning(f"시각화 생성 중 오류: {e}")

        st.markdown("<h3 style='color: #4b5563;'>내 성종을 가진 가수와 난이도별 추천 노래:</h3>", unsafe_allow_html=True)
       
        for singer in data['singers']:
            filtered_songs = singer['songs']
           
            if filtered_songs:
                st.markdown(f"**<span style='color: #047857;'>{singer['name']}</span>**", unsafe_allow_html=True)
           
                for song in filtered_songs:
                    level_style = "color: #2563eb;"
                    if song['level'] == '상':
                        level_style = "color: #dc2626;"
                    elif song['level'] == '중':
                        level_style = "color: #059669;"
                   
                    song_markdown = f"""
                    <div style='background-color: #f3ffef; padding: 8px; border-radius: 6px; margin-bottom: 5px; border-left: 3px solid #6ee7b4; display: flex; align-items: center; justify-content: space-between;'>
                        <span style='flex-grow: 1;'>
                            <span style='{level_style}; font-weight: bold; margin-right: 5px;'>({song['level']})</span>
                            <span class='font-bold'>{song['title']}</span>:
                            <span style='color: #4b5563;'>{song['detail']}</span>
                        </span>
                        <a href="{song.get('link', '#')}" target="_blank" title="유튜브에서 노래 듣기">
                            <span style='font-size: 1.5em; color: #ff0000; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);'>▶️</span>
                        </a>
                    </div>
                    """
                    st.markdown(song_markdown, unsafe_allow_html=True)