from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import DevStudents


@admin.register(DevStudents)
class DevStudentsAdmin(admin.ModelAdmin):
    list_display = ('sname', 'fname', 'email', 'active', 'creation_date')
    list_filter = ('active', 'creation_date')
    search_fields = ('fname', 'sname', 'email')
    ordering = ('-creation_date',)
    list_per_page = 20

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('fname', 'sname', 'email')
        }),
        ('Sécurité', {
            'fields': ('mot_de_passe',),
            'classes': ('collapse',),
            'description': "Section sensible - manipuler avec précaution"
        }),
        ('Statut', {
            'fields': ('active', 'creation_date'),
            'classes': ('wide',)
        }),
    )

    readonly_fields = ('creation_date',)

    def save_model(self, request, obj, form, change):
        """Hashage du mot de passe avant sauvegarde"""
        if obj.mot_de_passe and not obj.mot_de_passe.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2$')):
            obj.mot_de_passe = make_password(obj.mot_de_passe)
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """Rend les champs en lecture seule"""
        if obj:  # En mode édition
            return self.readonly_fields + ('email',)
        return self.readonly_fields

    def get_fieldsets(self, request, obj=None):
        """Adapte les fieldsets selon le contexte"""
        fieldsets = super().get_fieldsets(request, obj)
        if not obj:  # En mode création
            fieldsets[1][1]['classes'] = ()  # Affiche la section sécurité
        return fieldsets