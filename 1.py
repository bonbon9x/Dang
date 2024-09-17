import streamlit as st
import pandas as pd
import random

# Khởi tạo session state cho điểm và người chơi
if 'players' not in st.session_state:
    st.session_state['players'] = ['Người chơi 1', 'Người chơi 2', 'Người chơi 3']
    st.session_state['current_scores'] = [0, 0, 0]
    st.session_state['total_scores'] = [0, 0, 0]
    st.session_state['first_place_count'] = [0, 0, 0]
    st.session_state['selected_player'] = None
    st.session_state['show_scores'] = False  # Để hiển thị và ẩn bảng điểm

# Chức năng "Chọn ngẫu nhiên người chơi"
def select_random_player():
    st.session_state['selected_player'] = random.choice(st.session_state['players'])

# Chức năng "Kết thúc ván" và đặt lại điểm hiện tại
def end_round():
    max_score = max(st.session_state['current_scores'])
    if max_score > 0:  # Chỉ tính số trận thắng nếu có điểm lớn hơn 0
        for i, score in enumerate(st.session_state['current_scores']):
            if score == max_score:
                st.session_state['first_place_count'][i] += 1
    st.session_state['total_scores'] = [sum(x) for x in zip(st.session_state['total_scores'], st.session_state['current_scores'])]
    st.session_state['current_scores'] = [0, 0, 0]  # Reset điểm hiện tại ngay lập tức

# Hiển thị bảng điểm dưới dạng bảng
def show_scores():
    data = {
        'Hạng': [1, 2, 3],  # Đảm bảo ranking từ 1 đến 3
        'Tên người chơi': st.session_state['players'],
        'Tổng điểm': st.session_state['total_scores'],
        'Số trận thắng': st.session_state['first_place_count']
    }
    df = pd.DataFrame(data)
    st.table(df.set_index('Hạng'))  # Loại bỏ cột STT không mong muốn

# Tăng điểm cho người chơi
def increase_score(index):
    st.session_state['current_scores'][index] += 1

# Giảm điểm cho người chơi
def decrease_score(index):
    st.session_state['current_scores'][index] = max(0, st.session_state['current_scores'][index] - 1)

# Đổi tên tiêu đề của ứng dụng
st.title("Chống tính VP bẩn - Smashup")

# Hiển thị tên và điểm của từng người chơi
for i in range(3):
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        # Lưu tên mới của người chơi vào session_state
        st.session_state['players'][i] = st.text_input(f"Tên người chơi {i+1}", value=st.session_state['players'][i], key=f'name_{i}')
    with col2:
        st.write(f"Điểm hiện tại: {st.session_state['current_scores'][i]}")
    with col3:
        col_plus, col_minus = st.columns([1, 1])
        with col_plus:
            st.button("➕", on_click=increase_score, args=(i,), key=f'plus_{i}')  # Sử dụng kí tự unicode cho nút "+"
        with col_minus:
            st.button("➖", on_click=decrease_score, args=(i,), key=f'minus_{i}')  # Sử dụng kí tự unicode cho nút "-"

# Hàng chứa các nút
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Chọn người chơi ngẫu nhiên", key='random_player'):
        select_random_player()
    if st.session_state['selected_player']:
        st.write(f"Người chơi ngẫu nhiên được chọn: {st.session_state['selected_player']}", unsafe_allow_html=True)

with col2:
    if st.button("Kết thúc ván", key='end_round'):
        end_round()

with col3:
    if st.button("Hiển Thị Điểm", key='toggle_scores'):
        st.session_state['show_scores'] = not st.session_state['show_scores']

# Hiển thị bảng điểm nếu đã bật hiển thị
if st.session_state['show_scores']:
    show_scores()
