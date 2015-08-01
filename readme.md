# Prodebate

## Setup
- Install Docker and docker-compose
- `git clone`
- `docker-compose up`

## To Do

### Sooner
- Edit things
- Add existing points as support/counter points
- Manifestation models.
	- Spin out into into its own app?
	- Refactor to allow the same URL to be applied to multiple notes
	- External URL or Prodebate position
- Private/draft points?

### Later
- I think URLs need to be drastically rethought. They weren't well-thought-out in the first place. I don't like how everything is pretty dependent on GET params. 
- Grandparents might need to go into the elaboration model because without that you can only ever respond to the parent point. See conceptual discussion.
- Unit tests! Models are really simple now (no methods to test) and views are in flux. If I stay with Django views for awhile I should write tests; if I go to DRF then the whole game changes.
- Refine comments. Kinda want to see how they're used first, though some Bootstrapping couldn't hurt 'em.

## Conceptual Discussions

### Grandparents

I say "school uniforms should be mandated" and the counterpoint is "the U.S. Constitution mandates freedom of expression", and I counter with "students are not guaranteed Constitutional rights", that last argument doesn't entirely make sense if the first argument isn't included. 

The most obvious solution then might be to add grandparent to the model if we're in a tree that has one. This would be the easiest from a technical and organization perspective, but the UI would take some thought to make sure it's intuitive. This is because you can't assume that someone wants their point to get a grandparent tag.

This might present some issues with duplicate content. A new point "Students are not guaranteed Constitutional rights" could have an elaboration as a counterpoint to parent "the U.S. Constitution mandates freedom of expression" and grandparent "school uniforms should be mandated", but "Christians should be allowed to proselytize" is a grandparent that *could* share the new point's elaboration text, but could also have slightly different text making it unique to that parent/grandparent chain.

### Duplicate Content
 
This site can get super messy, super fast. For example, "School uniforms should be mandated" and "School uniforms should not be mandated" can contain all the same arguments. The obvious solution would be to moderate to minimize that, but that creates other problems. "Marriage equality is a universal right" and "Marriage should not be redefined to include same-sex couples" could be lumped together and are going to share arguments, but anyone who is in favor of the latter would object to starting the debate under the umbrella of the former, and vice-versa. Or, if we were to consolidate the abortion debate, what terms do we use? "Pro-choice", "pro-reproductive freedom", "pro-baby murder", "pro-life", "anti-choice"? 

### Localization, granularity

Big issue. "School uniforms should be mandated" with counterpoint "the U.S. Constitution mandates freedom of expression" causes problems if original poster was in Brazil. "School uniforms should be mandated at primary schools in Rio de Janeiro" and "School uniforms should be mandated in all Italian public schools" would have a lot of the same arguments, but lumping them under the generic umbrella could take away interesting opportunities for discussion. Maybe there are specific things about primary schools in Rio that would make the debate different there. 

Tags/categorization could play a role here. Or there might be a way to centralize "School uniforms should be mandated" but have a "sister" point like "... in primary schools in Rio".

### Ownership / editing of positions

While working on the 'edit' feature, I realized that some questions need to be considered. Positions statements are different than, say, a Stack Exchange question title because argument trees could be built on specific wording. Stupid example, but if the position is "Hitler favored school uniforms" and I counter with "Reductio ad hiterlum", and then the position is edited to "Stalin favored school uniforms", the counterpoint becomes moot. On the flip side, a poorly-worded position could be improved by an edit. Also, that example really demonstrates a spot where moderation would step in - changing one word changes the entire position, so it shouldn't be allowed. 

Editing elaborations isn't as consequential and is a more likely use case of an editing feature. 

Also, who gets to edit stuff? I think ideally I'd like to follow Stack Exchange here - wiki-type revisions with history and certain editing privileges afforded to people who have the reptutation to do so. For now it'll just be a logged-in user; obviously that's not a long-term solution.

## Ideas

- Endorsements. Nonprofit organizations, political candidates, etc. could endorse ideas. If this became a commercial venture, for-profit orgs could as well. 
- Different filtering methods. Most well-cited. Most views. Most popular. Most controversial. Then people could decide how they want to parse the arguments.
- Underlying premises. Provide a way to add parent points, not just child points.
- Replace your news site/blog's comment section with prodebate trees. If I write an article about climate change where I advance three arguments, create three arguments in prodebate and have a way to embed them. That way their comment section provides more structured conversation, and content added can join the prodebate site at large. If a user can pull other arguments out of the article, they can always add to prodebate but the author could also include new arguments in the discussion.
- What if we made an argument 'spec', like the CommonMark or ePub or HTML5 specs? Put all the rules out there, then make it accessible to everyone.