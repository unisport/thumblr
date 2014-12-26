from django.shortcuts import render

__author__ = 'smirnoffs'


def size_adding_view(request):
    return render(request, 'size_adding.html')