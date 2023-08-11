from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def some_input(request):
    # template = loader.get_template("news/some_input.html")
    # return HttpResponse(template.render())
    return render(request, "news/some_input.html")


def obr(request):
    some_text = request.POST["some_text"]
    
    # return HttpResponseRedirect(
    #     "/some_output",
    #     some_text=some_text
    # )
    # return redirect(f"/some_output?some_text={some_text}")
    # return redirect(reverse("/some_output"), args=(some_text, ))
    # return redirect(reverse("news:some", kwargs={"some_text" : some_text}))
    # return redirect(f"{reverse('news:some')}?some_text={some_text}")
    # return redirect(reverse("news:some"), args=[some_text])
    return redirect(reverse("news:some", kwargs={"some_text" : some_text}))
    # return redirect(reverse("news:some", kwargs={"some_text" : some_text}))

    
def some_output(request, some_text : str = "arr"):
    # some_text = request.GET["some_text"]
    # some_text = request.GET.get("some_text", 'arr')
    # template = loader.get_template("news/some_output.html")
    # context = {"some_text" : some_text}
    # return HttpResponse(template.render(context))
    return render(request, "news/some_output.html", {"some_text" : some_text})

