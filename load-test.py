import asyncio
import aiohttp

BASE_URL = "https://onlinetestzone.com"

# Shared headers
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Referer": "https://onlinetestzone.com",
    "Cookie": "csrftoken=UICtYfIE7nyY1MAhiFELt0azn71FPt98; messages=W1siX19qc29uX21lc3NhZ2UiLDAsMjUsIkxvZ2dlZCBpbiBzdWNjZXNzZnVsbHkuIiwiIl1d:1uxPKR:ZwuxJ9qXL55G3jso8QpAerTO8cpw0nVxP61ThRtVqqY; sessionid=cv405rno3g65dd3d3ho3lamk68z2701d"
}

# Login payload (you may replace registration_id/dob for each user)
LOGIN_PAYLOAD = {
    "csrfmiddlewaretoken": "KQvmZofn97DPoGZrtDdKQmM3TaFbmVGUuoXFNtNR6k1DfipyB8Hl9cMs67wG1eFS",
    "registration_id": "REG-2025-20000101-29127",
    "dob": "2000-01-01",
    "force_login": "true",
    "connection": "keep-alive"
}

# Answer payload builder
def question_payload(csrf_token: str, index: int, answer="D"):
    return {
        "csrfmiddlewaretoken": csrf_token,
        "question_index": str(index),
        "answer": answer,
        "action": "next"
    }

async def user_flow(session, user_id: int):
    csrf_token = "KQvmZofn97DPoGZrtDdKQmM3TaFbmVGUuoXFNtNR6k1DfipyB8Hl9cMs67wG1eFS"  # TODO: dynamically fetch from login if needed

    try:
        # 1. Login
        async with session.post(f"{BASE_URL}/users/login/", data=LOGIN_PAYLOAD, headers=HEADERS) as resp:
            print(f"[User {user_id}] Login -> {resp.status}")

        # 2. Dashboard
        async with session.get(f"{BASE_URL}/users/dashboard/", headers=HEADERS) as resp:
            print(f"[User {user_id}] Dashboard -> {resp.status}")

        # ===================== General Test =====================
        # 3. Start GT
        async with session.get(f"{BASE_URL}/exam_dashboard/start_test/", headers=HEADERS) as resp:
            print(f"[User {user_id}] Start GT -> {resp.status}")

        # 4. Submit 20 GT questions
        for q_index in range(20):
            payload = question_payload(csrf_token, q_index, "D")
            async with session.post(f"{BASE_URL}/exam_dashboard/test_page/{q_index}/",
                                    data=payload,
                                    headers=HEADERS) as resp:
                print(f"[User {user_id}] GT Q{q_index} -> {resp.status}")

        # 5. Final Submit GT
        async with session.post(f"{BASE_URL}/exam_dashboard/submit_test/",
                                data={"csrfmiddlewaretoken": csrf_token},
                                headers=HEADERS) as resp:
            print(f"[User {user_id}] GT Final Submit -> {resp.status}")

        # ===================== Technical Test =====================
        # 6. Start TT
        async with session.get(f"{BASE_URL}/exam_dashboard/start_technical_test/", headers=HEADERS) as resp:
            print(f"[User {user_id}] Start TT -> {resp.status}")

        # 7. Submit 20 TT questions
        for q_index in range(20):
            payload = question_payload(csrf_token, q_index, "D")
            async with session.post(f"{BASE_URL}/exam_dashboard/technical_test_page/{q_index}/",
                                    data=payload,
                                    headers=HEADERS) as resp:
                print(f"[User {user_id}] TT Q{q_index} -> {resp.status}")

        # 8. Final Submit TT
        async with session.post(f"{BASE_URL}/exam_dashboard/submit_technical_test/",
                                data={"csrfmiddlewaretoken": csrf_token},
                                headers=HEADERS) as resp:
            print(f"[User {user_id}] TT Final Submit -> {resp.status}")

    except Exception as e:
        print(f"[User {user_id}] Error: {e}")

async def main(concurrent_users=200):
    timeout = aiohttp.ClientTimeout(total=120)  # extend if needed
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [user_flow(session, i) for i in range(concurrent_users)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main(200))  # 🔥 adjust concurrency here
