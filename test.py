from django.utils import timezone
from django.utils.timezone import localtime # 追加

ima = timezone.now()
print(ima)
context = { 'now': ima }
print(context)