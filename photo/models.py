# 1. 모델 : 데이터베이스에 저장될 데이터가 있다면 해당 데이터를 묘사한다.
# 2. 뷰(기능) : 계산, 처리 - 실제 기능, 화면
# 3. URL 맵핑 : 라우팅 테이블에 기록한다. urls.py에 기록 - 주소를 지정
# 4. 화면에 보여줄 것이있다 : 템플릿작성(html)
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# 외래키(ForeignKey) - User 테이블에서 해당 유저를 찾을 수 있는 주키
# 주키(PrimaryKey) - User 테이블에 1 admin x x x x
class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'user_photos')
    # User 모델의 주키를 저장, CASCADE() 괄호는 즉시 호출, User입장에서 photo를 찾아올 때 해당유저가 작성한 사진 목록을 전부 가져올 수 있다.
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', default='photos/no_image.png') # default가 없으면 무조건 사진 업로드 해야함, pillow 라이브러리 설치해야함
    text = models.TextField() # default 없어도 됨
    created = models.DateTimeField(auto_now_add=True) # auto_now_add : 데이터베이스에 row가 새로 등록될 때 시간
    updated = models.DateTimeField(auto_now=True) # auto_now : 등록, 고쳐질때마다 시간

    # makemigrations -> migrate
    class Meta: # 옵션
         ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def get_absolute_url(self): # 글 수정되거나 완료되면 어디 url로 이동되느냐
        return reverse('photo:photo_detail', args=[self.id])