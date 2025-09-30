from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'is_active', 'created_at', 'last_login')
    list_filter = ('is_active', 'role', 'created_at')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)


@admin.register(ServerTemplate)
class ServerTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_id', 'name', 'minecraft_version', 'server_type', 'is_public', 'created_by', 'download_count')
    list_filter = ('is_public', 'minecraft_version', 'server_type')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)


@admin.register(ServerConfig)
class ServerConfigAdmin(admin.ModelAdmin):
    list_display = ('config_id', 'config_name', 'user', 'minecraft_version', 'server_type', 'ram_mb', 'max_players', 'created_at')
    list_filter = ('minecraft_version', 'server_type', 'online_mode', 'pvp_enabled')
    search_fields = ('config_name', 'user__username')
    ordering = ('-created_at',)


@admin.register(Mod)
class ModAdmin(admin.ModelAdmin):
    list_display = ('mod_id', 'mod_name', 'mod_version', 'minecraft_version', 'author', 'category', 'is_verified')
    list_filter = ('is_verified', 'minecraft_version', 'category', 'mod_type')
    search_fields = ('mod_name', 'author', 'description')
    ordering = ('mod_name',)


@admin.register(ConfigMod)
class ConfigModAdmin(admin.ModelAdmin):
    list_display = ('config_mod_id', 'config', 'mod', 'load_order', 'is_enabled')
    list_filter = ('is_enabled',)
    ordering = ('config', 'load_order')


@admin.register(ModIncompatibility)
class ModIncompatibilityAdmin(admin.ModelAdmin):
    list_display = ('incompatibility_id', 'mod_id_1', 'mod_id_2', 'conflict_type')
    list_filter = ('conflict_type',)
    search_fields = ('mod_id_1__mod_name', 'mod_id_2__mod_name')


@admin.register(RunningServer)
class RunningServerAdmin(admin.ModelAdmin):
    list_display = ('server_id', 'user', 'config', 'status', 'server_ip', 'server_port', 'player_count', 'last_activity')
    list_filter = ('status', 'user', 'config__minecraft_version')
    search_fields = ('user__username', 'config__config_name')
    ordering = ('-last_activity',)


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('error_id', 'config', 'error_type', 'severity', 'mod', 'created_at')
    list_filter = ('severity', 'error_type', 'created_at')
    search_fields = ('error_message', 'config__config_name')
    ordering = ('-created_at',)


@admin.register(ModDependency)
class ModDependencyAdmin(admin.ModelAdmin):
    list_display = ('dependency_id', 'mod', 'required_mod', 'is_required')
    list_filter = ('is_required',)
    search_fields = ('mod__mod_name', 'required_mod__mod_name')


@admin.register(ServerBackup)
class ServerBackupAdmin(admin.ModelAdmin):
    list_display = ('backup_id', 'server', 'backup_name', 'file_size', 'is_automatic', 'created_at')
    list_filter = ('is_automatic', 'created_at')
    search_fields = ('backup_name', 'server__config__config_name')
    ordering = ('-created_at',)


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'ip_address', 'expires_at', 'created_at')
    list_filter = ('expires_at',)
    search_fields = ('user__username', 'ip_address')
    ordering = ('-created_at',)


@admin.register(ServerStatistic)
class ServerStatisticAdmin(admin.ModelAdmin):
    list_display = ('stat_id', 'server', 'players_online', 'memory_usage', 'cpu_usage', 'tps', 'timestamp')
    list_filter = ('server',)
    ordering = ('-timestamp',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'amount', 'currency', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'currency', 'payment_method')
    search_fields = ('user__username',)
    ordering = ('-created_at',)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_id', 'name', 'price', 'currency', 'max_ram', 'max_players', 'max_servers')
    list_filter = ('currency',)
    ordering = ('price',)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscription_id', 'user', 'plan', 'status', 'start_date', 'end_date', 'auto_renew')
    list_filter = ('status', 'auto_renew', 'plan')
    search_fields = ('user__username',)
    ordering = ('-start_date',)


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'user', 'title', 'status', 'priority', 'created_at', 'closed_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'user__username', 'description')
    ordering = ('-created_at',)


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'ticket', 'user', 'is_internal', 'created_at')
    list_filter = ('is_internal', 'created_at')
    search_fields = ('message_text', 'user__username')
    ordering = ('-created_at',)


@admin.register(ServerLog)
class ServerLogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'server', 'log_level', 'timestamp', 'message_preview')
    list_filter = ('log_level', 'server', 'timestamp')
    search_fields = ('message',)
    ordering = ('-timestamp',)

    def message_preview(self, obj):
        return obj.message[:60] + '...' if len(obj.message) > 60 else obj.message
    message_preview.short_description = 'Message Preview'


@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    list_display = ('world_id', 'server', 'world_name', 'world_size', 'created_at', 'last_modified')
    search_fields = ('world_name', 'server__config__config_name')
    ordering = ('-created_at',)


@admin.register(PlayerStat)
class PlayerStatAdmin(admin.ModelAdmin):
    list_display = ('stat_id', 'server', 'player_name', 'player_uuid', 'play_time', 'blocks_mined', 'mobs_killed', 'deaths', 'last_seen')
    list_filter = ('server',)
    search_fields = ('player_name', 'player_uuid')
    ordering = ('-last_seen',)