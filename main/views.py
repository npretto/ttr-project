from django.shortcuts import render
from django.http import HttpResponse

import nltk
import requests
import re
from nltk.corpus import wordnet as wn

from lxml import html
from lxml import etree

import requests_cache
requests_cache.install_cache('http_cache', backend='sqlite', expire_after=None)



def index(request):

  if("text" in request.GET):
    text = request.GET['text']
  else:
    text = """
Adjust an oven rack to the upper-middle position and preheat the oven to 400 degrees F. Line a 12-cup muffin tin with paper liners or spray with non-stick cooking spray.
Melt 2 tablespoons of the butter in a 12-inch skillet over medium-high heat. Add the apples, brown sugar, ¼ teaspoon of the cinnamon. Cook, stirring often, until the moisture has completely evaporated and the apples are well browned, about 9 minutes. Remove the pan from the heat and allow to cool for 10 minutes.
Meanwhile, whisk the flour, baking powder, baking soda, salt and the remaining ½ teaspoon of ground cinnamon together in a large bowl.
Whisk the granulated sugar, eggs, oil, and 4 tablespoons of melted butter together in a medium bowl until thick, about 30 seconds. Whisk the cider, yogurt and vanilla into the sugar mixture until combined.
Fold the sugar mixture and the cooled apples into the flour mixture until just combined. Divide the batter evenly among the prepared muffin cups (there should be able ⅓ cup of batter per cup, and the cups will be filled to the rim).
Mix Together the Topping: In a small bowl, stir together the sugar, brown sugar and cinnamon for the topping. Sprinkle the muffin tops evenly with the topping.
Bake until golden brown and a toothpick inserted in the center comes out with a few moist crumbs attached, 18 to 22 minutes, rotating the muffin tin halfway through baking. Let the muffins cool in the muffin tin on a wire rack for 10 minutes. Remove the muffins from the pan and place on a wire cooling rack. Cool for 5 more minutes before serving. The muffins can be served warm or at room temperature. Store the muffins in an airtight container at room temperature for up to 3 days.
"""

  sentences = nltk.sent_tokenize(text)

  tagged = [nltk.pos_tag(nltk.word_tokenize(sent)) for sent in sentences]

  context = {"text" : text, "tagged_sentences" : tagged };

  return render(request, 'main/text_view.html', context)


def parse(request,url):
  context = {}
  context["url"] = url;

  page = requests.get(url)
  tree = html.fromstring(page.content)
  context['title'] = tree.xpath('//meta[@property="og:title"]/@content')[0]
  ingredients = tree.xpath('//span[@class="recipe-ingred_txt added"]/text()')
  steps = tree.xpath('//span[@class="recipe-directions__list--item"]/text()')

  #rimuovo le cose tra parentesi
  ingredients  = [re.sub('\(.*\)', '', sent) for sent in ingredients]

  ingredients = [nltk.word_tokenize(sent) for sent in ingredients]

  ingredients = [nltk.pos_tag(sent) for sent in ingredients]
  ingredients = tag_ingredients(ingredients)

  splitted_ingredients = split_ingredients(ingredients)


  #main_ingredients = get_main_ingredients(ingredients)

  context['ingredients'] = ingredients
  context['steps'] = steps
  context['splitted_ingredients'] = splitted_ingredients
  #context['main'] = main_ingredients
  #context['tagged_ingredients'] = tagged_ingredients

  return render(request, 'main/parse.html', context)

def split_ingredients(ingredients):
  ings = []
  for sentence in ingredients:
    quantity = []
    unit = []
    ing = []
    flavour = []
    for (word,pos_tag,tag) in sentence:
      if tag == "QNT":
        quantity.append(word)
      if tag == "UNIT":
        unit.append(word)
      if tag == "MAIN_ING":
        ing.append(word)
      if tag == "ING_NAME":
        flavour.append(word)
    ings.append( (" ".join(quantity)," ".join(unit)," ".join(ing)," ".join(flavour) ) )
  return ings


def get_main_ingredients(ingredients):
  main = []
  for sentence in ingredients:
    words = []
    for (word,pos_tag,tag) in sentence:
      if tag == "MAIN_ING":
        words.append(word)
    main.append(words)
  return main

def tag_ingredients(ingredients):
  return [[tag_word(word,pos_tag) for (word,pos_tag) in sent] for sent in ingredients]

def tag_word(word,pos_tag):
  #return (word, "AA")
  print("tagging " + word)
  hypers = get_hypers(word)
  tag = "ING_NAME";


  if 'containerful.n.01' in hypers or 'small_indefinite_quantity.n.01' in hypers:
    tag = "UNIT"

  for h in hypers:
    if 'unit' in h:
      tag = "UNIT"

  if pos_tag == "CD":
    tag = "QNT"

  if pos_tag in [",",":"]:
    tag = "IRR" #irrelevant
  
  if tag == "ING_NAME" and pos_tag in ["NN","NNS"]:
    tag = "MAIN_ING"

  return (word, pos_tag, tag)


def get_hypers(word):
  #return [syn.hypernyms()[0].name() for syn in wn.synsets(word)]
  hypers = []
  for syn in wn.synsets(word):
    try:
      hypers.append(syn.hypernyms()[0].name())
    except:
      pass
      
  print(hypers)
  return hypers
