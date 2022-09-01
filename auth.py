class auth():
  def check_auth(request):
    if 'matrix' in request.cookies:
        return render_template(f'{language}/index.html')
      else:
