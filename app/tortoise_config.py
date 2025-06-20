from app.config import config

TORTOISE_ORM = {
	"connections": {
		"default": config.DB_URL.get_secret_value()
	},
	"apps": {
		"models": {
			"models": ["app.models.models", "aerich.models"],  
			"default_connection": "default",
		}
	}
}