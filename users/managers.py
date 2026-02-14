from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Manager for custom User model with email as the unique identifier.
    """
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError("Поле email обязательно.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with staff privileges."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
