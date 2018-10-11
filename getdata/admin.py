from django.contrib import admin
from .models import Subject, AnatVariable, AnatValue, Sequence, Inclusion, FuncROImeanVariable, FuncROImeanValue, PathVariable

admin.site.register(Subject)
admin.site.register(FuncROImeanVariable)
admin.site.register(FuncROImeanValue)
admin.site.register(AnatValue)
admin.site.register(AnatVariable)
admin.site.register(Sequence)
admin.site.register(Inclusion)
admin.site.register(PathVariable)
