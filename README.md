# JWT Marketplace API
API sederhana dengan JWT untuk autentikasi & manajemen profile.

# Cara Menjalankannya
1. pip install -r requirements.txt
2. buat file .env berdasarkan .env.example
3. python app.py

# Endpointnya
- POST /auth/login  → login dan dapatkan token JWT
- GET /items        → publik
- PUT /profile      → butuh token JWT

## Contoh Postman/cURL
curl -X POST http://localhost:5000/auth/login '{"email":"dadar1@example.com","password":"dadar123"}'
