runserver:
	uvicorn main:app --reload --port 8001

tunnel:
	ssh -p 2222 -R app:80:localhost:8001 timur@tun.romanenko-dev.ru