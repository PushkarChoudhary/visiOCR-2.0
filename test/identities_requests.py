# invalid request samples
curl -X POST -d "email=abc@email.com&username=abc@email.com&password1=password&password2=password" http://127.0.0.1:8000/api/v1/auth/register/
curl -X POST -d "username=abc@email.com&password=password&password2=password" http://127.0.0.1:8000/api/v1/auth/register/

# common password
curl -X POST -d "email=abc@email.com&username=abc@email.com&password=password&password2=password" http://127.0.0.1:8000/api/v1/auth/register/

# register
curl -X POST -d "email=abc@email.com&username=abc@email.com&password=Abc@1234&password2=Abc@1234" http://127.0.0.1:8000/api/v1/auth/register/

# get token (wrong credentials)
curl -X POST -d "username=abc@email.com&password=password" http://127.0.0.1:8000/api/v1/auth/token/

# get token
curl -X POST -d "username=abc@email.com&password=Abc@1234" http://127.0.0.1:8000/api/v1/auth/token/

# sample token
{
    "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyOTQ5MDY2NSwianRpIjoiZjY2ZTI0NjVhZDEwNDdkNWIxMjBkYmMzYmQwNzk1OTAiLCJ1c2VyX2lkIjoxfQ.z-QMaGTUN_DepJpdxcLLw_CkYCTugSl5_aGC1fJDKKo",
    "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5NDA0NTY1LCJqdGkiOiIzMWY1YTA5YjJlYjc0ZjYyYTgyOGI0ZDM1MTkxOTE5NyIsInVzZXJfaWQiOjF9.kRHaBSvYTaQKsXVAJui-jAA77i133DRA7wosQRFVXUo"
}

# get new token (refresh access token)
curl -X POST -d "refresh=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyOTQ5MDY2NSwianRpIjoiZjY2ZTI0NjVhZDEwNDdkNWIxMjBkYmMzYmQwNzk1OTAiLCJ1c2VyX2lkIjoxfQ.z-QMaGTUN_DepJpdxcLLw_CkYCTugSl5_aGC1fJDKKo" http://127.0.0.1:8000/api/v1/auth/token/refresh/

# sample token
{
    "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5NDA1MzU3LCJqdGkiOiI1MGJmYzhiYTFlMjg0NDNkODgyYjcwYzhhYTQxODdkZSIsInVzZXJfaWQiOjF9.0GlTmhWnLQVhlg8wOvaIHbVgb5HPDEcMBtMKRs98VE8"
}

# store token
#$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5NDEyODg3LCJqdGkiOiI0Yzc5MjFhNmMyZGU0MDU2YWQ4YTI1YzNmODk2MGQ1NyIsInVzZXJfaWQiOjF9.OFhOjDd1NF4GAoCqZ-NWP0gwekZaY6KP2t0dK_iHO3Y"

# get all identities
curl -X GET -H "Authorization: Bearer $token" http://127.0.0.1:8000/api/v1/identities/

# create a new identity
curl -X POST -d "name=Pushkar Choudhary&aadhaar=111122223333&pan=abcxy2233p&dob=12/06/2000&gender=Male" -H "Authorization: Bearer $token" http://127.0.0.1:8000/api/v1/identities/ 
curl -X POST -d "name=Ishan Karn&aadhaar=111122223393&pan=asdfg1122y&dob=11/11/2000&gender=Male" -H "Authorization: Bearer $token" http://127.0.0.1:8000/api/v1/identities/ 

# sample output
{"id":2,"name":"Ishan Karn","pan":"asdfg1122y","aadhaar":"111122223393","dob":"11/11/2000","gender":"Male","creator":"abc@email.com"}

# full update a new identity
curl -X PUT -d "name=Pushkar Kumar Choudhary&aadhaar=111122223388&pan=asdeg1122y&dob=11/11/2000&gender=Male" -H "Authorization: Bearer $token" http://127.0.0.1:8000/api/v1/identities/1/

# partial update a new identity
curl -X PATCH -d "dob=09/11/2000" -H "Authorization: Bearer $token" http://127.0.0.1:8000/api/v1/identities/2/

# delete a new identity
curl -X DELETE -H "Authorization: Bearer $token" http://127.0.0.1:8000/api/v1/identities/2/

# upload image for ocr
curl -X POST -F "title=alpha" -F "file=@pan4.jpg" http://127.0.0.1:8000/api/upload/