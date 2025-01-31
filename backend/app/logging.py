import logging
import logging.config

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True,
        },  
        "uvicorn": {
            "level": "INFO",
            "handlers": ["default"],
        },
        "sqlalchemy.engine": {
            "level": "WARNING",
            "handlers": ["default"],
        },
    },
}

logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)