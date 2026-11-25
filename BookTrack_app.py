import streamlit as st
import json
import os
import pandas as pd
import uuid

# ==========================================
# 1. НАСТРОЙКИ ПРИЛОЖЕНИЯ
# ==========================================

st.set_page_config(
    page_title="BookTrack",
    page_icon="📚️",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "books.json"


# ==========================================
# 2. РАБОТА С ДАННЫМИ
# ==========================================

def load_books():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_books(books):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            books,
            file,
            ensure_ascii=False,
            indent=4
        )
def load_settings():

    if os.path.exists("settings.json"):
        with open("settings.json", "r", encoding="utf-8") as file:
            return json.load(file)

    return {"yearly_goal": 20}


def save_settings(settings):

    with open("settings.json", "w", encoding="utf-8") as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)        
def save_cover(uploaded_file):

    if uploaded_file is None:
        return None

    os.makedirs("covers", exist_ok=True)

    extension = os.path.splitext(uploaded_file.name)[1].lower()

    if extension not in [".png", ".jpg", ".jpeg", ".webp"]:
        return None

    filename = f"{uuid.uuid4().hex}{extension}"

    cover_path = os.path.join("covers", filename)

    with open(cover_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return cover_path

if "books" not in st.session_state:
    st.session_state.books = load_books()


# ==========================================
# 3. ДИЗАЙН
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

.stApp {
    background-color: #F5F1E9;
    color: #343B40;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

h1, h2, h3 {
    color: #343B40 !important;
    font-family: 'Playfair Display', serif !important;
}

p, label {
    color: #59646B;
}

.hero {
    background: #E7E2D8;
    padding: 35px;
    border-radius: 20px;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 38px;
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E7E2D8;
    padding: 22px;
    border-radius: 16px;
    min-height: 125px;
}

.metric-title {
    color: #7B858A;
    font-size: 14px;
}

.metric-value {
    color: #343B40;
    font-size: 30px;
    font-weight: 700;
}

.book-card {
    background: #FFFFFF;
    border: 1px solid #E7E2D8;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 12px;
}

div.stButton > button {
    background-color: #526C7A;
    color: white;
    border: none;
    border-radius: 10px;
}

div.stButton > button:hover {
    background-color: #405866;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #EAE5DC;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. БОКОВОЕ МЕНЮ
# ==========================================

with st.sidebar:

    st.markdown("# 📚️ BookTrack")
    st.caption("Твоя личная библиотека")

    st.divider()

    page = st.radio(
        "НАВИГАЦИЯ",
        [
            "Главная",
            "Моя библиотека",
            "Мои цели",
            "Избранное",
            "Прогресс",
            "Статистика"
        ]
    )

    st.divider()

    st.caption("READ MORE. TRACK BETTER.")


# ==========================================
# 5. ПОДСЧЁТ СТАТИСТИКИ
# ==========================================

books = st.session_state.books

total_books = len(books)

finished_books = sum(
    1 for book in books
    if book["status"] == "Прочитана"
)

reading_books = sum(
    1 for book in books
    if book["status"] == "Читаю"
)

planned_books = sum(
    1 for book in books
    if book["status"] == "Хочу прочитать"
)


# ==========================================
# 6. ГЛАВНАЯ СТРАНИЦА
# ==========================================

if page == "Главная":

    st.markdown("""
    <div class="hero">
        <h1>Твоя история чтения начинается здесь.</h1>
        <p>
            Собирай любимые книги, следи за прогрессом
            и открывай новые истории.
        </p>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input(
        "Как к тебе обращаться?",
        placeholder="Введи своё имя"
    )

    if name:
        st.success(f"Рады видеть тебя, {name}!")

    st.markdown("## Твоя библиотека")

    col1, col2, col3 = st.columns(3)
    metrics = [
        (col1, "Всего книг", total_books),
        (col2, "Прочитано", finished_books),
        (col3, "Читаю сейчас", reading_books)
    ]

    for col, title, value in metrics:

        with col:

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("## Последние добавленные книги")

    if books:

        for book in reversed(books[-3:]):

            st.markdown(f"""
            <div class="book-card">
                <h3>📖 {book['title']}</h3>
                <p>{book['author']} · {book['genre']}</p>
                <p>Статус: {book['status']}</p>
            </div>
            """, unsafe_allow_html=True)

    else:

        st.info(
            "Твоя библиотека пока пуста. "
            "Добавь первую книгу!"
        )


# ==========================================
# 7. МОЯ БИБЛИОТЕКА
# ==========================================

elif page == "Моя библиотека":

    st.title("Моя библиотека")

    st.write(
        "Добавляй книги, ищи их и управляй своей коллекцией."
    )

    with st.expander("＋ Добавить новую книгу", expanded=True):

        with st.form("add_book_form"):

            title = st.text_input("Название книги")

            author = st.text_input("Автор")

            genre = st.selectbox(
                "Жанр",
                [
                    "Роман",
                    "Фэнтези",
                    "Детектив",
                    "Фантастика",
                    "Классика",
                    "Психология",
                    "Научная литература",
                    "Другое"
                ]
            )

            pages = st.number_input(
                "Количество страниц",
                min_value=1,
                value=200,
                step=1
            )
            cover_file = st.file_uploader(
                "Обложка книги",
                type=["png", "jpg", "jpeg", "webp"],
                help="Выбери изображение обложки с компьютера"
            )
            status = st.selectbox(
                "Статус чтения",
                [
                    "Хочу прочитать",
                    "Читаю",
                    "Прочитана"
                ]
            )

            submitted = st.form_submit_button(
                "Добавить книгу"
            )

            if submitted:

                if not title.strip() or not author.strip():

                    st.error(
                        "Заполни название книги и имя автора."
                    )

                else:

                    new_book = {
                        "title": title.strip(),
                        "author": author.strip(),
                        "genre": genre,
                        "pages": int(pages),
                        "status": status,
                        "progress": 0,
                        "favorite": False,
                        "cover": save_cover(cover_file)
                    }

                    if status == "Прочитана":
                        new_book["progress"] = int(pages)

                    st.session_state.books.append(new_book)

                    save_books(st.session_state.books)

                    st.success(
                        f"Книга «{title}» добавлена!"
                    )

                    st.rerun()

    st.divider()

    st.subheader("Все книги")

    search = st.text_input(
        "🔍️ Поиск по названию или автору",
        placeholder="Например, Джейн Остин"
    )

    filter_status = st.selectbox(
        "Фильтр по статусу",
        [
            "Все книги",
            "Хочу прочитать",
            "Читаю",
            "Прочитана"
        ]
    )

    filtered_books = []

    for index, book in enumerate(st.session_state.books):

        matches_search = (
            search.lower() in book["title"].lower()
            or search.lower() in book["author"].lower()
        )

        matches_status = (
            filter_status == "Все книги"
            or book["status"] == filter_status
        )

        if matches_search and matches_status:

            filtered_books.append((index, book))

    if filtered_books:

        for index, book in filtered_books:
            with st.container(border=True):

                cover_path = book.get("cover")

                if cover_path and os.path.exists(cover_path):
                    col_cover, col_info = st.columns([1, 3])

                    with col_cover:
                        st.image(
                            cover_path,
                            width=130
                        )

                    with col_info:
                        st.markdown(f"### 📖 {book['title']}")
                        st.write(f"Автор: {book['author']}")
                        st.write(f"Жанр: {book['genre']}")
                        st.write(f"Страниц: {book['pages']}")
                        st.write(f"Статус: {book['status']}")

                else:
                    st.markdown(f"### 📖 {book['title']}")
                    st.write(f"Автор: {book['author']}")
                    st.write(f"Жанр: {book['genre']}")
                    st.write(f"Страниц: {book['pages']}")
                    st.write(f"Статус: {book['status']}")
                is_favorite = book.get("favorite", False)

                if st.button(
                    "❤️ Убрать из избранного" if is_favorite else "♡ В избранное",
                    key=f"favorite_{index}"
                ):

                    st.session_state.books[index]["favorite"] = not is_favorite

                    save_books(st.session_state.books)

                    st.rerun()
                with st.expander("✏️ Редактировать книгу"):

                    with st.form(f"edit_book_form_{index}"):

                        edited_title = st.text_input(
                            "Название книги",
                            value=book["title"]
                        )

                        edited_author = st.text_input(
                            "Автор",
                            value=book["author"]
                        )

                        edited_genre = st.selectbox(
                            "Жанр",
                            [
                                "Роман",
                                "Фэнтези",
                                "Детектив",
                                "Фантастика",
                                "Классика",
                                "Психология",
                                "Научная литература",
                                "Другое"
                            ],
                            index=[
                                "Роман",
                                "Фэнтези",
                                "Детектив",
                                "Фантастика",
                                "Классика",
                                "Психология",
                                "Научная литература",
                                "Другое"
                            ].index(book["genre"])
                        )

                        edited_pages = st.number_input(
                            "Количество страниц",
                            min_value=1,
                            value=int(book["pages"]),
                            step=1
                        )

                        edited_status = st.selectbox(
                            "Статус чтения",
                            [
                                "Хочу прочитать",
                                "Читаю",
                                "Прочитана"
                            ],
                            index=[
                                "Хочу прочитать",
                                "Читаю",
                                "Прочитана"
                            ].index(book["status"])
                        )
                        edited_cover = st.file_uploader(
    "Заменить обложку",
    type=["png", "jpg", "jpeg", "webp"],
    key=f"edit_cover_{index}"
)

                        save_changes = st.form_submit_button(
                            "Сохранить изменения"
                        )

                        if save_changes:

                            if not edited_title.strip() or not edited_author.strip():
                                st.error("Название и автор не могут быть пустыми.")

                            else:
                                st.session_state.books[index]["title"] = edited_title.strip()
                                st.session_state.books[index]["author"] = edited_author.strip()
                                st.session_state.books[index]["genre"] = edited_genre
                                st.session_state.books[index]["pages"] = int(edited_pages)
                                st.session_state.books[index]["status"] = edited_status

                                if edited_status == "Прочитана":
                                    st.session_state.books[index]["progress"] = int(edited_pages)

                                elif edited_status == "Хочу прочитать":
                                    st.session_state.books[index]["progress"] = 0

                                else:
                                    st.session_state.books[index]["progress"] = min(
                                        int(book.get("progress", 0)),
                                        int(edited_pages)
                                    )
                            if edited_cover is not None:
                                st.session_state.books[index]["cover"] = save_cover(edited_cover)  
                                save_books(st.session_state.books)

                                st.success("Изменения сохранены!")

                                st.rerun()
                col1, col2 = st.columns(2)

                with col1:

                    new_status = st.selectbox(
                        "Изменить статус",
                        [
                            "Хочу прочитать",
                            "Читаю",
                            "Прочитана"
                        ],
                        index=[
                            "Хочу прочитать",
                            "Читаю",
                            "Прочитана"
                        ].index(book["status"]),
                        key=f"status_{index}"
                    )

                    if new_status != book["status"]:

                        st.session_state.books[index]["status"] = new_status

                        if new_status == "Прочитана":
                            st.session_state.books[index]["progress"] = book["pages"]

                        save_books(st.session_state.books)

                        st.rerun()

                with col2:

                    if st.button(
                        "Удалить книгу",
                        key=f"delete_{index}"
                    ):

                        st.session_state.books.pop(index)

                        save_books(st.session_state.books)

                        st.rerun()

    else:

        st.info("По твоему запросу книги не найдены.")


# ==========================================
# 8. ПРОГРЕСС ЧТЕНИЯ
# ==========================================
elif page == "Избранное":

    st.title("❤️ Избранное")

    st.write("Твоя личная подборка книг.")

    favorite_books = [
        book for book in books
        if book.get("favorite", False)
    ]

    if favorite_books:

        st.write(f"В избранном книг: {len(favorite_books)}")

        for book in favorite_books:

            with st.container(border=True):

                cover_path = book.get("cover")

                if cover_path and os.path.exists(cover_path):

                    col_cover, col_info = st.columns([1, 3])

                    with col_cover:
                        st.image(cover_path, width=130)

                    with col_info:
                        st.markdown(f"### 📖 {book['title']}")
                        st.write(f"Автор: {book['author']}")
                        st.write(f"Жанр: {book['genre']}")
                        st.write(f"Страниц: {book['pages']}")
                        st.write(f"Статус: {book['status']}")

                else:

                    st.markdown(f"### 📖 {book['title']}")
                    st.write(f"Автор: {book['author']}")
                    st.write(f"Жанр: {book['genre']}")
                    st.write(f"Страниц: {book['pages']}")
                    st.write(f"Статус: {book['status']}")

    else:

        st.info(
            "Пока здесь нет избранных книг. "
            "Добавь их в избранное в своей библиотеке."
        )

elif page == "Мои цели":

    st.title("🎯 Мои цели")
    st.write("Следи за своими читательскими достижениями.")

    st.subheader("Цель на год")

    settings = load_settings()

    yearly_goal = st.number_input(
        "Сколько книг хочешь прочитать за год?",
        min_value=1,
        max_value=365,
        value=int(settings["yearly_goal"]),
        step=1
    )

    if yearly_goal != settings["yearly_goal"]:
        settings["yearly_goal"] = yearly_goal
        save_settings(settings)
    completed_books = sum(
    1 for book in books
    if book["status"] == "Прочитана"
)
    progress = min(completed_books / yearly_goal, 1.0)

    st.divider()

    st.subheader("Твой результат")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Прочитано книг",
            completed_books
        )

    with col2:
        st.metric(
            "Осталось прочитать",
            max(yearly_goal - completed_books, 0)
        )

    st.progress(progress)

    st.write(
        f"Выполнено: {progress * 100:.1f}%"
    )
    if completed_books >= yearly_goal:
        st.success("🏆️ Поздравляем! Ты достигла своей цели!")
    else:
        remaining = yearly_goal - completed_books

        st.info(
            f"📚️ Осталось прочитать {remaining} "
            f"{'книгу' if remaining % 10 == 1 and remaining % 100 != 11 else 'книги' if remaining % 10 in [2, 3, 4] and remaining % 100 not in [12, 13, 14] else 'книг'} до цели!"
        )        
elif page == "Прогресс":

    st.title("Прогресс чтения")

    reading_list = [
        (index, book)
        for index, book in enumerate(books)
        if book["status"] == "Читаю"
    ]

    if not reading_list:

        st.info(
            "Пока нет книг со статусом «Читаю». "
            "Добавь книгу и выбери этот статус."
        )

    else:

        for index, book in reading_list:

            st.markdown(f"### 📖 {book['title']}")

            st.write(f"Автор: {book['author']}")

            current_progress = st.slider(
                "Количество прочитанных страниц",
                min_value=0,
                max_value=book["pages"],
                value=min(book["progress"], book["pages"]),
                key=f"pages_{index}"
            )

            st.session_state.books[index]["progress"] = current_progress

            percentage = current_progress / book["pages"]

            st.progress(percentage)

            st.write(
                f"Прочитано: {current_progress} из "
                f"{book['pages']} страниц "
                f"({percentage * 100:.0f}%)"
            )

            if current_progress == book["pages"]:

                if st.button(
                    "Отметить как прочитанную",
                    key=f"finish_{index}"
                ):

                    st.session_state.books[index]["status"] = "Прочитана"

                    save_books(st.session_state.books)

                    st.rerun()

            st.divider()

        save_books(st.session_state.books)


# ==========================================
# 9. СТАТИСТИКА
# ==========================================

elif page == "Статистика":

    st.title("Статистика чтения")

    total_pages_read = sum(
        book["progress"]
        for book in books
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Всего книг",
        total_books
    )

    col2.metric(
        "Прочитано книг",
        finished_books
    )

    col3.metric(
        "Прочитано страниц",
        total_pages_read
    )

    st.divider()

    st.subheader("Распределение по статусам")
    status_data = pd.DataFrame({
        "Статус": [
            "Хочу прочитать",
            "Читаю",
            "Прочитана"
        ],
        "Количество": [
            planned_books,
            reading_books,
            finished_books
        ]
    })

    st.bar_chart(
        status_data.set_index("Статус")
    )

    st.divider()

    st.subheader("Жанры библиотеки")

    if books:
        # Создаём список всех жанров
        all_genres = [
            book["genre"]
            for book in books
        ]

        # Создаём множество уникальных жанров
        unique_genres = set(all_genres)

        st.metric(
            "Уникальных жанров",
            len(unique_genres)
        )

        st.write("Жанры в твоей библиотеке:")

        st.write(", ".join(sorted(unique_genres)))
        genre_data = pd.DataFrame(books)

        genre_counts = (
            genre_data["genre"]
            .value_counts()
            .rename_axis("Жанр")
            .reset_index(name="Количество")
        )

        st.bar_chart(
            genre_counts.set_index("Жанр")
        )

    else:

        st.info(
            "Добавь книги, чтобы увидеть статистику жанров."
        )
        st.divider()

    st.subheader("📚️ Полная таблица библиотеки")

    if books:

        table_data = pd.DataFrame(books)

        table_data = table_data.rename(columns={
            "title": "Название",
            "author": "Автор",
            "genre": "Жанр",
            "pages": "Всего страниц",
            "status": "Статус",
            "progress": "Прочитано страниц"
        })

        st.dataframe(
            table_data[
                [
                    "Название",
                    "Автор",
                    "Жанр",
                    "Всего страниц",
                    "Статус",
                    "Прочитано страниц"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Добавь книги, чтобы увидеть таблицу.")
