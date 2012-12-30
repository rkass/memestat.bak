from django.shortcuts import render_to_response

def hello(request):
  content = {
  'background' : 'background6_2.png',

  'top_meme_text' : 'One Percent Cat',
  'top_meme_url' : 'http://www.reddit.com/r/AdviceAnimals/comments/157ec9/ so_the_world_didnt_end/',
  'top_meme_image' : 'onepercentcat.jpg',

  'hot_meme_text' : 'Reality Facing Bunny',
  'hot_meme_url' : 'http://www.reddit.com/r/AdviceAnimals/comments/15byvb/facing_reality_bunny/',
  'hot_meme_image' : 'realityfacingbunny.jpg',
  }
  return render_to_response('main.html', content)
