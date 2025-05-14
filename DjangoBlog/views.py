# views.py
from ckeditor_uploader.views import upload
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ckeditor_uploader import views as ck_views
# 允许已登录用户上传
upload_view = login_required(ck_views.upload)
# 允许已登录用户查看服务器上的图片
browse_view = login_required(ck_views.browse)