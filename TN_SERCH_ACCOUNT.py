import streamlit as st
import tweepy

# ダミー認証情報（本番時は環境変数に設定）
API_KEY = "TNSS_API_KEY_for_X"
API_SECRET = "TNSS_API_SECRET_KEY_for_X"
ACCESS_TOKEN = "TNSS_ACCESS_TOKEN"
ACCESS_SECRET = "TNSS_ACCSES_TOKEN_SECRET"

# NGワードリスト（セッション状態で管理）
if "ng_words" not in st.session_state:
    st.session_state.ng_words = []

# --- NGワード登録UI ---
st.title("TN SEARCH ACCOUNTS")
st.subheader("NGワード管理")

new_word = st.text_input("NGワードを追加")
if st.button("追加") and new_word.strip():
    if new_word not in st.session_state.ng_words:
        st.session_state.ng_words.append(new_word.strip())

if st.button("全削除"):
    st.session_state.ng_words.clear()

st.write("現在のNGワード:", st.session_state.ng_words)

# --- ユーザー検索 ---
st.subheader("抽出設定")
query = st.text_input("検索キーワード")

# X APIクライアント設定
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def fetch_and_filter_users(query, ng_words, limit=5):
    extracted_users = []
    tweets = api.search_tweets(q=query, lang="ja", count=50)  # 例: 最新50件

    for tweet in tweets:
        text = tweet.text.lower()
        if any(word.lower() in text for word in ng_words):
            continue  # NGワード含む → スキップ

        user = tweet.user
        # 条件：フォロワー100以下 & ツイート少なめ
        if user.followers_count <= 100 and user.statuses_count < 50:
            extracted_users.append(user.screen_name)

        if len(extracted_users) >= limit:
            break

    return extracted_users

if st.button("抽出開始"):
    result = fetch_and_filter_users(query, st.session_state.ng_words)
    if result:
        selected_user = st.selectbox("抽出されたユーザー", result)
        st.success(f"選択中のユーザー: {selected_user}")
    else:
        st.warning("条件に合致するユーザーは見つかりませんでした。")
