# Backend Completion Plan - Config & Enums Improvements

## Step 1: Enhance `config.py`
- [x] Add validation: `SecretStr`, `PositiveInt`, `PostgresDsn`
- [x] Add missing API config: `APP_NAME`, `APP_VERSION`, `DEBUG`, `HOST`, `PORT`
- [x] Add CORS settings: `ALLOWED_ORIGINS: list[str]`
- [x] Add Scheduler config: `SCRAPER_INTERVAL_MINUTES`
- [x] Add Logging config: `LOG_LEVEL`, `LOG_FILE`
- [x] Add Token settings: `REFRESH_TOKEN_EXPIRE_DAYS`, `JWT_ISSUER`, `JWT_AUDIENCE`
- [x] Add `field_validator` for SECRET_KEY min length

## Step 2: Fix `enums.py` naming consistency
- [x] Fix enum values to use space-separated format
- [x] Add `CrewStatus` enum
- [x] Add `ImportStatus` enum
- [x] Add `NotificationType` enum
- [x] Add `UserStatus` enum

## Step 3: Update `main.py`
- [x] Use settings for APP_NAME and APP_VERSION

## Step 4: Update `jwt.py`
- [x] Use `settings.SECRET_KEY.get_secret_value()` for SecretStr type

## Step 5: Verify
- [x] Verify code compiles
- [x] Verify enum values load correctly
- [x] Verify Settings defaults load correctly

