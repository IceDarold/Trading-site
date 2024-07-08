import streamlit as st

def main():
    st.title("Пример небольшого сайта на Streamlit")

    st.header("Ввод данных")
    name = st.text_input("Введите ваше имя:")
    age = st.slider("Выберите ваш возраст:", 0, 100, 25)
    submitted = st.button("Отправить")

    if submitted:
        st.subheader("Вывод данных")
        st.write(f"Имя: {name}")
        st.write(f"Возраст: {age}")

    st.header("Визуализация данных")
    st.line_chart({
        'День': [1, 2, 3, 4, 5],
        'Значение': [10, 23, 12, 9, 30]
    })

if __name__ == "__main__":
    main()
