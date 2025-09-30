from django.db import models

from django.db import models
from django.conf import settings

class CustomUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=50)
    avatar_url = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'Users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class ServerTemplate(models.Model):
    template_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    minecraft_version = models.CharField(max_length=50)
    server_type = models.CharField(max_length=100)
    recommended_ram = models.IntegerField()
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='created_by')
    download_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Server_Templates'
        verbose_name = 'Шаблон сервера'
        verbose_name_plural = 'Шаблоны серверов'

    def __str__(self):
        return self.name


class ServerConfig(models.Model):
    config_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='user_id')
    config_name = models.CharField(max_length=255)
    minecraft_version = models.CharField(max_length=50)
    server_type = models.CharField(max_length=100)
    ram_mb = models.IntegerField()
    max_players = models.IntegerField()
    difficulty = models.CharField(max_length=50, null=True, blank=True)
    game_mode = models.CharField(max_length=50, null=True, blank=True)
    world_seed = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    template = models.ForeignKey(ServerTemplate, on_delete=models.SET_NULL, null=True, blank=True, db_column='template_id')
    view_distance = models.IntegerField()
    online_mode = models.BooleanField(default=True)
    pvp_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'Server_Configs'
        verbose_name = 'Конфигурация сервера'
        verbose_name_plural = 'Конфигурации серверов'
    def __str__(self):
        return self.config_name


class Mod(models.Model):
    mod_id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100)
    download_url = models.URLField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    mod_name = models.CharField(max_length=255)
    mod_version = models.CharField(max_length=50)
    minecraft_version = models.CharField(max_length=50)
    mod_type = models.CharField(max_length=100)
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()

    class Meta:
        db_table = 'Mods'
        verbose_name = 'Мод'
        verbose_name_plural = 'Моды'

    def __str__(self):
        return f"{self.mod_name} v{self.mod_version}"


class ConfigMod(models.Model):
    config_mod_id = models.AutoField(primary_key=True)
    config = models.ForeignKey(ServerConfig, on_delete=models.CASCADE, db_column='config_id')
    mod = models.ForeignKey(Mod, on_delete=models.CASCADE, db_column='mod_id')
    load_order = models.IntegerField()
    is_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'Config_Mods'
        verbose_name = 'Конфигурация мода'
        verbose_name_plural = 'Конфигурации модов'

    def __str__(self):
        return f"{self.config.config_name} - {self.mod.mod_name}"


class ModIncompatibility(models.Model):
    incompatibility_id = models.AutoField(primary_key=True)
    mod_id_1 = models.ForeignKey(Mod, on_delete=models.CASCADE, related_name='incompatibilities_as_first', db_column='mod_id_1')
    mod_id_2 = models.ForeignKey(Mod, on_delete=models.CASCADE, related_name='incompatibilities_as_second', db_column='mod_id_2')
    conflict_type = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Mod_Incompatibilities'
        verbose_name = 'Несовместимость мода'
        verbose_name_plural = 'Несовместимость модов'

    def __str__(self):
        return f"{self.mod_id_1} ↔ {self.mod_id_2} ({self.conflict_type})"


class RunningServer(models.Model):
    server_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='user_id')
    config = models.ForeignKey(ServerConfig, on_delete=models.CASCADE, db_column='config_id')
    server_ip = models.GenericIPAddressField(null=True, blank=True)
    server_port = models.IntegerField()
    status = models.CharField(max_length=50) 
    start_time = models.DateTimeField(null=True, blank=True)
    stop_time = models.DateTimeField(null=True, blank=True)
    cpu_usage = models.FloatField(null=True, blank=True)
    memory_usage_mb = models.IntegerField(null=True, blank=True)
    player_count = models.IntegerField(default=0)
    uptime_seconds = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Running_Servers'
        verbose_name = 'Запуск сервера'
        verbose_name_plural = 'Запуск серверов'

    def __str__(self):
        return f"Server {self.server_id} ({self.status})"


class ErrorLog(models.Model):
    error_id = models.AutoField(primary_key=True)
    config = models.ForeignKey(ServerConfig, on_delete=models.CASCADE, db_column='config_id')
    error_type = models.CharField(max_length=100)
    error_message = models.TextField()
    mod = models.ForeignKey(Mod, on_delete=models.SET_NULL, null=True, blank=True, db_column='mod_id')
    severity = models.CharField(max_length=50)  
    created_at = models.DateTimeField(auto_now_add=True)
    server = models.ForeignKey(RunningServer, on_delete=models.SET_NULL, null=True, blank=True, db_column='server_id')

    class Meta:
        db_table = 'Error_Logs'
        verbose_name = 'Лог ошибки'
        verbose_name_plural = 'Логи ошибок'

    def __str__(self):
        return f"{self.error_type} ({self.severity})"


class ModDependency(models.Model):
    dependency_id = models.AutoField(primary_key=True)
    mod = models.ForeignKey(Mod, on_delete=models.CASCADE, related_name='dependencies', db_column='mod_id')
    required_mod = models.ForeignKey(Mod, on_delete=models.CASCADE, related_name='required_by', db_column='required_mod_id')
    is_required = models.BooleanField(default=True)

    class Meta:
        db_table = 'Mod_Dependencies'
        verbose_name = 'Зависимость мода'
        verbose_name_plural = 'Зависимости модов'

    def __str__(self):
        req = "required" if self.is_required else "optional"
        return f"{self.mod} depends on {self.required_mod} ({req})"


class ServerBackup(models.Model):
    backup_id = models.AutoField(primary_key=True)
    server = models.ForeignKey(RunningServer, on_delete=models.CASCADE, db_column='server_id')
    backup_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    file_size = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_automatic = models.BooleanField(default=False)

    class Meta:
        db_table = 'Server_Backups'
        verbose_name = 'Бэкап сервера'
        verbose_name_plural = 'Бэкапы серверов'

    def __str__(self):
        return self.backup_name


class UserSession(models.Model):
    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='user_id')
    session_token = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'User_Sessions'
        verbose_name = 'Бэкап сервера'
        verbose_name_plural = 'Бэкапы серверов'

    def __str__(self):
        return f"Session for {self.user.username}"


class ServerStatistic(models.Model):
    stat_id = models.AutoField(primary_key=True)
    server = models.ForeignKey(RunningServer, on_delete=models.CASCADE, db_column='server_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    players_online = models.IntegerField()
    memory_usage = models.IntegerField() 
    cpu_usage = models.FloatField()
    tps = models.FloatField()  

    class Meta:
        db_table = 'Server_Statistics'
        verbose_name = 'Статистика сервера'
        verbose_name_plural = 'Статистика серверов'

    def __str__(self):
        return f"Stats for {self.server} at {self.timestamp}"


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='user_id')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=50)  
    payment_method = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'Payments'
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"


class SubscriptionPlan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    max_ram = models.IntegerField()
    max_players = models.IntegerField()
    max_servers = models.IntegerField()
    features = models.TextField()  

    class Meta:
        db_table = 'Subscription_Plans'
        verbose_name = 'План подписки'
        verbose_name_plural = 'Планы подписки'

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='user_id')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, db_column='plan_id')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=50)
    auto_renew = models.BooleanField(default=False)

    class Meta:
        db_table = 'User_Subscriptions'
        verbose_name = 'Подписка пользователя'
        verbose_name_plural = 'Подписки пользователей'

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"


class SupportTicket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='user_id')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=20)  
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'Support_Tickets'
        verbose_name = 'Тикет поддержки'
        verbose_name_plural = 'Тикеты поддержки'

    def __str__(self):
        return f"Ticket #{self.ticket_id}: {self.title}"


class TicketMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, db_column='ticket_id')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='user_id')
    message_text = models.TextField()
    is_internal = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Ticket_Messages'
        verbose_name = 'Сообщение тикета'
        verbose_name_plural = 'Сообщение тикета'

    def __str__(self):
        return f"Message in #{self.ticket.ticket_id}"


class ServerLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    server = models.ForeignKey(RunningServer, on_delete=models.CASCADE, db_column='server_id')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    log_level = models.CharField(max_length=20) 

    class Meta:
        db_table = 'Server_Logs'
        verbose_name = 'Логи сервера'
        verbose_name_plural = 'Логи сервера'

    def __str__(self):
        return f"[{self.log_level}] {self.message[:50]}..."


class World(models.Model):
    world_id = models.AutoField(primary_key=True)
    server = models.ForeignKey(RunningServer, on_delete=models.CASCADE, db_column='server_id')
    world_name = models.CharField(max_length=255)
    world_size = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Worlds'
        verbose_name = 'Мир'
        verbose_name_plural = 'Миры'

    def __str__(self):
        return self.world_name


class PlayerStat(models.Model):
    stat_id = models.AutoField(primary_key=True)
    server = models.ForeignKey(RunningServer, on_delete=models.CASCADE, db_column='server_id')
    player_uuid = models.CharField(max_length=36)  # UUID4
    player_name = models.CharField(max_length=16)
    play_time = models.IntegerField()  # seconds
    blocks_mined = models.IntegerField(default=0)
    mobs_killed = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Player_Stats'
        verbose_name = 'Игровая статистика'
        verbose_name_plural = 'Игровые статистики'

    def __str__(self):
        return f"{self.player_name} on {self.server}"