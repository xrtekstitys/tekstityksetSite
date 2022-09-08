class auth():
  def check_auth(request):
    if 'matrix' in request.cookies:
      return True
    else:
      return False