from django.shortcuts import render
from .models import Photo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def photo_list(request):
    # 보여줄 사진 데이터
    photos = Photo.objects.all() # ORM 매니저 이름이 objects 임
    return render(request, 'photo/list.html', {'photos' : photos})
    # templates 안의 photo 안의 list.html 라는말임, photos를 list.html 템플릿 안에서는 'photos' 라는 이름으로 쓰겠다 라는 말임
    # 원래 관례는 'object_list'가 기본 이름임

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect

class PhotoUploadView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['photo', 'text'] # 작성자(author), 작성시간(created) auto-now-add에 의해 자동으로 시간은 들어감
    template_name = 'photo/upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id # author는 필수항목이기 때문에 form의 유효성을 검사하기 전에 author를 매칭시켜줘야 한다.
        if form.is_valid():
            # 데이터가 올바르다면 저장을 하겠다
            form.instance.save() # instance가 뭐냐: model(Photo)의 팩토리패턴, 폼팩토리에서 포토 모델의 값을 입력받을 수 있는 폼을 생성해준다. 폼 안에는 포토 모델의 인스턴스가 존재한다.
            return redirect('/')
        else:
            return self.render_to_response({'form':form}) # form을 그대로 돌려주겠다.

class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = '/'
    template_name = 'photo/delete.html'


class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/update.html'

"""
서버에 이미지 파일을 업로드하거나 수정하거나 지운다.
장고 웹 앱이 해당 작업을 수행한다.
장고 웹 앱은 특정 서버에 업로드 되어 있다.
* 그럼 해당 기능은 특정 서버 안에서만 영향을 끼칠 수 있다.
-> 실 서비스를 배포하면 서버 컴퓨터는 1대가 아니다.
-> 사용자가 늘어날 때마다 섭 ㅓ컴퓨터도 늘어난다.
-> 장고 웹 앱이 업로드 되어있는 서버 컴퓨터가 늘어난다.
-> 이미지 파일이 업로드 되는 컴퓨터의 댓수도 늘어나야 한다.
-> 업로드 받은 후에 다른 서버에도 공유해줘야 한다.
-> 공유해주는데 사용되는 자원(돈이나 시간)이 아깝다.
-> 어떻게하면 공유하는데 들어가는 돈이나 시간을 절약할 수 있을까?
-> 이미지는 한 곳의 서버에다만 올려놓고, 거기에 접속해서 사용하자.
"""