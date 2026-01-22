"""
Test script for testing submissions API
Bu script orqali masala javobini yuborib tekshirishingiz mumkin.
"""

import requests
import time
import json

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def print_response(title, response):
    """Pretty print response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")


def create_problem():
    """Masala yaratish"""
    print("📝 Masala yaratilmoqda...")
    data = {
        "title": "Ikki sonni yig'indisi",
        "description": "Ikki sonni yig'indisini toping",
        "input_description": "Ikki butun son a va b",
        "output_description": "a + b natijasi",
        "constraints": "1 <= a, b <= 1000",
        "time_limit_sec": 2,
        "memory_limit_mb": 256
    }
    response = requests.post(f"{BASE_URL}/problems", json=data)
    print_response("Masala yaratish natijasi", response)
    
    if response.status_code == 200:
        return response.json()["id"]
    return None


def create_testcase(problem_id: int):
    """Testcase yaratish"""
    print("🧪 Testcase yaratilmoqda...")
    data = {
        "problem_id": problem_id,
        "count": 3,
        "min_value": 1,
        "max_value": 100,
        "seed": 42
    }
    response = requests.post(f"{BASE_URL}/testcases/generate/int", json=data)
    print_response("Testcase yaratish natijasi", response)
    return response.status_code == 201


def submit_solution(problem_id: int, language: str, code: str):
    """Submission yuborish"""
    print(f"📤 {language.upper()} kod yuborilmoqda...")
    data = {
        "problem_id": problem_id,
        "language": language,
        "source_code": code
    }
    response = requests.post(f"{BASE_URL}/submissions", json=data)
    print_response(f"{language.upper()} Submission natijasi", response)
    
    if response.status_code == 201:
        submission = response.json()
        submission_id = submission["id"]
        print(f"✅ Submission ID: {submission_id}")
        print(f"⏳ Status: {submission['status']}")
        print("\n⏳ Kod Docker'da ishlanmoqda... (bir necha soniya kutish kerak)")
        return submission_id
    return None


def check_submission_status(submission_id: str):
    """Submission statusini tekshirish"""
    # Bu endpoint hozircha yo'q, lekin kelajakda qo'shish mumkin
    print(f"\n💡 Submission ID: {submission_id}")
    print("💡 Statusni tekshirish uchun database'ga qarang yoki API endpoint qo'shing")


def main():
    print("🚀 Judge API Test Script")
    print("=" * 60)
    
    # 1. Masala yaratish
    problem_id = create_problem()
    if not problem_id:
        print("❌ Masala yaratilmadi!")
        return
    
    # 2. Testcase yaratish
    if not create_testcase(problem_id):
        print("❌ Testcase yaratilmadi!")
        return
    
    # 3. Python submission
    python_code = """a = int(input())
b = int(input())
print(a + b)"""
    submit_solution(problem_id, "python", python_code)
    
    time.sleep(2)  # Bir oz kutish
    
    # 4. C++ submission
    cpp_code = """#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}"""
    submit_solution(problem_id, "cpp", cpp_code)
    
    time.sleep(2)  # Bir oz kutish
    
    # 5. JavaScript submission
    js_code = """const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let lines = [];
rl.on('line', (line) => {
    lines.push(parseInt(line));
    if (lines.length === 2) {
        console.log(lines[0] + lines[1]);
        rl.close();
    }
});"""
    submit_solution(problem_id, "js", js_code)
    
    print("\n✅ Barcha testlar yakunlandi!")
    print("\n💡 Natijalarni ko'rish uchun:")
    print("   1. Database'ga qarang (submissions jadvali)")
    print("   2. Celery worker loglarini tekshiring")
    print("   3. Docker container loglarini ko'ring")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Xatolik: Server ishlamayapti!")
        print("💡 Quyidagi command'ni ishga tushiring:")
        print("   docker-compose up -d")
    except Exception as e:
        print(f"\n❌ Xatolik: {e}")

