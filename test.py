import nltk



text = """
Prepare the Muffins: Adjust an oven rack to the upper-middle position and preheat the oven to 400 degrees F. Line a 12-cup muffin tin with paper liners or spray with non-stick cooking spray.
Melt 2 tablespoons of the butter in a 12-inch skillet over medium-high heat. Add the apples, brown sugar, ¼ teaspoon of the cinnamon. Cook, stirring often, until the moisture has completely evaporated and the apples are well browned, about 9 minutes. Remove the pan from the heat and allow to cool for 10 minutes.
Meanwhile, whisk the flour, baking powder, baking soda, salt and the remaining ½ teaspoon of ground cinnamon together in a large bowl.
Whisk the granulated sugar, eggs, oil, and 4 tablespoons of melted butter together in a medium bowl until thick, about 30 seconds. Whisk the cider, yogurt and vanilla into the sugar mixture until combined.
Fold the sugar mixture and the cooled apples into the flour mixture until just combined. Divide the batter evenly among the prepared muffin cups (there should be able ⅓ cup of batter per cup, and the cups will be filled to the rim).
Mix Together the Topping: In a small bowl, stir together the sugar, brown sugar and cinnamon for the topping. Sprinkle the muffin tops evenly with the topping.
Bake until golden brown and a toothpick inserted in the center comes out with a few moist crumbs attached, 18 to 22 minutes, rotating the muffin tin halfway through baking. Let the muffins cool in the muffin tin on a wire rack for 10 minutes. Remove the muffins from the pan and place on a wire cooling rack. Cool for 5 more minutes before serving. The muffins can be served warm or at room temperature. Store the muffins in an airtight container at room temperature for up to 3 days.

"""

#tokens = nltk.word_tokenize(text)

#tagged = nltk.pos_tag(tokens)

#entities = nltk.chunk.ne_chunk(tagged)

sentences = nltk.sent_tokenize(text)

tagged = [nltk.pos_tag(nltk.word_tokenize(sent)) for sent in sentences]